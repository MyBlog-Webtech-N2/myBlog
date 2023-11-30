from django.urls import path

from reaction.views import ArticleReaction

urlpatterns = [
    path('<int:article_id>/', ArticleReaction.as_view(),name="article_reaction"),
]