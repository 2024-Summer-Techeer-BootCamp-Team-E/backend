from django.db import models

from search.models import Search


# Create your models here.

class Product(models.Model):
  id = models.AutoField(primary_key=True)  #
  search = models.ForeignKey(Search, on_delete=models.CASCADE)
  product_name = models.CharField(max_length=100)
  category_id = models.IntegerField() #카테고리 아이디
  price = models.DecimalField(max_digits=10, decimal_places=2)  #가격
  delivery_charge = models.DecimalField(max_digits=10, decimal_places=2, default=0) # 배송비
  link = models.URLField()
  image_url = models.URLField()
  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now=True)
  is_deleted = models.BooleanField(default=False)

  def __str__(self):
    return self.product_name
