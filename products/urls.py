from django_backend.urls import path
from . import views
from products.ali import product_detail_API
urlpatterns = [
    path('', views.index),
    path('products/info/', product_detail_API.as_view(), name = 'info'),
]