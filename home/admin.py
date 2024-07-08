from django.contrib import admin

from .models import Question


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ('title', 'body', 'user', 'id', 'created')
    search_fields = ('user__username', 'user__email', 'title')
    raw_id_fields = ('user',)
    prepopulated_fields = {'slug': ('title',)}
