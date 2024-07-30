from model_bakery import baker
from rest_framework.test import APITestCase

from users.models import User
from users.serializers import (
    UserSerializer,
    UserRegisterSerializer
)


class TestUserSerializer(APITestCase):
    @classmethod
    def setUpTestData(cls):
        baker.make(User, username='username', email='email@gmail.com', is_active=True)

    def test_valid_data(self):
        data = {'username': 'kevin', 'email': 'kevin@gmail.com', 'password': 'password', 'is_active': True}
        serializer = UserSerializer(data=data)
        self.assertTrue(serializer.is_valid())
        self.assertEqual(serializer.validated_data['username'], 'kevin')

    def test_empty_fields(self):
        serializer = UserSerializer(data={})
        self.assertFalse(serializer.is_valid())
        self.assertEqual(len(serializer.errors), 2)

    def test_invalid_username(self):
        data = {'username': 'username', 'email': 'another_email@gmail.com', 'password': 'password'}
        serializer = UserSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertEqual(len(serializer.errors), 1)
        self.assertEqual(serializer.errors['username'][0], 'user with this username already exists.')

    def test_invalid_email(self):
        data = {'username': 'another_username', 'email': 'email@gmail.com', 'password': 'password'}
        serializer = UserSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertEqual(len(serializer.errors), 1)
        self.assertEqual(serializer.errors['email'][0], 'user with this email already exists.')


class TestUserRegisterSerializer(APITestCase):
    @classmethod
    def setUpTestData(cls):
        baker.make(User, username='username', email='email@gmail.com', is_active=True)

    def test_valid_data(self):
        data = {'username': 'kevin', 'email': 'kevin@gmail.com', 'password': 'asdF@123', 'password2': 'asdF@123'}
        serializer = UserRegisterSerializer(data=data)
        self.assertTrue(serializer.is_valid())
        self.assertEqual(serializer.validated_data['username'], 'kevin')

    def test_common_password(self):
        data = {'username': 'kevin', 'email': 'kevin@gmail.com', 'password': 'password', 'password2': 'password'}
        serializer = UserRegisterSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertEqual(len(serializer.errors), 1)
        self.assertEqual(serializer.errors['non_field_errors'][0], 'This password is too common.')

    def test_passwords_dont_match(self):
        data = {'username': 'kevin', 'email': 'kevin@gmail.com', 'password': 'password', 'password2': 'not_matched'}
        serializer = UserRegisterSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertEqual(len(serializer.errors), 1)
        self.assertEqual(serializer.errors['non_field_errors'][0], 'Passwords must match.')

    def test_not_unique_username(self):
        data = {'username': 'username', 'email': 'kevin@gmail.com', 'password': 'asdF@123', 'password2': 'asdF@123'}
        serializer = UserRegisterSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertEqual(len(serializer.errors), 1)
        self.assertEqual(serializer.errors['username'][0], 'user with this username already exists.')

    def test_not_unique_email(self):
        data = {'username': 'kevin', 'email': 'email@gmail.com', 'password': 'asdF@123', 'password2': 'asdF@123'}
        serializer = UserRegisterSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertEqual(len(serializer.errors), 1)
        self.assertEqual(serializer.errors['email'][0], 'user with this email already exists.')

    def test_empty_password2(self):
        data = {'username': 'kevin', 'email': 'kevin@gmail.com', 'password': 'asdF@123'}
        serializer = UserRegisterSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertEqual(len(serializer.errors), 1)
        self.assertEqual(serializer.errors['password2'][0], 'This field is required.')

    def test_empty_fields(self):
        serializer = UserRegisterSerializer(data={})
        self.assertFalse(serializer.is_valid())
        self.assertEqual(len(serializer.errors), 4)
