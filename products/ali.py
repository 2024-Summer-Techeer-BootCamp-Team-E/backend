from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Product
from .serializers import ProductSerializer
from rest_framework import status
from django.contrib.sites import requests
from .iop import base
from environ import Env

env = Env()
env.read_env()

URL = env('ALI_URL')
APP_KEY = env('ALI_APPKEY')
APP_SECRET = env('ALI_APPSECRET')


class product_detail_API(APIView):
  # SELECT
  def get(self, request):
    queryset = Product.objects.all()
    serializer = ProductSerializer(queryset, many=True)   #딕셔너리 -> json data로 변환
    return Response(serializer.data)


# INSERT
def getAliAPI(request):
  search_id = request.data['search_id']
  category_id = request.data['category_id']
  keyword = request.data['keyword']


  client = base.IopClient(URL, APP_KEY, APP_SECRET)
  request = base.IopRequest('aliexpress.affiliate.product.query')
  request.add_api_param('app_signature', '')  # API signature을 입력해야되는데 그런거 없음
  request.add_api_param('category_ids', category_id)  # 상품이 어떤 종류로 되어 있는지
  request.add_api_param('fields', 'commission_rate,sale_price')  # Respond parameter list. eg: commission_rate,sale_price
  request.add_api_param('keywords', keyword)  # 검색
  request.add_api_param('max_sale_price', '100')  # 상한선 설정
  request.add_api_param('min_sale_price', '15')  # 하한선 설정
  request.add_api_param('page_no', '1')  # 첫번째 장
  request.add_api_param('page_size', '5')  # 검색해본 페이지의 수
  request.add_api_param('platform_product_type', 'ALL')  #
  request.add_api_param('sort', 'SALE_PRICE_ASC')  # 정렬 순서 설정
  request.add_api_param('target_currency', 'KRW')  # 한화
  request.add_api_param('target_language', 'KO')  # 한글
  request.add_api_param('tracking_id', 'default')  # 그냥 trackingID
  request.add_api_param('ship_to_country', '')  # 잘 모르겠음 한국을 넣으려고 했는데 다 안됨
  request.add_api_param('delivery_days', '')  # 배송 예정일
  response = client.execute(request)

  products = response.body.aliexpress_affiliate_product_query_response.resp_result.result.products.product
  for i in products:
    # id, name, price, delivery_charge, link, image_url -> json data에서 알맞게 수정.
    id = products[i].id
    name = products[i].name
    price = products[i].price
    delivery_charge = products[i].delivery_charge
    link = products[i].link
    image_url = products[i].image_url

    product = Product(id=id, search_id=search_id, product_name=name, price=price, delivery_charge = delivery_charge, link=link, image_url=image_url, category_id=category_id)
    product.save()
    serializer = ProductSerializer(product)
    return Response(serializer.data)
