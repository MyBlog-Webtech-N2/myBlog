from django.urls import path, include

from .views import InscriptionView

urlpatterns = [
    path("", include("django.contrib.auth.urls")),
    path('signup/', InscriptionView.as_view(), name='signup')
]