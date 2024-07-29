from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Product, ProductManager
from search.models import Search
from .serializers import ProductSerializer, AliPostRequestSerializer, AliPostResponseSerializer
from drf_yasg.utils import swagger_auto_schema
from environ import Env
from celery.result import AsyncResult
from .tasks import get_ali_products, get_ali
from .iop import base

env = Env()
env.read_env()

URL = env('ALI_URL')
APP_KEY = env('ALI_APPKEY')
APP_SECRET = env('ALI_APPSECRET')


class ProductView(APIView):
  @swagger_auto_schema(request_body=AliPostRequestSerializer, responses={"201": AliPostResponseSerializer})
  def post(self, request):
    search_url = request.data['search_url']

    # Redis에 검색 기록이 있는 경우
    if ProductManager.exists_in_redis(search_url):
      product_from_redis = ProductManager.get_from_redis(search_url)
      # Redis에 상품 기록이 있는 경우
      if product_from_redis:
        serializer = ProductSerializer(product_from_redis, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
      else:
        return self.handle_redis_miss(search_url)
    else:
      return self.handle_redis_miss(search_url)

  def handle_redis_miss(self, search_url):

    category_list = ['0',
                     '3, 200000345, 200000343, 200000297, 201768104, 200574005, 200165144',
                     '6, 13, 15, 1503, 39',
                     '7, 44, 502, 509',
                     '66',
                     '18',
                     '34',
                     '30, 21, 26, 36, 1420, 320']

    try:
      searched = Search.objects.get(search_url=search_url)
      category = searched.category_id
      category_id = category_list[category]
      keyword = searched.keyword

      task = get_ali_products.delay(search_url, category_id, keyword)
      async_result = AsyncResult(task.id)

      stop_n_go = async_result.get()
      readyplease = async_result.ready()
      if stop_n_go and readyplease:  # 작업이 완료되었는지
        products_data = async_result.result
        get_products = []
        for product in products_data[:20]:
          product = Product(
            product_name = product['product_name'],
            price = product['price'],
            delivery_charge = 0,
            link = product['link'],
            image_url = product['image_url'],
            category_id = category_id
          )
          get_products.append(product)
        serializer = ProductSerializer(get_products, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
      else:
        return Response(status=status.HTTP_425_TOO_EARLY)

    except Search.DoesNotExist:
      print(f"Search object with search_url '{search_url}' does not exist.")
      return Response(status=status.HTTP_404_NOT_FOUND)


