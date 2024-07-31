from .amazon import Comprehend
from .models import Search
import json
from celery import shared_task
from .gpt import CoreWordExtractor, ProductCategorizer

@shared_task
def get_keyword(search_url):
  search_product = Search.objects.get(search_url=search_url)

  comprehend = Comprehend()
  categorizer = ProductCategorizer()
  extracter = CoreWordExtractor()
  translate_text = comprehend.translate(search_product.name)

  keyword_list = []

  category_list = ['', 'FASHION', 'HOME', 'ELECTRONICS', 'BEAUTY', 'SPORTS', 'AUTOMOBILE', 'EXTRA']
  category = json.loads(categorizer.categorizer(translate_text))
  for i in range(1, len(category_list)):
    if category["CATEGORY_ID"] == category_list[i]:
      category_id = i
      break

  product_keyword = json.loads(extracter.extract_corewords(translate_text))
  keyword_list.append(product_keyword["COREWORD"])

  if isinstance(keyword_list, list):
    keyword = ', '.join(keyword_list)

  keyword = comprehend.translate(keyword)
  search_product.category_id = category_id
  search_product.keyword = keyword
  search_product.save()

  return search_url
