from django.contrib import admin

from . import models


class AnswerInline(admin.StackedInline):
    model = models.Answer
    raw_id_fields = ('owner', 'question')


class AnswerCommentsInline(admin.StackedInline):
    model = models.AnswerComment
    raw_id_fields = ('owner', 'answer', 'reply')


@admin.register(models.Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ('short_title', 'short_body', 'owner', 'id', 'created')
    search_fields = ('owner__username', 'owner__email', 'title')
    raw_id_fields = ('owner',)
    prepopulated_fields = {'slug': ('title',)}
    inlines = (AnswerInline,)


@admin.register(models.Answer)
class AnswerAdmin(admin.ModelAdmin):
    list_display = ('owner', 'short_body', 'question')
    search_fields = ('owner__username', 'owner__email', 'body')
    raw_id_fields = ('question', 'owner')
    inlines = (AnswerCommentsInline,)


@admin.register(models.AnswerComment)
class AnswerCommentAdmin(admin.ModelAdmin):
    list_display = ('owner', 'answer', 'is_reply')
    raw_id_fields = ('owner', 'answer', 'reply')
    search_fields = ('owner__username', 'owner__email', 'body', 'reply__body')
