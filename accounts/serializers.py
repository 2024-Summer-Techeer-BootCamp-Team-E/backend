from rest_framework import serializers
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from .models import Account

class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = ('user_id', 'password', 'name')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = Account.objects.create_user(**validated_data)
        return user

class LoginSerializer(serializers.Serializer):
    user_id = serializers.CharField()
    password = serializers.CharField(write_only=True)
    access = serializers.CharField(read_only=True)
    refresh = serializers.CharField(read_only=True)

    def validate(self, data):
        user_id = data.get('user_id')
        password = data.get('password')

        if user_id and password:
            user = authenticate(user_id=user_id, password=password)
            if not user:
                raise serializers.ValidationError('유효하지 않은 아이디입니다.')
        else:
            raise serializers.ValidationError('Both "user_id" and "password" are required.')

        refresh = RefreshToken.for_user(user)
        return {
            'user_id': user.user_id,
            'access': str(refresh.access_token),
            'refresh': str(refresh),
        }