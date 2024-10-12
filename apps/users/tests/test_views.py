import os
from datetime import timedelta, datetime
from unittest.mock import patch
from urllib.parse import urlencode

import jwt
from django.conf import settings
from django.core.files.uploadedfile import SimpleUploadedFile
from django.shortcuts import Http404
from django.urls import reverse
from model_bakery import baker
from rest_framework import status
from rest_framework.test import APIRequestFactory, APITestCase
from rest_framework_simplejwt.tokens import AccessToken
from rest_framework_simplejwt.tokens import RefreshToken

from apps.users.models import User
from apps.users.views import UsersListAPI
from utils import JWT_token


class TestUsersListAPI(APITestCase):
    @classmethod
    def setUpTestData(cls):
        baker.make(User, 34)

    def setUp(self):
        self.factory = APIRequestFactory()
        self.user = baker.make(User, username='username', email='email@gmail.com', password='password', is_active=True)
        self.not_active_user = baker.make(User, username='not_active', email='not_active@gmail.com',
                                          password='password')
        self.user_token = str(AccessToken.for_user(self.user))
        self.admin = baker.make(User, username='admin', email='admin@gmail.com', password='admin', is_active=True,
                                is_admin=True)
        self.admin_token = str(AccessToken.for_user(self.admin))
        self.url = reverse('users:users-list')

    def test_permission_denied(self):
        request = self.factory.get(self.url, HTTP_AUTHORIZATION='Bearer ' + self.user_token)
        response = UsersListAPI.as_view()(request)
        self.assertEqual(response.status_code, 403)

    def test_list_GET(self):
        request = self.factory.get(self.url, HTTP_AUTHORIZATION='Bearer ' + self.admin_token)
        response = UsersListAPI.as_view()(request)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data['data']), 10)

    def test_list_paginated_GET(self):
        request = self.factory.get(f"{self.url}?{urlencode({'page': 2})}",
                                   HTTP_AUTHORIZATION='Bearer ' + self.admin_token)
        response = UsersListAPI.as_view()(request)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data['data']), 10)


class TestUserRegisterAPI(APITestCase):
    @classmethod
    def setUpTestData(cls):
        baker.make(User, is_active=True, username='username', email='email')

    def setUp(self):
        self.url = reverse('users:user-register')
        self.valid_data = {
            'username': 'kevin',
            'email': 'kevin@example.com',
            'password': 'asdF@123',
            'password2': 'asdF@123',
        }
        self.invalid_data = {
            'username': 'username',
            'email': 'amir@example.com',
            'password': 'asdF@123',
            'password2': 'asdF@123',
        }

    def test_success_register(self):
        response = self.client.post(self.url, data=self.valid_data)
        self.assertEqual(response.status_code, 201)
        self.assertIn('message', response.data['data'])
        self.assertIn('data', response.data)
        self.assertEqual(User.objects.all().count(), 2)

    def test_not_unique_username(self):
        response = self.client.post(self.url, data=self.invalid_data)
        self.assertEqual(response.status_code, 400)
        self.assertIn('errors', response.data)
        self.assertIn('username', response.data['errors'])

    def test_mismatch_password(self):
        self.invalid_data['password'] = '<PASSWORD>'
        self.invalid_data['username'] = 'testuser'
        response = self.client.post(self.url, data=self.invalid_data)
        self.assertEqual(response.status_code, 400)
        self.assertIn('errors', response.data)

    def test_register_with_avatar(self):
        self.valid_data['avatar'] = 'avatar.png'
        response = self.client.post(self.url, data=self.valid_data)
        self.assertEqual(response.status_code, 201)


