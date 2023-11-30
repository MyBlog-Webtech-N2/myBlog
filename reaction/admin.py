from django.contrib import admin

from .models import Comment


# Register your models here.

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('article', 'author', 'star', 'created_at')
    list_filter = ('article', 'author')