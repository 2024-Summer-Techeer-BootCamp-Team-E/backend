from django_backend.urls import path
from products.views import Async_chain

urlpatterns = [
    path('info/', Async_chain.as_view(), name='info')
]