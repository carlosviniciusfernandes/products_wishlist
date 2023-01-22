from django.conf import settings
from django.db import models

class Wishlist(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    product_id = models.CharField(null=False, default=None, max_length=255)

    class Meta:
        db_table = 'wishlist'
        unique_together = ['user', 'product_id']
