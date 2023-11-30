from django.urls import path

from .views import *

urlpatterns = [
    path('', DashboardView.as_view(), name='dashboard'),
    path('article/<int:article_id>/', DashboardArticleView.as_view(), name='dashboard_article'),
    path('article/<int:article_id>/reactions', DashboardArticleReactionView.as_view(), name='dashboard_article_reaction'),
]