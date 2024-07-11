from django.http import HttpResponse
from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from .serializers import ProductSerializer

class ProductInfo(generics.GenericAPIView):
    serializer_class = ProductSerializer