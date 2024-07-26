# Create your tasks here
from __future__ import absolute_import, unicode_literals
from .serializers import ProductSerializer
from .models import Product, ProductManager
from celery import shared_task
from environ import Env
from .iop import base

env = Env()
env.read_env()

URL = env('ALI_URL')
APP_KEY = env('ALI_APPKEY')
APP_SECRET = env('ALI_APPSECRET')


@shared_task
def get_ali_products(search_url, category_id, keyword):
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