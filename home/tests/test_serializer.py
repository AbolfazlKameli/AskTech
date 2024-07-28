from rest_framework.test import APITestCase

from home.models import Tag
from home.serializers import QuestionSerializer
from users.models import User


class TestQuestionSerializer(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='username', email='email@gmail.com', password='password')
        self.tag = Tag.objects.create(name='tag')

    def test_valid_data(self):
        data = {'tag': [self.tag], 'owner': self.user, 'title': 'test_title', 'body': 'test_body'}
        serializer = QuestionSerializer(data=data)
        self.assertTrue(serializer.is_valid())

    def test_missing_tag(self):
        data = {'owner': self.user, 'title': 'test_title', 'body': 'test_body'}
        serializer = QuestionSerializer(data=data)
        self.assertTrue(serializer.is_valid())

    def test_missing_fields(self):
        data = {'owner': self.user, 'body': 'test_body'}
        serializer = QuestionSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertEqual(len(serializer.errors), 1)

    def test_invalid_tag(self):
        data = {'tag': ['test', 'test2'], 'owner': self.user, 'title': 'test_title', 'body': 'test_body'}
        serializer = QuestionSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertEqual(len(serializer.errors), 1)

    def test_empty_fields(self):
        serializer = QuestionSerializer(data={})
        self.assertFalse(serializer.is_valid())
        self.assertEqual(len(serializer.errors), 2)
