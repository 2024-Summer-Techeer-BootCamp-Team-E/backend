from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from .amazon import Comprehend

class TranslateView(APIView):
    def post(self, request):
        search_url = request.data['search_url']
        product_name = request.data['product_name']

        translate_text = Comprehend.translate(product_name)
        
        types = ['ORGANIZATION', 'COMMERCIAL_ITEM', 'QUANTITY']
        keyword_list = []

        keyword = Comprehend.entities1(translate_text)
        
        for entity in keyword['Entities']:
            if entity['Type'] in types:
                keyword_list.append(entity['Text'])


