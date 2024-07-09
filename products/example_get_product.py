from python import iop
import time
import environ

env = environ.Env()
env.read_env()

URL = env('ALI_URL')
APP_KEY = env('ALI_APPKEY')
APP_SECRET = env('ALI_APPSECRET')

start_time = time.time()
client = iop.IopClient(URL, APP_KEY, APP_SECRET)
request = iop.IopRequest('aliexpress.affiliate.product.query')
request.add_api_param('app_signature', '') # API signature을 입력해야되는데 그런거 없음
request.add_api_param('category_ids', '44') # 상품이 어떤 종류로 되어 있는지
request.add_api_param('fields', 'commission_rate,sale_price') # Respond parameter list. eg: commission_rate,sale_price
request.add_api_param('keywords', 'mp3') # 검색
request.add_api_param('max_sale_price', '100') # 상한선 설정
request.add_api_param('min_sale_price', '15') # 하한선 설정
request.add_api_param('page_no', '1') #첫번째 장
request.add_api_param('page_size', '5') # 검색해본 페이지의 수
request.add_api_param('platform_product_type', 'ALL') #
request.add_api_param('sort', 'SALE_PRICE_ASC') # 정렬 순서 설정
request.add_api_param('target_currency', 'KRW') # 한화
request.add_api_param('target_language', 'KO') # 한글
request.add_api_param('tracking_id', 'default') # 그냥 trackingID
request.add_api_param('ship_to_country', '') # 잘 모르겠음 한국을 넣으려고 했는데 다 안됨
request.add_api_param('delivery_days', '') # 배송 예정일
response = client.execute(request)
print(response.type)
print(response.body)
end_time = time.time()
print('response time: ' + str(end_time - start_time))