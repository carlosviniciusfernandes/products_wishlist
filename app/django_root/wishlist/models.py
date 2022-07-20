from typing import Optional

from django.conf import settings
from django.db import models
from luiza_labs.client import LuizaLabsClient
from luiza_labs.models import Product


class Wishlist(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    product_id = models.CharField(unique=True, null=False)

    _product_data: Optional[Product] = None

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

        self.client: Optional[LuizaLabsClient] = kwargs.get('client')

    @property
    def product_data(self):
        if self.client:
            self._product_data = self.client.retrieve_product_details(self.id)

        return self._product_data

    class Meta:
        db_table = 'wishlist'
