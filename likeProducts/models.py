from django.db import models
from accounts.models import Account


# Create your models here.
class LikeProduct(models.Model):
  id = models.AutoField(primary_key=True)
  user = models.ForeignKey(Account, on_delete=models.CASCADE)
  name = models.CharField(max_length=100)
  price = models.IntegerField()
  delivery_charge = models.IntegerField(default=0)
  link = models.URLField()
  image_url = models.URLField()
  category_id = models.IntegerField()
  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now=True)
  is_deleted = models.BooleanField(default=False)