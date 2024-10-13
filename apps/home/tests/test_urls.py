from django.urls import reverse, resolve
from rest_framework.test import APISimpleTestCase

from apps.home import views


class TestUrls(APISimpleTestCase):
    def test_home_url(self):
        home_url = reverse('home:home')
        self.assertEqual(resolve(home_url).func.view_class, views.HomeAPI)

    # Answers
    def test_answer_like_url(self):
        answer_like_url = reverse('home:answer-like', args=(20,))
        self.assertEqual(resolve(answer_like_url).func.view_class, views.LikeAPI)

    def test_answer_dislike_url(self):
        answer_dislike_url = reverse('home:answer-dislike', args=(20,))
        self.assertEqual(resolve(answer_dislike_url).func.view_class, views.DisLikeAPI)

    def test_accept_answer_url(self):
        accept_answer_url = reverse('home:answer-accept', args=(20,))
        self.assertEqual(resolve(accept_answer_url).func.view_class, views.AcceptAnswerAPI)

    def test_answer_create_url(self):
        answer_crete_url = reverse('home:answer-create', args=(20,))
        self.assertEqual(resolve(answer_crete_url).func.view_class, views.CreateAnswerAPI)

    def test_comment_create_url(self):
        comment_create_url = reverse('home:comment-create', args=(20,))
        self.assertEqual(resolve(comment_create_url).func.view_class, views.CreateCommentAPI)

    def test_reply_create_url(self):
        reply_create_url = reverse('home:reply-create', args=(20,))
        self.assertEqual(resolve(reply_create_url).func.view_class, views.CreateReplyAPI)
