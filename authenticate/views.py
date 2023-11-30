from django.contrib.auth import login
from django.shortcuts import render, redirect
from django.views import View

from .forms import CustomUserCreationForm


# Create your views here.
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
        print(form.is_valid())
        if form.is_valid():
            utilisateur = form.save()
            login(request, utilisateur)
            return redirect('article_home')
        return render(request, 'registration/inscription.html', {'form': form})
