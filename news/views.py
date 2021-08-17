from django.http import Http404
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from django_filters.rest_framework import DjangoFilterBackend

from .models import NewsCategoryModel, NewsModel
from .serializers import NewsCategorySerializer, NewsSerializer


# Top 2 News List
class TopNewsList(APIView):
    def get(self, request):
        news = NewsModel.objects.order_by('-id')[:3]
        serializer = NewsSerializer(news, many=True)
        return Response(serializer.data)


# Most viewed 2 news list
class MostViewedList(APIView):
    def get(self, request):
        news = NewsModel.objects.order_by('-count_of_viewed')[:3]
        serializer = NewsSerializer(news, many=True)
        return Response(serializer.data)


# Filters
class Filter(DjangoFilterBackend):
    def filter_queryset(self, request, queryset, view):
        filter_class = self.get_filter_class(view, queryset)
        if filter_class:
            return filter_class(request.query_params, queryset=queryset, request=request).qs
        return queryset


# News CRUD
class NewsCategoryList(APIView):
    filter_fields = ('name', 'id')
    search_fields = ('name',)
    ordering_fields = ('name', 'id')

    def get(self, request):
        queryset = NewsCategoryModel.objects.all()
        filter = Filter()
        filtered_queryset = filter.filter_queryset(request, queryset, self)
        serializer = NewsCategorySerializer(filtered_queryset, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = NewsCategorySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class NewsCategoryDetail(APIView):
    def get_object(self, pk):
        try:
            return NewsCategoryModel.objects.get(pk=pk)
        except NewsCategoryModel.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        category = self.get_object(pk)
        serializer = NewsCategorySerializer(category)
        return Response(serializer.data)

    def put(self, request, pk):
        category = self.get_object(pk)
        serializer = NewsCategorySerializer(category, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        category = self.get_object(pk)
        category.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class NewsList(APIView):
    filter_fields = ('title', 'news_category')
    search_fields = ('title', 'content')
    ordering_fields = ('id', 'created_date', 'count_of_viewed')

    def get(self, request):
        queryset = NewsModel.objects.all()
        filter = Filter()
        filtered_queryset = filter.filter_queryset(request, queryset, self)
        serializer = NewsSerializer(filtered_queryset, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = NewsSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class NewsDetail(APIView):
    def get_object(self, pk):
        try:
            return NewsModel.objects.get(pk=pk)
        except NewsModel.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        news = self.get_object(pk)
        news.count_of_viewed += 1
        news.save()
        serilizer = NewsSerializer(news)
        return Response(serilizer.data)

    def put(self, request, pk):
        news = self.get_object(pk)
        serializer = NewsSerializer(news, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        news = self.get_object(pk)
        news.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

