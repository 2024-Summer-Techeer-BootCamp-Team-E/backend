from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Product
from .serializers import (
  ProductSerializer,
  AliPostRequestSerializer,
  AliPostResponseSerializer
)
from rest_framework import status
from .iop import base
from environ import Env
from search.models import Search
from drf_yasg.utils import swagger_auto_schema

env = Env()
env.read_env()

URL = env('ALI_URL')
APP_KEY = env('ALI_APPKEY')
APP_SECRET = env('ALI_APPSECRET')

class ProductView(APIView):
  @swagger_auto_schema(request_body=AliPostRequestSerializer, responses={"201": AliPostResponseSerializer})
  def post(self, request):
    search_url = request.data['search_url']
    category_id = request.data['category_id']
    keyword = request.data['keyword']
    n = request.data['page_num']

    try:
      searched_product = Search.objects.get(search_url=search_url)
      try:
        products = Product.objects.filter(search=searched_product)
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data)
      except Product.DoesNotExist:
        #검색 기록은 있지만 조회되는 상품이 없을때
        product_data = self.getAli(category_id, keyword, searched_product, n)
        return Response(product_data, status=status.HTTP_201_CREATED)
    except Search.DoesNotExist:
      # 검색 기록이 없는 경우 검색 기록 생성 후 제품 조회
      search = Search(
        search_url=search_url,
        name=request.data['search_name'],
        price=request.data['search_price'],
        delivery_charge=0
      )
      search.save()

      product_data = self.getAli(category_id, keyword, search, n)
      return Response(product_data, status=status.HTTP_201_CREATED)

  def getAli(self, category_id, keyword, search, n):
    client = base.IopClient(URL, APP_KEY, APP_SECRET)
    request = base.IopRequest('aliexpress.affiliate.product.query')
    request.add_api_param('app_signature', '')  # API signature을 입력해야 되는데 그런 거 없음
    request.add_api_param('category_ids', category_id)  # 상품이 어떤 종류로 되어 있는지
    request.add_api_param('fields', 'commission_rate,sale_price')  #
    request.add_api_param('keywords', keyword)  # 검색
    request.add_api_param('max_sale_price', '100')  # 상한선 설정
    request.add_api_param('min_sale_price', '15')  # 하한선 설정
    request.add_api_param('page_no', '1')  # 첫번째 장
    request.add_api_param('page_size', n)  # 검색해본 페이지의 수
    request.add_api_param('platform_product_type', 'ALL')  #
    request.add_api_param('sort', '')  # 정렬 순서 설정
    request.add_api_param('target_currency', 'KRW')  # 한화
    request.add_api_param('target_language', 'KO')  # 한글
    request.add_api_param('tracking_id', 'default')  # 그냥 trackingID
    request.add_api_param('ship_to_country', '')  # 잘 모르겠음 한국을 넣으려고 했는데 다 안됨
    request.add_api_param('delivery_days', '')  # 배송 예정일
    response = client.execute(request)

    products = response.body['aliexpress_affiliate_product_query_response']['resp_result']['result']['products'][
      'product']
    saved_products = []
    for i in range(0, int(n)):  # 최대 5개의 상품만 저장
      name = products[i].get('product_title')
      price = products[i].get('target_app_sale_price')
      delivery_charge = 0
      link = products[i].get('product_detail_url')
      image_url = products[i].get('product_main_image_url')

      product = Product(
        search=search,
        name=name,
        price=price,
        delivery_charge=delivery_charge,
        link=link,
        image_url=image_url,
        category_id=category_id
      )
      product.save()
      saved_products.append(product)

    serializer = ProductSerializer(saved_products, many=True)
    return serializer.data

