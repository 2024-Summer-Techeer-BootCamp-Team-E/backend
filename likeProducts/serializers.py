from rest_framework import serializers
from .models import LikeProduct
from products.serializers import ProductSerializer

class LikeProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = LikeProduct
        fields = '__all__'

class LikeGetRequestSerializer(serializers.Serializer):
    pass

class LikeGetResponseSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    name = serializers.CharField()
    price = serializers.IntegerField()
    delivery_charge = serializers.IntegerField(default=0)
    link = serializers.URLField()
    image_url = serializers.URLField()
    category_id = serializers.IntegerField()
    created_at = serializers.DateTimeField()
    updated_at = serializers.DateTimeField()
    is_deleted = serializers.BooleanField()
    user = serializers.IntegerField()

class LikePostRequestSerializer(serializers.Serializer):
    name = serializers.CharField()
    price = serializers.IntegerField()
    delivery_charge = serializers.IntegerField(default=0)
    link = serializers.URLField()
    image_url = serializers.URLField()
    category_id = serializers.IntegerField()

class LikePostResponseSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    name = serializers.CharField()
    price = serializers.IntegerField()
    delivery_charge = serializers.IntegerField(default=0)
    link = serializers.URLField()
    image_url = serializers.URLField()
    category_id = serializers.IntegerField()
    created_at = serializers.DateTimeField()
    updated_at = serializers.DateTimeField()
    is_deleted = serializers.BooleanField()
    user = serializers.IntegerField()

class LikeDeleteRequestSerializer(serializers.Serializer):
    id = serializers.IntegerField()
