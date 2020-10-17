from django.urls import path
from news.views import AllArticlesListView, AddArticle, ArticleDetailView, CategoryArticlesList, ArticleDeleteView, \
    UpdateArticleView, MostPopularArticlesListView, PromotedArticlesView, MostPopularPromotedArticlesView, \
    ArticlesIndexView

app_name = 'news'

urlpatterns = [

    path('add/', AddArticle.as_view(), name='add_article'),
    path('edit/<int:pk>/<slug:slug>', UpdateArticleView.as_view(), name='update_article'),
    path('delete/<int:pk>/<slug:slug>', ArticleDeleteView.as_view(), name='delete_article'),

    path('index/', ArticlesIndexView.as_view(), name='articles_index'),

    path('show/<int:pk>/<slug:slug>', ArticleDetailView.as_view(), name='article_detail'),

    path('category/<slug:slug>/', CategoryArticlesList.as_view(), name='category_articles_list'),
    path('all/', AllArticlesListView.as_view(), name='all_articles_list'),
    path('trending/', MostPopularArticlesListView.as_view(), name='trending'),

    path('promoted/', PromotedArticlesView.as_view(), name='promoted_articles'),
    path('hot/', MostPopularPromotedArticlesView.as_view(), name='hot_promoted_articles'),

]
