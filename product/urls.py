from django_backend.urls import path
from .views import ScrapeTitleView

# from . import views #이거 원래

urlpatterns = [
    path('scrape/', ScrapeTitleView.as_view(), name='scrape'),
]
