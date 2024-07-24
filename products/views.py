import requests
from bs4 import BeautifulSoup
from django.http import JsonResponse
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from search.models import Search
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from search.serializers import SearchSerializer
import logging

# 크롤링
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
import time

# 로거 설정
logger = logging.getLogger(__name__)

# Utility function to clean price strings
def clean_price(price_str):
    return price_str.replace(',', '')

class ScrapeTitleView(APIView):
    #이거 ViewSet으로 한번 해보자
    @swagger_auto_schema(
        operation_description="URL에서 제품 정보를 스크랩",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'url': openapi.Schema(type=openapi.TYPE_STRING)
            },
            required=['url']
        ),

        responses={
            200: openapi.Response(
                description="성공",
            ),
            500: "서버 오류"
        }
    )

    def post(self, request):
        url = request.data.get('url', None)

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
