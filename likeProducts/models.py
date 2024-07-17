from django.db import models
from accounts.models import Account
from products.models import Product


# Create your models here.
class LikeProduct(models.Model):
  id = models.AutoField(primary_key=True)
  user = models.ForeignKey(Account, on_delete=models.CASCADE)
  name = models.CharField(max_length=100)
  price = models.DecimalField(max_digits=10, decimal_places=2)
  delivery_charge = models.DecimalField(max_digits=10, decimal_places=2, default=0)
  link = models.URLField()
  image_url = models.URLField()
  category_id = models.IntegerField()
  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now=True)
  is_deleted = models.BooleanField(default=False)