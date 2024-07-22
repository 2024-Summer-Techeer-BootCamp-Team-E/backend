from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from drf_yasg.utils import swagger_auto_schema
from .amazon import Comprehend
from .models import Search
from products.models import Product
from .serializers import KeywordsSerializer
from .serializers import KeywordRequestSerializer, KeywordResponseSerializer

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
            
        except Exception as e:
            return Response({"Error : ", str(e)}, status=status.HTTP_400_BAD_REQUEST)
        
        product = get_object_or_404(Search, search_url=search_url)

        #name = Search.objects.filter(search_url=search_url).values('name')
        #price = Search.objects.filter(search_url=search_url).values('price')

        try:
            #name = request.data.get('name')
            if not product.name:
                return Response({"error": "No name provided"}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"Error : ", str(e)}, status=status.HTTP_400_BAD_REQUEST)

        comprehend = Comprehend()
        translate_text = comprehend.translate(product.name)
                
        types = ['ORGANIZATION', 'COMMERCIAL_ITEM', 'QUANTITY', 'OTHER']
        keyword_list = []

        keyword = comprehend.entities1(translate_text)

        #commercial_item_texts = extract_commercial_item_text(keyword)
        #keyword_list.append(commercial_item_texts)

        if 'COMMERCIAL_ITEM' not in [entity['Type'] for entity in keyword['Entities']]:
            return Response({"error": "No commercial item found"}, status=status.HTTP_400_BAD_REQUEST)

        for entity in keyword.get('Entities', []):
            if entity.get('Type') in types:
                keyword_list.append(entity.get('Text'))

        
        if isinstance(keyword_list, list):
            keyword_str = ', '.join(keyword_list)

        category_id = 0
        '''
        product_data = {
            "search_url":search_url,
            "name":product.name,
            "keyword": keyword_str,
            "category_id": category_id,
            "price":product.price,
        }
        #product.save()
        '''
        product.category_id = category_id
        product.keyword = keyword_str
        product.save()

        serializer = KeywordsSerializer(product)
        return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
        #return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)