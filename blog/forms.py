# forms.py

from django import forms
from .models import Article


class ArticleForm(forms.ModelForm):
    class Meta:
        model = Article
        fields = ['title', 'content', 'author']


class ArticleSearchForm(forms.Form):
    search_term = forms.CharField(max_length=100, required=False, label='Search',
                                  widget=forms.TextInput(attrs={'placeholder': 'Search for a title or q content'}))
