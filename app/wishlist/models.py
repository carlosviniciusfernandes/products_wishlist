from typing import Optional

from django.conf import settings
from django.db import models
from luiza_labs.client import LuizaLabsClient
from luiza_labs.models import Product

PRODUCT_API = LuizaLabsClient()


class Wishlist(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    product_id = models.CharField(null=False, max_length=256)

    # TODO make user_id and product_id unique together
    # (currently only product_id is unique, which is problem to add the same item do another user wishlist)

    _product_data: Optional[Product] = None

    @staticmethod
    def _get_product_data(product_id: str) -> Product:
        return PRODUCT_API.retrieve_product_details(product_id)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self._product_data = self._get_product_data(self.product_id)

    @property
    def product_data(self):
        return self._get_product_data(self.product_id)

    class Meta:
        db_table = 'wishlist'
        unique_together = ['user', 'product_id']
