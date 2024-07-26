from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Product, ProductManager
from search.models import Search
from .serializers import ProductSerializer, AliPostRequestSerializer, AliPostResponseSerializer
from drf_yasg.utils import swagger_auto_schema
from environ import Env
from .tasks import get_ali_products
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
            # products = get_ali_products(search_url, category_id, keyword)
            task = get_ali_products.delay(search_url, category_id, keyword)
            task_id = task.id
            return Response(task_id, status=status.HTTP_200_OK)
        except Search.DoesNotExist:
            print(f"Search object with search_url '{search_url}' does not exist.")
            return Response(status=status.HTTP_404_NOT_FOUND)

'''
    def get_ali_products(self, search_url, category_id, keyword):
        client = base.IopClient(URL, APP_KEY, APP_SECRET)
        request = base.IopRequest('aliexpress.affiliate.product.query')
        request.add_api_param('app_signature', '')
        request.add_api_param('category_ids', category_id)
        request.add_api_param('fields', 'commission_rate,sale_price')
        request.add_api_param('keywords', keyword)
        request.add_api_param('max_sale_price', '100')
        request.add_api_param('min_sale_price', '15')
        request.add_api_param('page_no', '1')
        request.add_api_param('page_size', '20')
        request.add_api_param('platform_product_type', 'ALL')
        request.add_api_param('sort', '')
        request.add_api_param('target_currency', 'KRW')
        request.add_api_param('target_language', 'KO')
        request.add_api_param('tracking_id', 'default')
        request.add_api_param('ship_to_country', '')
        request.add_api_param('delivery_days', '')
        response = client.execute(request)

        products = response.body.get('aliexpress_affiliate_product_query_response', {}).get('resp_result', {}).get('result', {}).get('products', {}).get('product', [])
        saved_products = []
        for product_data in products[:20]:
            product = Product(
                product_name=product_data.get('product_title'),
                price=product_data.get('target_app_sale_price'),
                delivery_charge=0,
                link=product_data.get('product_detail_url'),
                image_url=product_data.get('product_main_image_url'),
                category_id=category_id
            )
            saved_products.append(product)

        ProductManager.save_to_redis(search_url, saved_products)
        serializer = ProductSerializer(saved_products, many=True)
        return serializer.data
'''