# Create your tasks here
from __future__ import absolute_import, unicode_literals
from celery import shared_task
from .models import Product, ProductManager
from .serializers import ProductSerializer
from environ import Env
from .iop import base
from celery.result import AsyncResult

# 크롤링
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
import time

###
from django.http import JsonResponse
from rest_framework.response import Response
from rest_framework import status
from search.models import Search
from search.serializers import SearchSerializer
import logging


env = Env()
env.read_env()

URL = env('ALI_URL')
APP_KEY = env('ALI_APPKEY')
APP_SECRET = env('ALI_APPSECRET')

logger = logging.getLogger(__name__)

@shared_task
def get_ali(search_url):
  def get_ali_product(search_url, category_id, keyword):
    try:
      client = base.IopClient(URL, APP_KEY, APP_SECRET)
      request = base.IopRequest('aliexpress.affiliate.product.query')
      request.add_api_param('app_signature', '')
      request.add_api_param('category_ids', '')
      request.add_api_param('fields', 'commission_rate,sale_price')
      request.add_api_param('keywords', keyword)
      request.add_api_param('max_sale_price', '100')
      request.add_api_param('min_sale_price', '15')
      request.add_api_param('page_no', '1')
      request.add_api_param('page_size', '20')
      request.add_api_param('sort', '')
      request.add_api_param('target_currency', 'KRW')
      request.add_api_param('target_language', 'KO')
      request.add_api_param('tracking_id', 'default')
      request.add_api_param('ship_to_country', '')
      request.add_api_param('delivery_days', '')
      response = client.execute(request)

      logger.debug("AliExpress API 응답: %s", response)

      products = response.body.get('aliexpress_affiliate_product_query_response', {}).get('resp_result', {}).get('result', {}).get('products', {}).get('product', [])
      saved_products = []
      for product_data in products[:20]:
        product = Product(
          product_name=product_data.get('product_title'),
          price=product_data.get('target_sale_price'),
          delivery_charge=0,
          link=product_data.get('product_detail_url'),
          image_url=product_data.get('product_main_image_url'),
          category_id=category_id
        )
        saved_products.append(product)

      ProductManager.save_to_redis(search_url, saved_products)
      serializer = ProductSerializer(saved_products, many=True)
      return serializer.data
    except Exception as e:
      logger.error("AliExpress API 호출 중 오류 발생: %s", e)
      return {'error': 'AliExpress API 호출 중 오류 발생'}

  def handle_redis_miss(search_url):

    try:
      searched = Search.objects.get(search_url=search_url)
      category_id = searched.category_id
      keyword = searched.keyword
      products = get_ali_product(search_url, category_id, keyword)
      serializer = ProductSerializer(products, many=True)
      # return keyword
      return serializer.data
    except Search.DoesNotExist:
      logger.error("Search URL이 존재하지 않습니다: %s", search_url)
      return {'error': 'URL을 입력하시오.'}
    except Exception as e:
      logger.error("handle_redis_miss 중 오류 발생: %s", e)
      return {'error': '데이터베이스 접근 중 오류 발생'}

  try:
    if ProductManager.exists_in_redis(search_url):
      product_from_redis = ProductManager.get_from_redis(search_url)
      if product_from_redis:
        serializer = ProductSerializer(product_from_redis, many=True)
        return serializer.data
      else:
        return handle_redis_miss(search_url)
    else:
      return handle_redis_miss(search_url)
  except Exception as e:
    logger.error("Redis 접근 중 오류 발생: %s", e)
    return {'error': 'Redis 접근 중 오류 발생'}

