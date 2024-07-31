from urllib.parse import urlencode

from django.contrib.auth.models import AnonymousUser
from django.urls import reverse
from model_bakery import baker
from rest_framework.test import APIRequestFactory
from rest_framework.test import APITestCase
from rest_framework_simplejwt.tokens import AccessToken

from home import models
from home.views import *
from users.models import User


class TestHomeAPI(APITestCase):
    @classmethod
    def setUpTestData(cls):
        tag = baker.make(models.Tag, name='test_tag')
        baker.make(models.Question, body='test body')
        baker.make(models.Question, body='test body test_search')
        baker.make(models.Question, body='test_tag body', tag=[tag])

    def test_home_GET(self):
        response = self.client.get(reverse('home:home'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data['data']), 3)
        self.assertEqual(response.data['data'][2]['id'], 1)
        self.assertEqual(response.data['data'][2]['body'], 'test body')

    def test_home_filter_tag_GET(self):
        url = f"{reverse('home:home')}?{urlencode({'tag': 'test_tag'})}"
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data['data']), 1)
        self.assertEqual(response.data['data'][0]['tag'], ['test_tag'])

    def test_home_filter_invalid_tag_GET(self):
        url = f"{reverse('home:home')}?{urlencode({'tag': ['invalid_tag']})}"
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)
        self.assertEqual(len(response.data), 1)

    def test_home_search_GET(self):
        url = f"{reverse('home:home')}?{urlencode({'search': 'search'})}"
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data['data']), 1)
        self.assertEqual(response.data['data'][0]['body'], 'test body test_search')

    def test_home_search_GET_404(self):
        url = f"{reverse('home:home')}?{urlencode({'search': 'username'})}"
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data['error'], 'question not found.')


class TestQuestionViewSet(APITestCase):
    def setUp(self):
        self.factory = APIRequestFactory()
        self.user = baker.make(User, is_active=True)
        self.tag = baker.make(models.Tag, name='test_tag')
        baker.make(models.Question, 33, owner=self.user)
        self.token = self.get_JWT_token()

    def get_JWT_token(self):
        token = AccessToken.for_user(self.user)
        return str(token)

    def test_permissions_allowed(self):
        request = self.factory.get(reverse('home:question-detail', args=[2]))
        request.user = AnonymousUser()
        response = QuestionViewSet.as_view({'get': 'retrieve'})(request, pk=2)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 2)

    def test_permissions_denied(self):
        request = self.factory.post(reverse('home:question-list'))
        request.user = AnonymousUser()
        response = QuestionViewSet.as_view({'get': 'create'})(request)
        self.assertEqual(response.status_code, 405)

    def test_question_list(self):
        request = self.factory.get(reverse('home:question-list'))
        request.user = AnonymousUser()
        response = QuestionViewSet.as_view({'get': 'list'})(request)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data['results']), 20)

    def test_question_list_pagination(self):
        url = f"{reverse('home:question-list')}?{urlencode({'page': 2})}"
        request = self.factory.get(url)
        request.user = AnonymousUser()
        response = QuestionViewSet.as_view({'get': 'list'})(request)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data['results']), 13)

    def test_question_create(self):
        data = {
            'tag': self.tag,
            'owner': self.user,
            'title': 'test_title',
            'body': 'test_body',
        }
        request = self.factory.post(reverse('home:question-list'), data=data, HTTP_AUTHORIZATION='Bearer ' + self.token)
        response = QuestionViewSet.as_view({'post': 'create'})(request)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['message'], 'question created successfully!')

    def test_question_partial_update(self):
        data = {
            'title': 'update test',
        }
        request = self.factory.patch(reverse('home:question-detail', args=[2]), data=data,
                                     HTTP_AUTHORIZATION='Bearer ' + self.token)
        response = QuestionViewSet.as_view({'patch': 'partial_update'})(request, pk=2)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['title'], 'update test')

    def test_question_full_update(self):
        data = {
            'title': 'update test',
            'body': 'update testing body'
        }
        request = self.factory.put(reverse('home:question-detail', args=[2]), data=data,
                                   HTTP_AUTHORIZATION='Bearer ' + self.token)
        response = QuestionViewSet.as_view({'put': 'update'})(request, pk=2)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['title'], 'update test')
        self.assertEqual(response.data['body'], 'update testing body')

    def test_question_delete(self):
        request = self.factory.delete(reverse('home:question-detail', args=[2]),
                                      HTTP_AUTHORIZATION='Bearer ' + self.token)
        response = QuestionViewSet.as_view({'delete': 'destroy'})(request, pk=2)
        self.assertEqual(response.status_code, 204)
