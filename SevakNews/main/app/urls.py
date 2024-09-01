from django.urls import path
from . import views
from django.views.decorators.cache import cache_page


urlpatterns = [
    path('', views.HomeNews.as_view(), name='home'),
    # path('', cache_page(300)(views.HomeNews.as_view()), name='home'),
    path('search-task/', views.SearchTask.as_view(), name='search-task'),
    path('category/<str:title>', views.CategoryNews.as_view(), name='category'),
    # path('category/<str:title>', cache_page(300)(views.CategoryNews.as_view()), name='category'),
    path('news/<int:news_id>', views.NewsContent, name='news-content'),
    # path('news/<int:news_id>', cache_page(300)(views.NewsContent), name='news-content'),
    path('add_news/', views.CreateNewsView.as_view(), name='add_news'),
]
