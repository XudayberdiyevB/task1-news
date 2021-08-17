from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework.urlpatterns import format_suffix_patterns
from .views import NewsCategoryList, NewsCategoryDetail, NewsList, NewsDetail, TopNewsList, MostViewedList

router = DefaultRouter()
urlpatterns = [
    path('', include(router.urls)),
    path('categories/', NewsCategoryList.as_view(), name="categories"),
    path('categories/<int:pk>', NewsCategoryDetail.as_view(), name="category_detail"),
    path('news/', NewsList.as_view(), name="news"),
    path('news/<int:pk>', NewsDetail.as_view(), name="news_detail"),
    path('news/top/', TopNewsList.as_view()),
    path('news/most-viewed/', MostViewedList.as_view()),
]