from model_bakery import baker
from rest_framework.test import APITestCase

from home.models import Tag, Question, AnswerComment, Answer
from home.serializers import QuestionSerializer, AnswerSerializer
from users.models import User


class TestQuestionSerializer(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='username', email='email@gmail.com', password='password')
        self.tag = baker.make(Tag)

    def test_valid_data(self):
        data = {'tag': [self.tag], 'owner': self.user, 'title': 'test_title', 'body': 'test_body'}
        serializer = QuestionSerializer(data=data)
        self.assertTrue(serializer.is_valid())
        self.assertEqual(len(serializer.validated_data), 3)
        self.assertEqual(serializer.validated_data['tag'], [self.tag])
        self.assertEqual(serializer.validated_data['body'], 'test_body')

    def test_missing_tag(self):
        data = {'owner': self.user, 'title': 'test_title', 'body': 'test_body'}
        serializer = QuestionSerializer(data=data)
        self.assertTrue(serializer.is_valid())
        with self.assertRaises(KeyError):
            return serializer.validated_data['tag']

    def test_missing_fields(self):
        data = {'owner': self.user, 'body': 'test_body'}
        serializer = QuestionSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertEqual(serializer.errors['title'][0], 'This field is required.')
        self.assertEqual(len(serializer.errors), 1)

    def test_invalid_tag(self):
        data = {'tag': ['test', 'test2'], 'owner': self.user, 'title': 'test_title', 'body': 'test_body'}
        serializer = QuestionSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertEqual(len(serializer.errors), 1)
        self.assertEqual(serializer.errors['tag'][0], 'Object with name=test does not exist.')

    def test_empty_fields(self):
        serializer = QuestionSerializer(data={})
        self.assertFalse(serializer.is_valid())
        self.assertEqual(len(serializer.errors), 2)


class TestAnswerSerializer(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='username', email='email@gmail.com', password='password')
        self.question = baker.make(Question, title='test_question')

    def test_valid_data(self):
        data = {'owner': self.user, 'question': self.question, 'body': 'test_answer'}
        serializer = AnswerSerializer(data=data)
        self.assertTrue(serializer.is_valid())
        self.assertEqual(serializer.validated_data['body'], 'test_answer')

    def test_empty_fields(self):
        serializer = AnswerSerializer(data={})
        self.assertFalse(serializer.is_valid())
        self.assertEqual(len(serializer.errors), 1)
        self.assertEqual(len(serializer.validated_data), 0)

    def test_get_comments(self):
        answer = baker.make(Answer)
        baker.make(AnswerComment, body='first comment', answer=answer)
        baker.make(AnswerComment, body='second comment', answer=answer)
        serializer = AnswerSerializer(instance=answer)
        data = serializer.data['comments']
        self.assertEqual(len(data), 2)
        self.assertEqual(data[0]['body'], 'second comment')
        self.assertEqual(data[1]['body'], 'first comment')
