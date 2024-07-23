from rest_framework import serializers
from .models import Search
class SearchSerializer(serializers.ModelSerializer):
  class Meta:
    model = Search
    fields = '__all__'
    
class KeywordsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Search
        fields = ['search_url', 'name', 'keyword', 'category_id']

class KeywordRequestSerializer(serializers.Serializer):
    search_url = serializers.CharField(required=True)

class KeywordResponseSerializer(serializers.Serializer):
    keyword = serializers.CharField()
    category_id = serializers.IntegerField()
