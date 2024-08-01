import requests
import re
from bs4 import BeautifulSoup
from django.http import JsonResponse
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from search.models import Search
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from search.serializers import SearchSerializer
from django.core.exceptions import MultipleObjectsReturned, ObjectDoesNotExist
import logging

# 크롤링
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
import time

# Celery
from .tasks import get_chrome, get_ali
from search.tasks import get_keyword
from celery import chain

# 로거 설정
logger = logging.getLogger(__name__)

# Utility function to clean price strings
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

class ScrapeTitleView(APIView):
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
        chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.5615.49 Safari/537.36")
        chrome_options.add_argument("--headless")  # Run in headless mode
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.binary_location = "/usr/bin/chromium"
        
        driver = webdriver.Chrome(service=Service("/usr/bin/chromedriver"), options=chrome_options)
        # driver = webdriver.Chrome(executable_path=ChromeDriverManager().install(), options=options)

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
            if "smartstore.naver" in url:
                # 상품명
                name_element = wait.until(
                    EC.visibility_of_element_located((By.CSS_SELECTOR, "h3._22kNQuEXmb._copyable"))
                )
                product_name = name_element.text.strip()

                # 가격
                price_element = wait.until(
                    EC.visibility_of_element_located((By.CSS_SELECTOR, "span.aICRqgP9zw _2oBq11Xp7s"))
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

            elif "11st.co.kr" in url:
                # 11번가
                # 상품명
                print("Finding product name element...")
                name_element = wait.until(
                    EC.visibility_of_element_located((By.CSS_SELECTOR, "h1.title"))
                )
                product_name = name_element.text.strip()
                print(f"Product Name: {product_name}")

                # 가격
                print("Finding product price element...")
                price_element = wait.until(
                    EC.visibility_of_element_located((By.CSS_SELECTOR, "span.value"))
                )
                product_price = clean_price(price_element.text.strip())
                print(f"Product Price: {product_price}")

                # 배송비
                delivery_element = wait.until(
                    EC.visibility_of_element_located((By.XPATH, "//dt[contains(., '배송비')]"))
                )
                delivery_text = delivery_element.text.strip()

                delivery_parts = delivery_text.split()
                for part in delivery_parts:
                    if "무료배송" in part:
                        product_delivery = clean_price(0)
                        break
                    if "원" in part:
                        product_delivery =clean_price (re.sub(r'[^0-9]', '', part))
                        break
                else:
                    product_delivery = clean_price(0)

                # 상품 이미지
                print("Finding product image element...")
                image_element = wait.until(
                    EC.visibility_of_element_located((By.CSS_SELECTOR, "img[onerror=\"this.src='https://cdn.011st.com/11dims/resize/600x600/quality/75/11src/img/product/no_image.gif'\"]"))
                )
                product_image_url = image_element.get_attribute("src")
                print(f"Product Image: {product_image_url}")

            elif "coupang" in url:
                #쿠팡
                # 상품명
                print("Finding product name element...")
                name_element = wait.until(
                    EC.visibility_of_element_located((By.CSS_SELECTOR, "h1.prod-buy-header__title"))
                )
                product_name = name_element.text.strip()
                print(f"Product Name: {product_name}")

                # 가격
                print("Finding product price element...")
                price_element = wait.until(
                    EC.visibility_of_element_located((By.CSS_SELECTOR, "span.total-price"))
                )
                product_price = clean_price(price_element.text.strip())
                print(f"Product Price: {product_price}")

                # 배송비
                print("Finding product elivery element...")
                delivery_element = wait.until(
                    EC.visibility_of_element_located((By.CSS_SELECTOR, "span.shipping-fee-txt"))
                )
                product_delivery = clean_price(delivery_element.text.strip())
                print(f"Product Price: {product_delivery}")


                # 상품 이미지
                print("Finding product img element...")
                image_element = wait.until(
                    EC.visibility_of_element_located((By.CSS_SELECTOR, "img.prod-image__detail"))
                )
                product_image_url = image_element.get_attribute("src")
                print(f"Product Image: {product_image_url}")

            elif "kurly" in url:
                # 마켓컬리
                # 상품명
                print("Finding product name element...")
                name_element = wait.until(
                    EC.visibility_of_element_located((By.CSS_SELECTOR, "h1.css-79gmk3 ezpe9l11"))
                )
                product_name = name_element.text.strip()
                print(f"Product Name: {product_name}")

                # 가격
                print("Finding product price element...")
                price_element = wait.until(
                    EC.visibility_of_element_located((By.CSS_SELECTOR, "span.css-9pf1ze e1q8tigr2"))
                )
                product_price = clean_price(price_element.text.strip())
                print(f"Product Price: {product_price}")

                # 배송비
                print("Finding product elivery element...")
                if product_price >= 40000:
                    product_delivery = 0
                else:
                    product_delivery = 3000
                print(f"Product Price: {product_delivery}")

                # 상품 이미지
                print("Finding product img element...")
                image_element = wait.until(
                    EC.visibility_of_element_located((By.CSS_SELECTOR, "img.css-1zjvv7"))
                )
                product_image_url = image_element.get_attribute("src")
                print(f"Product Image: {product_image_url}")

            else:
                driver.quit()
                return JsonResponse({'error': '지원되지 않는 URL입니다.'}, status=status.HTTP_400_BAD_REQUEST)

            # URL
            link = url

            # Combine product info
            # combined_info = f"{product_name} - {product_price} - {link} - {product_delivery} - {product_image_url}"
            # product_info_list.append(combined_info)

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

class Async_chain(APIView):
    @swagger_auto_schema(
        operation_description="URL에서 제품 정보를 스크랩 -> keyword 분석 -> Ali API 호출",
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
        url = request.data['url']
        task_chain = chain(get_chrome.s(url) | get_keyword.s() | get_ali.s())
        result = task_chain()

        products = result.get()

        try:
            search = Search.objects.get(search_url=url)
        except MultipleObjectsReturned:
            return Response({"error": "Multiple search results found for the given URL."},
                            status=status.HTTP_400_BAD_REQUEST)
        except ObjectDoesNotExist:
            return Response({"error": "No search results found for the given URL."}, status=status.HTTP_404_NOT_FOUND)

        search_data = {
            "name": search.name,
            "price": search.price,
            "delivery_charge": search.delivery_charge,
            "image_url": search.image_url,
            "search_url": search.search_url
        }

        serializer = SearchSerializer(data=search_data)
        if serializer.is_valid():
            return Response({"search": serializer.data, "products": products}, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)