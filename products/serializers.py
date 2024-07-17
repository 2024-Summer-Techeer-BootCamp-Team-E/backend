from rest_framework import serializers
from products.models import Product

class ProductSerializer(serializers.ModelSerializer):
  class Meta:
    model = Product
    fields = '__all__'

class AliPostRequestSerializer(serializers.Serializer):
  category_id = serializers.IntegerField()
  keyword = serializers.CharField()
  search_url = serializers.URLField()
  search_name = serializers.CharField()
  search_price = serializers.DecimalField(max_digits=10, decimal_places=2)
  page_num = serializers.CharField()

class AliPostResponseSerializer(serializers.Serializer):
  id = serializers.IntegerField()
  product_name = serializers.CharField()
  category_id = serializers.IntegerField()
  price = serializers.DecimalField(max_digits=10, decimal_places=2)
  delivery_charge = serializers.DecimalField(max_digits=10, decimal_places=2)
  link = serializers.URLField()
  image_url = serializers.URLField()
  created_at = serializers.DateTimeField()
  updated_at = serializers.DateTimeField()
  is_deleted = serializers.BooleanField()
  search = serializers.IntegerField()