@shared_task
def get_chrome(search_url):
  def clean_price(price_str):
    return price_str.replace(',', '')
  def chrome(url):
    # Setup Chrome options
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # Run in headless mode
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.binary_location = "/usr/bin/chromium"

    driver = webdriver.Chrome(service=Service("/usr/bin/chromedriver"), options=chrome_options)

    if not url:
      return JsonResponse({'error': 'URL을 입력하시오.'}, status=status.HTTP_400_BAD_REQUEST)

    existing_entry = Search.objects.filter(search_url=url).first()
    if existing_entry:
      serializer = SearchSerializer(existing_entry)
      driver.quit()
      return Response(serializer.data, status=status.HTTP_200_OK)

    driver.get(url)
    wait = WebDriverWait(driver, 10)
    product_info_list = []

    try:
      # 상품명
      name_element = wait.until(
        EC.visibility_of_element_located((By.CSS_SELECTOR, "h3._22kNQuEXmb._copyable"))
      )
      product_name = name_element.text.strip()

      # 가격
      price_element = wait.until(
        EC.visibility_of_element_located((By.CSS_SELECTOR, "span._1LY7DqCnwR"))
      )
      product_price = clean_price(price_element.text.strip())

      # 배송비
      delivery_element = wait.until(
        EC.visibility_of_element_located((By.CSS_SELECTOR, "span.bd_3uare"))
      )
      product_delivery = clean_price(delivery_element.text.strip())

      # 상품 이미지
      image_element = wait.until(
        EC.visibility_of_element_located((By.CSS_SELECTOR, "img.bd_2DO68"))
      )
      product_image_url = image_element.get_attribute("src")

      # URL
      link = url

      # Combine product info
      combined_info = f"{product_name} - {product_price} - {link} - {product_delivery} - {product_image_url}"
      product_info_list.append(combined_info)

      product_data = {
        "name": product_name,
        "price": product_price,
        "delivery_charge": product_delivery,
        "image_url": product_image_url,
        "search_url": link
      }

      serializer = SearchSerializer(data=product_data)
      if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
      return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    except Exception as e:
      logger.error(f"An error occurred: {str(e)}")
      print(f"An error occurred: {str(e)}")
      return JsonResponse({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    finally:
      driver.quit()


  chrome(search_url)
  # Setup Chrome options
  chrome_options = Options()
  chrome_options.add_argument("--headless")  # Run in headless mode
  chrome_options.add_argument("--no-sandbox")
  chrome_options.add_argument("--disable-dev-shm-usage")
  chrome_options.binary_location = "/usr/bin/chromium"

  driver = webdriver.Chrome(service=Service("/usr/bin/chromedriver"), options=chrome_options)

  existing_entry = Search.objects.filter(search_url=search_url).first()
  if existing_entry:
    serializer = SearchSerializer(existing_entry)
    driver.quit()
    return serializer.data.get('search_url')

  driver.get(search_url)
  time.sleep(3)
  wait = WebDriverWait(driver, 10)
  product_info_list = []

  try:
    # 상품명
    name_element = wait.until(
      EC.visibility_of_element_located((By.CSS_SELECTOR, "h3._22kNQuEXmb._copyable"))
    )
    product_name = name_element.text.strip()

    # 가격
    price_element = wait.until(
      EC.visibility_of_element_located((By.CSS_SELECTOR, "span._1LY7DqCnwR"))
    )
    product_price = clean_price(price_element.text.strip())

    # 배송비
    delivery_element = wait.until(
      EC.visibility_of_element_located((By.CSS_SELECTOR, "span.bd_3uare"))
    )
    product_delivery = clean_price(delivery_element.text.strip())

    # 상품 이미지
    image_element = wait.until(
      EC.visibility_of_element_located((By.CSS_SELECTOR, "img.bd_2DO68"))
    )
    product_image_url = image_element.get_attribute("src")

    # URL
    link = search_url

    # Combine product info
    combined_info = f"{product_name} - {product_price} - {link} - {product_delivery} - {product_image_url}"
    product_info_list.append(combined_info)

    product_data = {
      "name": product_name,
      "price": product_price,
      "delivery_charge": product_delivery,
      "image_url": product_image_url,
      "search_url": link
    }

    serializer = SearchSerializer(data=product_data)
    if serializer.is_valid():
      serializer.save()
      return serializer.data.get('search_url')
    else:
      return {'errors': serializer.errors}

  except Exception as e:
    logger.error(f"An error occurred: {str(e)}")
    print(f"An error occurred: {str(e)}")
    return {'error': str(e)}

  finally:
    driver.quit()

@shared_task
def get_keyword(search_url):
  keyword = "galaxy"
  return search_url