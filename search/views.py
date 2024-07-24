from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from drf_yasg.utils import swagger_auto_schema
from .amazon import Comprehend
from .models import Search
from .gpt import KeywordExtractor
from products.models import Product
from .serializers import KeywordsSerializer
from .serializers import KeywordRequestSerializer, KeywordResponseSerializer
import json

def extract_commercial_item_text(data):
    commercial_items = []
    for entity in data.get('Entities', []):
        if entity.get('Type') == 'COMMERCIAL_ITEM':
            commercial_items.append(entity.get('Text'))
    return commercial_items

class KeywordView(APIView):

    @swagger_auto_schema(request_body=KeywordRequestSerializer, responses={"200": KeywordResponseSerializer})
    def post(self, request):
        try:
            search_url = request.data.get('search_url')
            if not search_url:
                return Response({"error": "URL is required"}, status=status.HTTP_400_BAD_REQUEST)
            
            existing_urls = Search.objects.filter(search_url=search_url)
            if existing_urls.exists():
                # keyword 값이 null인지 확인
                null_keywords = existing_urls.filter(keyword__isnull=True)
                if null_keywords.exists():
                    pass
            
        except Exception as e:
            return Response({"Error : ", str(e)}, status=status.HTTP_400_BAD_REQUEST)
        
        product = get_object_or_404(Search, search_url=search_url)

        try:
            if not product.name:
                return Response({"error": "No name provided"}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"Error : ", str(e)}, status=status.HTTP_400_BAD_REQUEST)

        comprehend = Comprehend()
        extracter = KeywordExtractor()
        translate_text = comprehend.translate(product.name)
                
        types = ['ORGANIZATION', 'COMMERCIAL_ITEM', 'QUANTITY', 'OTHER', 'FASHION', 'HOME', 
                'SPORTS', 'ELECTRONICS', 'BEAUTY', 'AUTOMOBILE', 'EXTRA', 'FEATURE']
        keyword_list = []
        category_list = [[0],
                        [3, 200000345, 200000343, 200000297, 201768104, 200574005, 200165144],
                        [6, 13, 15, 1503, 39],
                        [7, 44, 502, 509],
                        [66],
                        [18],
                        [34],
                        [30, 21, 26, 36, 1420, 320]]
        
        keyword = comprehend.entities1(translate_text)

        #commercial_item_texts = extract_commercial_item_text(keyword)
        #keyword_list.append(commercial_item_texts)

        if 'COMMERCIAL_ITEM' not in [entity['Type'] for entity in keyword['Entities']]:
            gpt_keyword = extracter.extract_keywords(translate_text)
            # JSON 문자열을 파이썬 딕셔너리로 로드
            data_dict = json.loads(gpt_keyword)

            # KEYWORDS 필드에 접근 
            keyword_list = data_dict["KEYWORDS"]
            if data_dict["CATEGORIES"].get("FASHION") is not None:
                category_id = 1
            elif data_dict["CATEGORIES"].get("HOME") is not None:
                category_id = 2
            elif data_dict["CATEGORIES"].get("ELECTRONICS") is not None:
                category_id = 3
            elif data_dict["CATEGORIES"].get("BEAUTY") is not None:
                category_id = 4
            elif data_dict["CATEGORIES"].get("SPORTS") is not None:
                category_id = 5
            elif data_dict["CATEGORIES"].get("AUTOMOBILE") is not None:
                category_id = 6
            elif data_dict["CATEGORIES"].get("EXTRA") is not None:
                category_id = 7        

        else:
            for entity in keyword.get('Entities', []):
                if entity.get('Type') in types:
                    keyword_list.append(entity.get('Text'))

            category_id = 0
        
        if isinstance(keyword_list, list):
            keyword_str = ', '.join(keyword_list)

        product.category_id = category_list[category_id]
        product.keyword = keyword_str
        product.save()

        serializer = KeywordsSerializer(product)
        return Response(serializer.data, status=status.HTTP_202_ACCEPTED)