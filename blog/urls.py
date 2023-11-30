from django.urls import path, include
from blog import views
from .views import ArticleHome

urlpatterns = [
    path('', ArticleHome.as_view(), name='article_home'),
    path('delete/<int:article_id>/', views.ArticleDelete.as_view(), name='article_delete'),
    path('article/<int:article_id>/', views.ArticleDetail.as_view(), name="article_detail"),
    path('reaction/', include('reaction.urls')),
    path('addArticle/', views.ArticleAdd.as_view(), name="article_add")
]