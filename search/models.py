from django.db import models

# Create your models here.
class Search(models.Model):
  id = models.AutoField(primary_key=True)
  search_url = models.URLField(max_length=500)
  name = models.CharField(max_length=500)
  price = models.DecimalField(max_digits=10, decimal_places=2)
  delivery_charge = models.DecimalField(max_digits=10, decimal_places=2)
  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now=True)
  is_deleted = models.BooleanField(default=False)
