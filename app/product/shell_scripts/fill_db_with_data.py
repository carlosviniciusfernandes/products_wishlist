from product.models import Product

from luiza_labs.client import LuizaLabsClient
from luiza_labs.models import Product as LuizaProduct

client = LuizaLabsClient()

raw_products:list[LuizaProduct] = client.list_products(1)

products_to_save:list[Product] = [Product(**product.__dict__) for product in raw_products]

Product.objects.bulk_create(products_to_save)
