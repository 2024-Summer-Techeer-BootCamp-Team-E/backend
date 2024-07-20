from rest_framework import serializers
from products.models import Product
from search.models import Search


class ProductSerializer(serializers.Serializer):
  product_name = serializers.CharField(max_length=255)
  category_id = serializers.IntegerField()
  price = serializers.FloatField()
  link = serializers.URLField()
  image_url = serializers.URLField()
  delivery_charge = serializers.FloatField(default=0)
  created_at = serializers.DateTimeField(required=False)
  updated_at = serializers.DateTimeField(required=False)
  is_deleted = serializers.BooleanField(default=False)

class AliPostRequestSerializer(serializers.Serializer):
  search_url = serializers.URLField()

class AliPostResponseSerializer(serializers.Serializer):
  id = serializers.IntegerField()
  name = serializers.CharField()
  category_id = serializers.IntegerField()
  price = serializers.IntegerField()
  delivery_charge = serializers.IntegerField()
  link = serializers.URLField()
  image_url = serializers.URLField()
  created_at = serializers.DateTimeField()
  updated_at = serializers.DateTimeField()
  is_deleted = serializers.BooleanField()
  search = serializers.IntegerField()


  def create(self, validated_data):
      return Product.objects.create(**validated_data)
