from django_backend.urls import path
from . import ali
from products.views import ScrapeTitleView
from search.views import KeywordView

urlpatterns = [
    path('info/', ali.ProductView.as_view(), name = 'info'),
    path('scrape/', ScrapeTitleView.as_view(), name='scrape'),
    path('keyword/', KeywordView.as_view(), name='keyword'),
]