from urllib.parse import urlencode

from model_bakery import baker
from rest_framework.test import APIRequestFactory
from rest_framework.test import APITestCase
from rest_framework_simplejwt.tokens import AccessToken

from users.views import *


class TestUsersListAPI(APITestCase):
    @classmethod
    def setUpTestData(cls):
        baker.make(User, 34)

    def setUp(self):
        self.factory = APIRequestFactory()
        self.user = baker.make(User, username='username', email='email@gmail.com', password='password', is_active=True)
        self.not_active_user = baker.make(User, username='not_active', email='not_active@gmail.com',
                                          password='password')
        self.user_token = self.get_JWT_token(self.user)
        self.admin = baker.make(User, username='admin', email='admin@gmail.com', password='admin', is_active=True,
                                is_admin=True)
        self.admin_token = self.get_JWT_token(self.admin)

    def get_JWT_token(self, user):
        token = AccessToken.for_user(user)
        return str(token)

    def test_permission_denied(self):
        request = self.factory.get(reverse('users:users_list'), HTTP_AUTHORIZATION='Bearer ' + self.user_token)
        response = UsersListAPI.as_view()(request)
        self.assertEqual(response.status_code, 403)

    def test_list_GET(self):
        request = self.factory.get(reverse('users:users_list'), HTTP_AUTHORIZATION='Bearer ' + self.admin_token)
        response = UsersListAPI.as_view()(request)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data['results']), 20)

    def test_list_paginated_GET(self):
        request = self.factory.get(f"{reverse('users:users_list')}?{urlencode({'page': 2})}",
                                   HTTP_AUTHORIZATION='Bearer ' + self.admin_token)
        response = UsersListAPI.as_view()(request)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data['results']), 17)


class TestUserRegisterAPI(APITestCase):
    @classmethod
    def setUpTestData(cls):
        baker.make(User, is_active=True)

    def setUp(self):
        self.factory = APIRequestFactory()

    def test_success_register(self):
        data = {
            'username': 'username',
            'email': 'email@gmail.com',
            'password': 'asdF@123',
            'password2': 'asdF@123'
        }
        response = self.client.post(reverse('users:user_register'), data)
        self.assertEqual(response.status_code, 200)
