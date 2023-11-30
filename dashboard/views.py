from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.views import View

from blog.models import Article
from .forms import DashboardArticleForm
from reaction.models import Comment


class DashboardView(LoginRequiredMixin, View):
    def get(self, request):
        articles = Article.objects.filter(author=self.request.user.pk)
        return render(request, 'dashboard/home.html', {'articles': articles})


class DashboardArticleView(LoginRequiredMixin, View):
    def get(self, request, article_id):
        article = get_object_or_404(Article, pk=article_id)
        if article.author_id != self.request.user.id:
            return redirect('dashboard')
        form = DashboardArticleForm()
        return render(request, 'dashboard/article.html', {'form': form, 'article': article})

    def post(self, request, *args, **kwargs):
        article = get_object_or_404(Article, pk=request.POST.get('article'))
        if article.author_id != self.request.user.id:
            return redirect('dashboard')
        form = DashboardArticleForm(request.POST, instance=article)
        if form.is_valid():
            form.save()
            return JsonResponse({'message': 'Article modifier avec succès'}, status=200)
        else:
            return JsonResponse({'error': 'Merci de remplir tous les champs'}, status=400)

    def delete(self, request, *args, **kwargs):
        try:
            article_id = request.GET.get('id')
            article = get_object_or_404(Article, pk=article_id)
            if article.author_id == self.request.user.pk:
                article.delete()
                return JsonResponse({'message': 'Article supprimer avec succès'})
            else:
                return JsonResponse({'error': 'Cette article ne vous appartiens pas.'}, status=400)
        except KeyError:
            return JsonResponse({'error': 'Cette article ne vous appartiens pas.'}, status=400)


class DashboardArticleReactionView(LoginRequiredMixin, View):
    def get(self, request, article_id):
        article = get_object_or_404(Article, pk=article_id)
        if article.author_id != self.request.user.id:
            return redirect('dashboard')
        comments = Comment.objects.filter(article_id=article_id)

        return render(request, 'dashboard/reactions.html',
                      {'comments': comments})

    def delete(self, request, *args, **kwargs):
        try:
            comment_id = request.GET.get('id')
            comment = get_object_or_404(Comment, pk=comment_id)
            if comment.article.author_id == self.request.user.pk:
                comment.delete()
                return JsonResponse({'message': 'Commentaire supprimer avec succès'})
            else:
                return JsonResponse({'error': 'Cette article ne vous appartiens pas.'}, status=400)
        except KeyError:
            return JsonResponse({'error': 'Cette article ne vous appartiens pas.'}, status=400)
