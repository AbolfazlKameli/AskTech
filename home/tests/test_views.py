from rest_framework.test import APITestCase, APIRequestFactory
from users.models import User
from home import views
from home import serializers
from django.urls import reverse
from model_bakery import baker
from django.contrib.auth.models import AnonymousUser
from home import models


class TestHomeAPI(APITestCase):
    @classmethod
    def setUpTestData(cls):
        baker.make(models.Question, body='test body')

    def test_home_GET(self):
        response = self.client.get(reverse('home:home'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['data'][0]['id'], 1)
        self.assertEqual(response.data['data'][0]['body'], 'test body')
