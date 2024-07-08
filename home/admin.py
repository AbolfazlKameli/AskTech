from django.contrib import admin

from .models import Question, Answer


class AnswerInline(admin.StackedInline):
    model = Answer
    raw_id_fields = ('user', 'question')


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ('title', 'body', 'user', 'id', 'created')
    search_fields = ('user__username', 'user__email', 'title')
    raw_id_fields = ('user',)
    prepopulated_fields = {'slug': ('title',)}
    inlines = (AnswerInline,)


@admin.register(Answer)
class AnswerAdmin(admin.ModelAdmin):
    list_display = ('user', 'body', 'question')
    search_fields = ('user__username', 'user__email', 'body')
    raw_id_fields = ('question', 'user')
