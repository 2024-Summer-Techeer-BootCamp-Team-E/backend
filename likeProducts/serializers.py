from rest_framework import serializers
from .models import LikeProduct
from products.serializers import ProductSerializer

class LikeProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = LikeProduct
        fields = '__all__'

class GetRequestSerializer(serializers.Serializer):
    pass

class GetResponseSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    name = serializers.CharField()
    price = serializers.DecimalField(max_digits=10, decimal_places=2)
    delivery_charge = serializers.DecimalField(max_digits=10, decimal_places=2)
    link = serializers.URLField()
    image_url = serializers.URLField()
    category_id = serializers.IntegerField()
    created_at = serializers.DateTimeField()
    updated_at = serializers.DateTimeField()
    is_deleted = serializers.BooleanField()
    user = serializers.IntegerField()

class PostRequestSerializer(serializers.Serializer):
    name = serializers.CharField()
    price = serializers.DecimalField(max_digits=10, decimal_places=2)
    delivery_charge = serializers.DecimalField(max_digits=10, decimal_places=2)
    link = serializers.URLField()
    image_url = serializers.URLField()
    category_id = serializers.IntegerField()

class PostResponseSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    name = serializers.CharField()
    price = serializers.DecimalField(max_digits=10, decimal_places=2)
    delivery_charge = serializers.DecimalField(max_digits=10, decimal_places=2)
    link = serializers.URLField()
    image_url = serializers.URLField()
    category_id = serializers.IntegerField()
    created_at = serializers.DateTimeField()
    updated_at = serializers.DateTimeField()
    is_deleted = serializers.BooleanField()
    user = serializers.IntegerField()

class DeleteRequestSerializer(serializers.Serializer):
    id = serializers.IntegerField()
