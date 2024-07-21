from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from .amazon import Comprehend
from .models import Search
from products.models import Product
from products.serializers import ProductSerializer


class KeywordView(APIView):
    def getKewords(self, request):
        search_url = request.data['search_url']

        searched_product = Product.objects.filter(search_url=search_url).values('name')

        translate_text = Comprehend.translate(searched_product)
                
        types = ['ORGANIZATION', 'COMMERCIAL_ITEM', 'QUANTITY', 'OTHER']
        keyword_list = []

        keyword = Comprehend.entities1(translate_text)

        if 'COMMERCIAL_ITEM' not in keyword['Entities']:
            #keyword = Comprehend.entities2(translate_text)
            
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        for entity in keyword['Entities']:
            if entity['Type'] in types:
                keyword_list.append(entity['Text'])
        
        category_id = 0
        product_data = {
            "keyword": keyword_list,
            "category_id": category_id,
        }

        serializer = ProductSerializer(data=product_data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)