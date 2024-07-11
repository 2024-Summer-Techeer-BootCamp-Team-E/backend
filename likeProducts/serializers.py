from rest_framework import serializers
from .models import LikeProduct
from products.serializers import ProductSerializer

class LikeProductSerializer(serializers.ModelSerializer):
    product_details = ProductSerializer(source='product', read_only=True)  # product 필드의 상세정보 직렬화

    class Meta:
        model = LikeProduct
        fields = ['id', 'user', 'product', 'product_number', 'created_at', 'updated_at', 'is_deleted', 'product_details']

class ProductDetailsSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    product_name = serializers.CharField(max_length=100)
    category_id = serializers.IntegerField()
    price = serializers.DecimalField(max_digits=10, decimal_places=2)
    delivery_charge = serializers.DecimalField(max_digits=10, decimal_places=2)  # 배송비
    currency_id = serializers.IntegerField()  # 화폐 단위
    link = serializers.URLField()
    image_url = serializers.URLField()
    created_at = serializers.DateTimeField()
    updated_at = serializers.DateTimeField()
    is_deleted = serializers.BooleanField()

class GetRequestSerializer(serializers.Serializer):
    pass

class GetResponseSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    user = serializers.IntegerField()
    product = serializers.IntegerField()
    product_number = serializers.IntegerField()
    created_at = serializers.DateTimeField()
    updated_at = serializers.DateTimeField()
    is_deleted = serializers.BooleanField()
    product_details = ProductDetailsSerializer(many=False)

class PostRequestSerializer(serializers.Serializer):
    product = serializers.CharField()

class PostResponseSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    user = serializers.IntegerField()
    product = serializers.IntegerField()
    product_number = serializers.IntegerField()
    created_at = serializers.DateTimeField()
    updated_at = serializers.DateTimeField()
    is_deleted = serializers.BooleanField()
    product_details = ProductDetailsSerializer(many=False)

class DeleteRequestSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    product = serializers.IntegerField()
