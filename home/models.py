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

    # TODO: add tags or categories.

    def __str__(self):
        return f'{self.owner.username} - {self.title[:30]}...'

    @property
    def short_title(self):
        return f'{self.title[:30]}...'

    @property
    def short_body(self):
        return f'{self.body[:30]}...'


class Answer(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='answers')
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='answers')
    body = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('-modified', '-created')

    def __str__(self):
        return f'{self.owner.username} - {self.body[:20]}... - {self.question.title[:30]}'

    @property
    def short_body(self):
        return f'{self.body[:30]}...'


class AnswerComment(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='answer_comments')
    answer = models.ForeignKey(Answer, on_delete=models.CASCADE, related_name='comments')
    body = models.TextField()
    reply = models.ForeignKey('self', on_delete=models.CASCADE, related_name='replies', blank=True, null=True)
    is_reply = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('-modified', '-created')

    def __str__(self):
        return f'{self.owner.username} - {self.answer.body[:20]}...'
