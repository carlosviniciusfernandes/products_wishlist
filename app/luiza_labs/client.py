from typing import List

import requests

from .models import Product


class LuizaLabsClient:

    API_BASE_URL = 'http://challenge-api.luizalabs.com/api/product/'

    def __init__(self):
        headers = {
            "Accept": "*",
            "Content-Type": "application/json",
        }
        session = requests.session()
        session.headers.update(headers)
        self.session = session

    def list_products(self, page: int) -> List[Product]:
        url = f'{self.API_BASE_URL}?page={page}'
        response = self.session.get(url)
        response.raise_for_status()

        items = response.json().get("products", [])
        return [Product(**item) for item in items]

    def retrieve_product_details(self, id):
        url = f'{self.API_BASE_URL}{id}/'
        response = self.session.get(url)
        response.raise_for_status()

        item = response.json()
        return Product(**item)
