from django.contrib.auth import login
from django.shortcuts import render, redirect
from django.views import View
from django.shortcuts import render, get_object_or_404

from blog.models import Article
from .forms import CustomUserCreationForm
from .models import CustomUser


# Create your views here.

class ProfileView(View):
    def get(self, request, user_id):
        user = get_object_or_404(CustomUser, pk=user_id)
        articles = Article.objects.filter(author=user)
        return render(request, 'profile.html', {'profile': user, 'articles': articles})


class InscriptionView(View):

    def get(self, request):
        if self.request.user.is_authenticated:
            return redirect('article_home')
        form = CustomUserCreationForm()
        return render(request, 'registration/inscription.html', {'form': form})

    def post(self, request):
        if self.request.user.is_authenticated:
            return redirect('article_home')
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('article_home')
        return render(request, 'registration/inscription.html', {'form': form})