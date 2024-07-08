from django.db import models

from users.models import User


class Question(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='questions')
    title = models.CharField(max_length=500)
    body = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now_add=True)
    slug = models.SlugField(max_length=30, blank=True, null=True, unique=True)

    # TODO: add and tags or categories.

    def __str__(self):
        return f'{self.owner} - {self.title[:30]}...'


class Answer(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='answers')
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='answers')
    body = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.owner} - {self.body[:20]}... - {self.question}'
