from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import LikeProduct
from .serializers import LikeProductSerializer
from products.models import Product
# Create your views here.

class LikeProductView(APIView):
  permission_classes = [IsAuthenticated]

  def post(self, request):
    try:
      user_id = request.user
      product_id = request.data.get('product')

      # Check if product_id is provided
      if not product_id:
        return Response({"error": "Product ID is required"}, status=status.HTTP_400_BAD_REQUEST)

      # Get the Product instance
      try:
        product = Product.objects.get(id=product_id)
      except Product.DoesNotExist:
        return Response({"error": "Product not found"}, status=status.HTTP_404_NOT_FOUND)

      like_product = LikeProduct(user=user_id, product=product, product_number=1)
      like_product.save()

      serializer = LikeProductSerializer(like_product)
      return Response(serializer.data, status=status.HTTP_201_CREATED)

    except ValueError as e:
      return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    except Exception as e:
      return Response({"error": "An unexpected error occurred: " + str(e)},
                      status=status.HTTP_500_INTERNAL_SERVER_ERROR)



  def get(self, request): #헤더에 access 토큰 박아야됨
    try:
      # 현재 인증된 사용자의 좋아요한 상품들을 필터링하여 가져옵니다.
      liked_products = LikeProduct.objects.filter(user=request.user)
      serializer = LikeProductSerializer(liked_products, many=True)
      return Response(serializer.data, status=status.HTTP_200_OK)
    except Exception as e:
      return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

  def delete(self, request):
    id = request.data.get('id')
    user_id = request.user
    product_id = request.data.get('product')

    try:
        del_Likeproducts = LikeProduct.objects.get(id=id, user_id=user_id, product_id=product_id)
        del_Likeproducts.delete()
        return Response({'message': 'Deleted successfully'}, status=status.HTTP_204_NO_CONTENT)
    except LikeProduct.DoesNotExist:
        return Response({'error': 'LikeProduct not found'}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)


