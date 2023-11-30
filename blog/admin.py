from django.contrib import admin
from django import forms

from reaction.models import Comment
from .models import *


class ArticleAdminForm(forms.ModelForm):
    content = forms.CharField(widget=forms.Textarea(attrs={'rows': 20, 'cols': 80}))

    class Meta:
        model = Article
        fields = '__all__'


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    form = ArticleAdminForm
    list_display = ('title', 'author', 'date', 'active')
    list_filter = ('author', 'active')
    search_fields = ('title',)