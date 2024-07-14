from rest_framework import serializers
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from .models import Account

class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = ('email', 'password')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = Account.objects.create_user(**validated_data)
        return user

class LoginSerializer(serializers.Serializer):
    email = serializers.CharField()
    password = serializers.CharField(write_only=True)
    access = serializers.CharField(read_only=True)
    refresh = serializers.CharField(read_only=True)

    def validate(self, data):
        email = data.get('email')
        password = data.get('password')

        if email and password:
            user = authenticate(email=email, password=password)
            if not user:
                raise serializers.ValidationError('유효하지 않은 아이디입니다.')
        else:
            raise serializers.ValidationError('Both "email" and "password" are required.')

        refresh = RefreshToken.for_user(user)
        return {
            'email': user.email,
            'access': str(refresh.access_token),
            'refresh': str(refresh),
        }
