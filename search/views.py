from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from .amazon import Comprehend
from .models import Search

def getKewords(self, request):
    search_url = request.data['search_url']

    searched_product = Search.objects.filter(search_url=search_url).values('name')

    translate_text = Comprehend.translate(searched_product)
            
    types = ['ORGANIZATION', 'COMMERCIAL_ITEM', 'QUANTITY']
    keyword_list = []

    keyword = Comprehend.entities1(translate_text)

    #if 'COMMERCIAL_ITEM' not in keyword['Entities']:
    #    keyword = Comprehend.entities2(translate_text)
    #    categories_id = 0
    #    search = Search(
    #        categories_id = categories_id
    #        keyword = keyword
    #    )
    #    search.save()
            
    for entity in keyword['Entities']:
        if entity['Type'] in types:
            keyword_list.append(entity['Text'])

    
