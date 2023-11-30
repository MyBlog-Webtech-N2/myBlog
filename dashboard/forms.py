from django import forms

from blog.models import Article


class DashboardArticleForm(forms.ModelForm):
    class Meta:
        model = Article
        fields = ['title', 'content']

    title = forms.CharField(
        label='Name of article',
        max_length=100,
        widget=forms.TextInput(attrs={'class': 'tagInput', 'placeholder': 'Name of your article'}),
        required=True
    )
    content = forms.CharField(
        widget=forms.Textarea(
            attrs={'class': 'descriptionInput', 'placeholder': 'Make a constructive and simple content'}),
        required=True
    )