class TestUserRegisterVerificationAPI(APITestCase):
    def setUp(self):
        self.url = reverse('users:user-register-verify', args=['invalid_token'])
        self.user = baker.make(User, is_active=False)
        self.token = JWT_token.generate_activation_token(self.user, timedelta(minutes=1))

    def create_expired_token(self):
        payload = {
            'user_id': self.user.id,
            'exp': datetime.now() - timedelta(days=34)
        }
        return jwt.encode(payload, settings.SECRET_KEY, algorithm='HS256')

    def test_account_activation_success(self):
        response = self.client.get(self.url.replace('invalid_token', self.token))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('message', response.data)
        self.assertEqual(response.data['message'], 'Account activated successfully.')
        self.user.refresh_from_db()
        self.assertTrue(self.user.is_active)

    def test_account_already_active(self):
        self.user.is_active = True
        self.user.save()
        response = self.client.get(self.url.replace('invalid_token', self.token))
        self.assertEqual(response.status_code, status.HTTP_409_CONFLICT)
        self.assertIn('message', response.data)
        self.assertEqual(response.data['message'], 'this account already is active.')

    @patch('apps.users.views.JWT_token.get_object_or_404')
    def test_activation_url_invalid(self, mock_jwt_decode_token):
        mock_jwt_decode_token.side_effect = Http404
        response = self.client.get(self.url.replace('invalid_token', self.token))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertIn('error', response.data)
        self.assertEqual(response.data['error'], 'Activation URL is invalid')

    def test_invalid_token(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 400)
        self.assertIn('error', response.data)
        self.assertEqual(response.data['error'], 'Activation link is invalid!')

    def test_expired_token(self):
        expired_token = self.create_expired_token()
        response = self.client.get(self.url.replace('invalid_token', expired_token))
        self.assertEqual(response.status_code, 400)
        self.assertIn('error', response.data)
        self.assertEqual(response.data['error'], 'Activation link has expired!')


class TestResendVerificationEmailAPI(APITestCase):
    def setUp(self):
        self.url = reverse('users:user-register-resend-email')
        self.user = baker.make(User, is_active=False, email='email@gmail.com')
        self.active_user = baker.make(User, is_active=True, email='active_user@gmail.com')

    def test_successful_send_email(self):
        data = {'email': 'email@gmail.com'}
        response = self.client.post(self.url, data=data)
        self.assertEqual(response.status_code, 202)
        self.assertIn('message', response.data)
        self.assertEqual(response.data['message'], 'We`ve resent the activation link to your email.')

    @patch('utils.send_email.send_link')
    def test_invalid_email(self, mock_send_email):
        data = {'email': 'does_not_exists_user_email@gmail.com'}
        response = self.client.post(self.url, data=data)
        self.assertEqual(response.status_code, 400)
        self.assertIn('errors', response.data)
        self.assertEqual(response.data['errors']['non_field_errors'][0], 'User does not exist!')
        mock_send_email.assert_not_called()

    @patch('utils.send_email.send_link')
    def test_active_user_email(self, mock_send_email):
        data = {'email': 'active_user@gmail.com'}
        response = self.client.post(self.url, data=data)
        self.assertEqual(response.status_code, 400)
        self.assertIn('errors', response.data)
        self.assertEqual(response.data['errors']['non_field_errors'][0], 'Account already active!')
        mock_send_email.assert_not_called()


class TestChangePasswordAPI(APITestCase):
    def setUp(self):
        self.user = baker.make(User, is_active=True)
        self.user.set_password('kmk13245')
        self.user.save()
        self.token = str(RefreshToken.for_user(self.user).access_token)
        self.url = reverse('users:change-password')
        self.valid_data = {
            'old_password': 'kmk13245',
            'new_password': 'asdF@123',
            'confirm_new_password': 'asdF@123',
        }
        self.invalid_data = {
            'old_password': 'invalid_password',
            'new_password': 'asdF@123',
            'confirm_new_password': 'asdF@123',
        }

    def test_successful_change_password(self):
        response = self.client.put(self.url, data=self.valid_data, HTTP_AUTHORIZATION='Bearer ' + str(self.token))
        self.user.refresh_from_db()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['message'], 'Your password changed successfully.')
        self.assertTrue(self.user.check_password(self.valid_data['new_password']))

    def test_invalid_old_password(self):
        response = self.client.put(self.url, data=self.invalid_data, HTTP_AUTHORIZATION='Bearer ' + str(self.token))
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data['errors']['old_password'][0], 'Your old password is not correct.')


