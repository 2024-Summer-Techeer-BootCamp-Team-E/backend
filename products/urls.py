from django_backend.urls import path
from . import ali
urlpatterns = [
    path('', ali.ProductView.as_view(), name = 'info'),
]