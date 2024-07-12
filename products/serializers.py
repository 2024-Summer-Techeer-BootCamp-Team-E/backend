from rest_framework import serializers
from products.models import Product

class ProductSerializer(serializers.ModelSerializer):
  class Meta:
    model = Product
    fields = '__all__'

    def search(self, data):
      category_id = data.get('category_id')
      keyword = data.get('keyword')


