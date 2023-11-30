from django.urls import path, include
from blog import views
from .views import Home

urlpatterns = [
    path('', Home.as_view(), name='blog_home'),
    path('article/<int:article_id>/', views.ArticleDetail.as_view(), name="article_detail"),
    path('reaction/', include('reaction.urls')),
    path('addArticle/', views.ArticleAdd.as_view(), name="article_add")
]