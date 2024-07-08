from django.db import models

from users.models import User


class Question(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='questions')
    title = models.CharField(max_length=500)
    body = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now_add=True)
    slug = models.SlugField(max_length=30, blank=True, null=True)

    # TODO: add and tags or categories.

    def __str__(self):
        return f'{self.user} - {self.title[:30]}...'


class Answer(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user')
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='question')
    body = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user} - {self.body[:20]}... - {self.question}'
