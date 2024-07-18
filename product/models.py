from django.db import models

# Create your models here.

class Product(models.Model):
  id = models.AutoField(primary_key=True)
  name = models.CharField(max_length=100)
  category_id = models.IntegerField(default=1) #카테고리 아이디
  price = models.DecimalField(max_digits=10, decimal_places=2)  #가격
  delivery_charge = models.DecimalField(max_digits=10, decimal_places=2) # 배송비
  currency_id = models.IntegerField(default=1)   #화폐 단위
  link = models.CharField(max_length=255)
  image_url = models.CharField(max_length=255)