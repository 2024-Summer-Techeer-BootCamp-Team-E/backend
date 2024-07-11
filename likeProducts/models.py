from django.db import models
from accounts.models import Account
from products.models import Product


# Create your models here.
class LikeProduct(models.Model):
  id = models.AutoField(primary_key=True)
  user = models.ForeignKey(Account, on_delete=models.CASCADE)
  product = models.ForeignKey(Product, on_delete=models.CASCADE)
  product_number = models.IntegerField()
  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now=True)
  is_deleted = models.BooleanField(default=False)