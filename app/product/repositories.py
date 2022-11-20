from typing import TypedDict, Optional

from luiza_labs.client import LuizaLabsClient, ClientError

from .models import ProductManager
from .serializers import ProductSerializer


class Product(TypedDict):
    id: str
    price: float
    image: str
    brand: str
    title: str
    reviewScore: Optional[float]


class InvalidProductId(Exception):
    pass


class ProductRepotory:
    luiza_client = LuizaLabsClient()
    product_dao = ProductManager

    @classmethod
    def _get_product_by_id(cls, id, source='external')-> Product:
        get_from={
            'external': cls.luiza_client.retrieve_product_details(id).__dict__,
            'internal': ProductSerializer(cls.product_dao.get(id=id)).data
        }
        return get_from[source]

    @classmethod
    def get_by_id(cls, id: str)-> Product:
        try:
            return cls._get_product_by_id(id, source='external')
        except ClientError as e:
            raise InvalidProductId(f'Invalid id for product: {e}')
