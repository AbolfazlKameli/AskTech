from django.contrib import admin

from .models import Question, Answer


class AnswerInline(admin.StackedInline):
    model = Answer
    raw_id_fields = ('owner', 'question')


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ('title', 'body', 'owner', 'id', 'created')
    search_fields = ('owner__username', 'owner__email', 'title')
    raw_id_fields = ('owner',)
    prepopulated_fields = {'slug': ('title',)}
    inlines = (AnswerInline,)


@admin.register(Answer)
class AnswerAdmin(admin.ModelAdmin):
    list_display = ('owner', 'body', 'question')
    search_fields = ('owner__username', 'owner__email', 'body')
    raw_id_fields = ('question', 'owner')
