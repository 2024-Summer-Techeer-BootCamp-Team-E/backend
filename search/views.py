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
        
        keyword = comprehend.entities1(translate_text)

        #commercial_item_texts = extract_commercial_item_text(keyword)
        #keyword_list.append(commercial_item_texts)

        if 'COMMERCIAL_ITEM' not in [entity['Type'] for entity in keyword['Entities']]:
            gpt_keyword = extracter.extract_keywords(translate_text)
            # JSON 문자열을 파이썬 딕셔너리로 로드
            data_dict = json.loads(gpt_keyword)

            # KEYWORDS 필드에 접근 
            keyword_list = data_dict["KEYWORDS"]
            '''
            if data_dict["CATEGORIES"].get("FASHION"):
                category_id = 1
            elif data_dict["CATEGORIES"].get("HOME"):
                category_id = 2
            elif data_dict["CATEGORIES"].get("ELECTRONICS"):
                category_id = 3
            elif data_dict["CATEGORIES"].get("BEAUTY"):
                category_id = 4
            elif data_dict["CATEGORIES"].get("SPORTS"):
                category_id = 5
            elif data_dict["CATEGORIES"].get("AUTOMOBILE"):
                category_id = 6
            elif data_dict["CATEGORIES"].get("EXTRA"):
                category_id = 7
            '''
            category_list = data_dict["PERCENTAGE"]
            max_key = max(category_list, key=lambda k: category_list[k])
            category_id = types.index(max_key)

        else:
            for entity in keyword.get('Entities', []):
                if entity.get('Type') in types:
                    keyword_list.append(entity.get('Text'))

            category_id = 0
        
        if isinstance(keyword_list, list):
            keyword_str = ', '.join(keyword_list)

        '''
        if isinstance(category_list[category], list):
            category_id = ', '.join(category_list)
        '''

        #category_id = [", ".join(map(str, category_list[category]))]

        product.category_id = category_id
        product.keyword = keyword_str
        product.save()

        serializer = KeywordsSerializer(product)
        return Response(serializer.data, status=status.HTTP_202_ACCEPTED)