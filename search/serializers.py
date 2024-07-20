from rest_framework import serializers
from search.models import Search

class SearchSerializer(serializers.ModelSerializer):
  class Meta:
    model = Search
    fields = '__all__'