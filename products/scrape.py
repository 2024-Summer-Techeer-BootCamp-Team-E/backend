from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
import time

# Setup Chrome options
chrome_options = Options()
chrome_options.add_argument("--headless")  # Run in headless mode
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.page_load_strategy = 'eager'  # Eager page load strategy

# Use ChromeDriverManager to install and setup Chrome WebDriver
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=chrome_options)

# URL to be scraped
url = "https://smartstore.naver.com/monikhan/products/9988019725?NaPm=ct%3Dlyi9gra0%7Cci%3D36c66802a5f21d55a198905e5d1cff47498536b1%7Ctr%3Dnshfu%7Csn%3D204454%7Chk%3D131005aab83d89ab4aae016e0eacc46d316ac240"

# Open the page
print("Loading page...")
driver.get(url)
print("Page loaded.")
time.sleep(3)

# Initialize WebDriverWait
wait = WebDriverWait(driver, 10)

# List to store product info
product_info_list = []

try:
    #상품명
    print("Finding product name element...")
    name_element = wait.until(
        EC.visibility_of_element_located((By.CSS_SELECTOR, "h3._22kNQuEXmb._copyable"))
    )
    product_name = name_element.text.strip()
    print(f"Product Name: {product_name}")

    #가격
    print("Finding product price element...")
    price_element = wait.until(
        EC.visibility_of_element_located((By.CSS_SELECTOR, "span._1LY7DqCnwR"))
    )
    product_price = price_element.text.strip()
    print(f"Product Price: {product_price}")

    #배송비
    print("Finding product delivery charge element...")
    delivery_element = wait.until(
        EC.visibility_of_element_located((By.CSS_SELECTOR, "span.bd_3uare"))
    )
    product_delivery = delivery_element.text.strip()
    print(f"Product Price: {product_delivery}")

    # 상품 이미지
    print("Finding product image element...")
    image_element = wait.until(
        EC.visibility_of_element_located((By.CSS_SELECTOR, "img.bd_2DO68"))
    )
    product_image_url = image_element.get_attribute("src")
    print(f"Product Price: {product_image_url}")

    # URL
    product_link = url

    # Combine product info
    combined_info = f"{product_name} - {product_price} - {product_link} - {product_delivery} - {product_image_url}"
    product_info_list.append(combined_info)

except Exception as e:
    print(f"An error occurred: {e}")

finally:
    driver.quit()

# 결과 출력
for info in product_info_list:
    print(info)
