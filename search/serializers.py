from rest_framework import serializers
from .models import Search
from ..products.models import Product
from products.serializers import ProductSerializer

class KeywordsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ('product_name')


class TranslateRequestSerializer(serializers.Serializer):
    product_name = serializers.CharField()

class TranslateResponseSerializer(serializers.Serializer):
    product_name = serializers.CharField()