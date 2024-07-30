from model_bakery import baker
from rest_framework.test import APITestCase

from users.models import User
from users.serializers import UserSerializer


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
