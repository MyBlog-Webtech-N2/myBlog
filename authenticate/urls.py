from django.urls import path, include

from .views import *

urlpatterns = [
    path("", include("django.contrib.auth.urls")),
    path('signup/', InscriptionView.as_view(), name='signup'),
    path('profile/<int:user_id>/', ProfileView.as_view(), name='profile'),
]