class TestSetPasswordAPI(APITestCase):
    def setUp(self):
        self.user = baker.make(User, is_active=True)
        self.token = JWT_token.generate_activation_token(self.user, timedelta(minutes=1))
        self.url = reverse('users:set-password', args=[self.token])

    def test_successful_set_password(self):
        data = {'new_password': 'asdF@123', 'confirm_new_password': 'asdF@123'}
        response = self.client.post(self.url, data)
        self.user.refresh_from_db()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['message'], 'Password changed successfully.')
        self.assertTrue(self.user.check_password(data['new_password']))

    @patch('apps.users.views.JWT_token.get_object_or_404')
    def test_invalid_token_user(self, mock_not_found):
        data = {'new_password': 'asdF@123', 'confirm_new_password': 'asdF@123'}
        mock_not_found.side_effect = Http404
        response = self.client.post(self.url, data)
        self.user.refresh_from_db()
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.data['error'], 'Activation URL is invalid')
        self.assertFalse(self.user.check_password(data['new_password']))


class TestResetPasswordAPI(APITestCase):
    def setUp(self):
        self.user = baker.make(User, is_active=True, email='email@gmail.com')
        self.url = reverse('users:reset-password')

    def test_successful_reset(self):
        data = {'email': 'email@gmail.com'}
        response = self.client.post(self.url, data=data)
        self.assertEqual(response.status_code, 202)
        self.assertEqual(response.data['message'], 'A password reset link has been sent to your email.')

    def test_invalid_email(self):
        data = {'email': 'invalidemail@gmail.com'}
        response = self.client.post(self.url, data=data)
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.data['errors'], 'user with this Email not found.')


class TestBlockTokenAPI(APITestCase):
    def setUp(self):
        self.user = baker.make(User, is_active=True)
        self.token = str(RefreshToken.for_user(self.user))
        self.invalid_token = 'invalid.token.alksdjfadffeygfhasjf'
        self.url = reverse('users:token-block')

    @patch('rest_framework_simplejwt.tokens.BlacklistMixin.blacklist')
    def test_successful_block_token(self, mock_black_list):
        data = {'refresh': self.token}
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, 204)
        self.assertEqual(response.data['message'], 'Token blocked successfully!')
        mock_black_list.assert_called_once()

    def test_block_invalid_token(self):
        data = {'refresh': self.invalid_token}
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data['errors']['refresh'], 'The provided token is invalid or has expired.')


class TestUserProfileAPI(APITestCase):
    def setUp(self):
        self.user = baker.make(User, is_active=True)
        self.token = JWT_token.generate_token(self.user)['token']

    def test_retrieve_user_profile_GET(self):
        url = reverse('users:user_profile', args=[self.user.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['username'], self.user.username)
        self.assertEqual(response.data['score'], 0)

    def test_retrieve_user_profile_not_found(self):
        url = reverse('users:user_profile', args=[23])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.data['detail'], 'No User matches the given query.')

    @patch('storages.backends.s3boto3.S3Boto3Storage.save', return_value='test/avatar.png')
    def test_partial_update_user_profile(self, mock_save):
        base_dir = os.path.dirname(os.path.abspath(__file__))
        image_path = os.path.join(base_dir, 'test_data/images/test.png')

        with open(image_path, 'rb') as image:
            avatar = SimpleUploadedFile(
                'avatar.png',
                image.read(),
                content_type='image/png'
            )
        data = {'username': 'new_username', 'avatar': avatar}
        url = reverse('users:user_profile', args=[1])
        response = self.client.patch(url, data, HTTP_AUTHORIZATION='Bearer ' + self.token)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['message'], 'Updated profile successfully.')
        self.user.refresh_from_db()
        self.assertEqual(self.user.username, 'new_username')
        self.assertTrue(self.user.profile.avatar.name.endswith('avatar.png'))

    @patch('apps.users.views.send_verification_email.delay_on_commit')
    def test_update_email(self, mock_send_email_task):
        data = {'email': 'email@email.com'}
        url = reverse('users:user_profile', args=[1])
        response = self.client.patch(url, data, HTTP_AUTHORIZATION='Bearer ' + self.token)
        mock_send_email_task.assert_called_once()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.user.refresh_from_db()
        self.assertFalse(self.user.is_active)
        self.assertEqual(self.user.email, 'email@email.com')

    @patch('apps.users.views.bucket.bucket.delete_object')
    def test_delete_account(self, mock_delete_avatar):
        url = reverse('users:user_profile', args=[1])
        response = self.client.delete(url, HTTP_AUTHORIZATION='Bearer ' + self.token)
        self.assertEqual(response.status_code, 200)
        self.assertNotIn(self.user, User.objects.all())
