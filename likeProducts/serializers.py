from rest_framework import serializers
from .models import LikeProduct
from products.serializers import ProductSerializer

class LikeProductSerializer(serializers.ModelSerializer):
    product_details = ProductSerializer(source='product', read_only=True)  # product 필드의 상세정보 직렬화

    class Meta:
        model = LikeProduct
        fields = ['id', 'user', 'product', 'product_number', 'created_at', 'updated_at', 'is_deleted', 'product_details']
