from django.db import models

from users.models import User


class Question(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='questions')
    title = models.CharField(max_length=500)
    body = models.CharField(max_length=10000)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now_add=True)

    # TODO: add answers and tags or categories.

    def __str__(self):
        return f'{self.user} - {self.title[:30]}...'
