from django.test import TestCase
from django.urls import reverse, resolve

from home import views


class TestUrls(TestCase):
    def setUp(self):
        # Landing Page
        self.home_url = reverse('home:home')
        # Answers
        self.answer_like_url = reverse('home:answer_like', args=(20,))
        self.answer_dislike_url = reverse('home:answer_dislike', args=(20,))
        self.accept_answer_url = reverse('home:answer_accept', args=(20,))

    def test_home_url(self):
        self.assertEqual(resolve(self.home_url).func.view_class, views.HomeAPI)

    def test_answer_like_url(self):
        self.assertEqual(resolve(self.answer_like_url).func.view_class, views.LikeAPI)

    def test_answer_dislike_url(self):
        self.assertEqual(resolve(self.answer_dislike_url).func.view_class, views.DisLikeAPI)

    def test_accept_answer_url(self):
        self.assertEqual(resolve(self.accept_answer_url).func.view_class, views.AcceptAnswerAPI)
