from django_backend.urls import path
from . import views
from product.ali import product_detail_API
urlpatterns = [
    path('', views.index),
    path('product/info/', product_detail_API.as_view(), name = 'info'),
]