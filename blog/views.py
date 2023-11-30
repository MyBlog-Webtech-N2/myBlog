from django.views import View
from django.shortcuts import render, get_object_or_404

from reaction.models import Comment
from .models import Article, CustomUser
from django.http import JsonResponse
from django.contrib.auth.mixins import LoginRequiredMixin


class Home(View):
    def get(self, request):
        return render(request, 'home.html', {'posts': Article.objects.filter(active=True)})


class ArticleAdd(LoginRequiredMixin, View):
    def get(self, request):
        return render(request, "add_article.html")

    def post(self, request, *args, **kwargs):
        try:
            title = request.POST.get('title')
            content = request.POST.get('content')
            author = get_object_or_404(CustomUser, pk=self.request.user.pk)

            new_article = Article(title=title, content=content, author=author)
            new_article.save()

            response_data = {'message': 'Article ajoutée avec succès'}
            return JsonResponse(response_data)

        except KeyError:
            return JsonResponse({'error': 'Certains champs sont manquants'}, status=400)


class ArticleDetail(View):
    def get(self, request, article_id):
        article = get_object_or_404(Article, pk=article_id)
        return render(request, 'article_detail.html', {'article': article})

    def post(self, request, *args, **kwargs):
        try:
            comment_id = request.POST.get('comment_id')
            comment = get_object_or_404(Comment, pk=comment_id)
            if comment and comment.author_id == self.request.user.pk:
                comment.delete()
                response_data = {'message': 'Commentaire supprimer avec succès'}
                return JsonResponse(response_data)
            else:
                return JsonResponse({'error': 'Ce commentaire ne vous appartiens pas.'}, status=400)
        except KeyError:
            return JsonResponse({'error': 'Ce commentaire ne vous appartiens pas.'}, status=400)
