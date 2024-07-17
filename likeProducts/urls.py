from django.urls import path
from . import views
urlpatterns = [
  path('', views.LikeProductView.as_view(), name=''),
]