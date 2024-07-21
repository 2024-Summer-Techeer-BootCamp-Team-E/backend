from rest_framework import serializers
from .models import Search
from ..products.models import Product
from products.serializers import ProductSerializer

class KeywordsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ('product_name')


class KeywordRequestSerializer(serializers.Serializer):
    product_name = serializers.CharField()

class KeywordResponseSerializer(serializers.Serializer):
    product_name = serializers.CharField()