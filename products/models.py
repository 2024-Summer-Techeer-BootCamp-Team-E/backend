from django.db import models
import datetime
# Create your models here.

class Product(models.Model):
  id = models.AutoField(primary_key=True)  #
  product_name = models.CharField(max_length=100)
  category_id = models.IntegerField() #카테고리 아이디
  price = models.DecimalField(max_digits=10, decimal_places=2)  #가격
  delivery_charge = models.DecimalField(max_digits=10, decimal_places=2) # 배송비
  currency_id = models.IntegerField()   #화폐 단위
  link = models.URLField()
  image_url = models.URLField()
  created_at = models.DateTimeField(default=datetime.datetime.now)
  updated_at = models.DateTimeField(auto_now=True)
  is_deleted = models.BooleanField(default=False)
