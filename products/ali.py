import iop
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Product
from .serializers import ProductSerializer
from rest_framework import status
from django.contrib.sites import requests


# Ali API 관련 설정 (보류)
url = ""
tracking_id = ""
appKey = ""
appSecret = ""

class product_detail_API(APIView):
    # SELECT
    def get(self, request):
        queryset = Product.objects.all()
        serializer = ProductSerializer(queryset, many=True)   #딕셔너리 -> json data로 변환
        return Response(serializer.data)

    # INSERT
    def post(self, request):
        keyword = request.data

        client = iop.IopClient(url, appKey, appSecret)
        request = iop.IopRequest("aliexpress.affiliate.products.query")
        request.add_api_param("keywords", keyword)
        response = client.execute(request)
        serializer = ProductSerializer(response)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


