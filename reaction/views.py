from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404
from django.views import View

from .forms import CommentForm
from blog.models import Article, CustomUser


class ArticleReaction(LoginRequiredMixin, View):
    def get(self, request, article_id):
        article = get_object_or_404(Article, pk=article_id)
        reactions = [
            {'id': 5, 'img': "very-cool.png", 'name': 'Very Cool'},
            {'id': 4, 'img': "cool.png", 'name': 'Cool'},
            {'id': 3, 'img': "good.png", 'name': 'Good'},
            {'id': 2, 'img': "not-bad.png", 'name': 'Not Bad'},
            {'id': 1, 'img': "bad.png", 'name': 'Bad'},
        ]
        return render(request, 'article/article_add_reaction.html', {'article': article, 'reactions': reactions})

    def post(self, request, *args, **kwargs):
        article_id = request.POST.get('article')
        article = get_object_or_404(Article, pk=article_id)
        author = get_object_or_404(CustomUser, pk=self.request.user.pk)

        form = CommentForm(request.POST, initial={'article': article, 'author': author})

        if form.is_valid():
            comment = form.save(commit=False)
            comment.author = author
            comment.article = article
            comment.save()
            return JsonResponse({'message': 'Réaction ajoutée avec succès'})
        return JsonResponse({'error': 'Certains champs sont manquants'}, status=400)
