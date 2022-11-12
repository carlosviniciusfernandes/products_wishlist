from django.conf import settings
from django.db import models
from product.models import Product


class Wishlist(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.PROTECT)
    class Meta:
        db_table = 'wishlist'
        unique_together = ['user', 'product']
