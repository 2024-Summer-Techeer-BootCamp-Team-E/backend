from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Product
from .serializers import ProductSerializer
from rest_framework import status
from django.contrib.sites import requests
import iop
import environ

env = environ.Env()
env.read_env()

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
        #keyword = request.data
        keyword = 'mp3' # example
        category_id = '44' #example (키워드마다 카테고리 아이디 다르게 해야됨)

        client = iop.IopClient(env('ALI_URL'), env('ALI_APPKEY'), env('ALI_APPSECRET'))
        request = iop.IopRequest('aliexpress.affiliate.product.query')
        request.add_api_param('app_signature', '') # API signature을 입력해야되는데 그런거 없음
        request.add_api_param('category_ids', category_id) # 상품이 어떤 종류로 되어 있는지
        request.add_api_param('fields', 'commission_rate,sale_price') # Respond parameter list. eg: commission_rate,sale_price
        request.add_api_param('keywords', keyword) # 검색 (keyword를 어떻게 가져오는지 아직 미정)
        request.add_api_param('max_sale_price', '100') # 상한선 설정
        request.add_api_param('min_sale_price', '15') # 하한선 설정
        request.add_api_param('page_no', '1') #첫번째 장
        request.add_api_param('page_size', '5') # 검색해본 페이지의 수
        request.add_api_param('platform_product_type', 'ALL') #
        request.add_api_param('sort', 'SALE_PRICE_ASC') # 정렬 순서 설정
        request.add_api_param('target_currency', 'KRW') # 한화
        request.add_api_param('target_language', 'KO') # 한글
        request.add_api_param('tracking_id', 'default') # 그냥 trackingID (default가 가장 기본ID)
        request.add_api_param('ship_to_country', '') # 잘 모르겠음 한국을 넣으려고 했는데 다 안됨
        request.add_api_param('delivery_days', '') # 배송 예정일
        response = client.execute(request)
        serializer = ProductSerializer(response)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


