from django.db import models

# Create your models here.
class Search(models.Model):
  id = models.AutoField(primary_key=True)
  search_url = models.URLField(max_length=500)
  image_url = models.URLField(null=True)
  name = models.CharField(max_length=500)
  keyword = models.CharField(max_length=500, null=True)
  category_id = models.IntegerField(default=0)
  price = models.IntegerField()
  delivery_charge = models.IntegerField(default=0)
  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now=True)
  is_deleted = models.BooleanField(default=False)
