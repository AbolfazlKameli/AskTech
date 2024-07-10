from django.db import models

from users.models import User


class Question(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='questions')
    title = models.CharField(max_length=500)
    body = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    slug = models.SlugField(max_length=50)

    class Meta:
        ordering = ('-modified', '-created')

    # TODO: add answer comments and tags or categories.

    def __str__(self):
        return f'{self.owner} - {self.title[:30]}...'


class Answer(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='answers')
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='answers')
    body = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('-modified', '-created')

    def __str__(self):
        return f'{self.owner} - {self.body[:20]}... - {self.question.title}'
