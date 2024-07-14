from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import LikeProduct
from .serializers import (
  LikeProductSerializer,
  LikeGetRequestSerializer,
  LikeGetResponseSerializer,
  LikePostRequestSerializer,
  LikePostResponseSerializer,
  LikeDeleteRequestSerializer
)
from drf_yasg.utils import swagger_auto_schema
# Create your views here.

class LikeProductView(APIView):
  permission_classes = [IsAuthenticated]

  @swagger_auto_schema(request_body=LikePostRequestSerializer, responses={"201": LikePostResponseSerializer})
  def post(self, request):
    try:
      user_id = request.user
      name = request.data['name']
      price = request.data['price']
      delivery_charge = request.data['delivery_charge']
      link = request.data['link']
      image_url = request.data['image_url']
      category_id = request.data['category_id']

      # Check if product_id is provided
      if not user_id:
        return Response({"error": "로그인 해야 사용할 수 있습니다"}, status=status.HTTP_400_BAD_REQUEST)

      like_product = LikeProduct(user=user_id, name=name, price=price, delivery_charge=delivery_charge, link=link, image_url=image_url, category_id=category_id)
      like_product.save()

      serializer = LikeProductSerializer(like_product)
      return Response(serializer.data, status=status.HTTP_201_CREATED)

    except ValueError as e:
      return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    except Exception as e:
      return Response({"error": "An unexpected error occurred: " + str(e)},
                      status=status.HTTP_500_INTERNAL_SERVER_ERROR)

  @swagger_auto_schema(query_serializer=LikeGetRequestSerializer, responses={"200":LikeGetResponseSerializer})
  def get(self, request): #헤더에 access 토큰 박아야됨
    try:
      # 현재 인증된 사용자의 좋아요한 상품들을 필터링하여 가져옵니다.
      liked_products = LikeProduct.objects.filter(user=request.user)
      serializer = LikeProductSerializer(liked_products, many=True)
      return Response(serializer.data, status=status.HTTP_200_OK)
    except Exception as e:
      return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

  @swagger_auto_schema(request_body=LikeDeleteRequestSerializer, responses={"204": 'Deleted successfully', "404": 'LikeProduct not found', "400": 'Error'})
  def delete(self, request):
    id = request.data.get('id')
    user_id = request.user

    try:
        del_Likeproducts = LikeProduct.objects.get(id=id, user_id=user_id)
        del_Likeproducts.delete()
        return Response({'message': 'Deleted successfully'}, status=status.HTTP_204_NO_CONTENT)
    except LikeProduct.DoesNotExist:
        return Response({'error': 'LikeProduct not found'}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)


