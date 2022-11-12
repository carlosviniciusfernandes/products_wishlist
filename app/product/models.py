from uuid import uuid4
from django.db import models


class Product(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    price = models.FloatField(default=0.0)
    image = models.CharField(max_length=255)
    brand = models.CharField(max_length=32)
    title = models.TextField(max_length=255)
    reviewScore = models.FloatField(null=True, default=None)

    class Meta:
        db_table = 'product'
