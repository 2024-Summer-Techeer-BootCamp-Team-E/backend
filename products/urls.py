from django_backend.urls import path
from . import ali
from products.views import ScrapeTitleView

urlpatterns = [
    path('info/', ali.ProductView.as_view(), name = 'info'),
    path('scrape/', ScrapeTitleView.as_view(), name='scrape'),
]