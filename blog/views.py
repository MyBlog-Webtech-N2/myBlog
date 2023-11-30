from django.db.models import Q
from django.views import View
from django.shortcuts import render, get_object_or_404

from reaction.models import Comment
from .forms import ArticleForm, ArticleSearchForm
from .models import Article, CustomUser
from django.http import JsonResponse
from django.contrib.auth.mixins import LoginRequiredMixin


class ArticleHome(View):

    def get(self, request):
        form = ArticleSearchForm()
        return render(request, 'home.html', {'form': form, 'posts': Article.objects.filter(active=True)})

    def post(self, request):
        form = ArticleSearchForm(request.POST)
        if form.is_valid():
            search_term = form.cleaned_data['search_term']
            articles = Article.objects.filter(Q(title__icontains=search_term) | Q(content__icontains=search_term))
            return render(request, 'home.html', {'form': form, 'posts': articles})

    def delete(self, request, *args, **kwargs):
        try:
            article_id = request.GET.get('id')
            article = get_object_or_404(Article, pk=article_id)
            if article and article.author_id == self.request.user.pk:
                article.delete()
                return JsonResponse({'message': 'Article supprimer avec succès'})
            else:
                return JsonResponse({'error': 'Cette article ne vous appartiens pas.'}, status=400)
        except KeyError:
            return JsonResponse({'error': 'Cette article ne vous appartiens pas.'}, status=400)


class ArticleAdd(LoginRequiredMixin, View):
    def get(self, request):
        return render(request, "article/add_article.html")

    def post(self, request, *args, **kwargs):
        author = get_object_or_404(CustomUser, pk=self.request.user.pk)
        form = ArticleForm(request.POST, initial={'author': author})
        if form.is_valid():
            article = form.save(commit=False)
            article.author = author
            article.save()
            return JsonResponse({'message': 'Article ajoutée avec succès'})
        return JsonResponse({'error': 'Certains champs sont manquants'}, status=400)


class ArticleDetail(View):
    def get(self, request, article_id):
        article = get_object_or_404(Article, pk=article_id)
        return render(request, 'article/article_detail.html', {'article': article})

    def delete(self, request, *args, **kwargs):
        try:
            comment_id = request.GET.get('id')
            comment = get_object_or_404(Comment, pk=comment_id)
            if comment and comment.author_id == self.request.user.pk:
                comment.delete()
                return JsonResponse({'message': 'Commentaire supprimer avec succès'})
            else:
                return JsonResponse({'error': 'Ce commentaire ne vous appartiens pas.'}, status=400)
        except KeyError:
            return JsonResponse({'error': 'Ce commentaire ne vous appartiens pas.'}, status=400)


class ArticleDelete(LoginRequiredMixin, View):
    def post(self, request, article_id):
        try:
            article = get_object_or_404(Article, pk=article_id)
            if article and article.author_id == self.request.user.pk:
                article.delete()
                response_data = {'message': 'Article supprimer avec succès'}
                return JsonResponse(response_data)
            else:
                return JsonResponse({'error': 'Cette article ne vous appartiens pas.'}, status=400)
        except KeyError:
            return JsonResponse({'error': 'Cette article ne vous appartiens pas.'}, status=400)
