from django.http import HttpResponse
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import authenticate
from .serializers import ProductSerializer

