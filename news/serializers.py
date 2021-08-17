from rest_framework import serializers
from .models import NewsCategoryModel, NewsModel

class NewsCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = NewsCategoryModel
        fields = '__all__'

class NewsSerializer(serializers.ModelSerializer):
    class Meta:
        model = NewsModel
        fields = '__all__'