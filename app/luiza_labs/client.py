from typing import List

import requests

from .models import Product


class ClientError(Exception):
    pass


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

    def __enter__(self):  # TODO compose this in a request context manager class
        ...

    def __exit__(self, exc_type, exc_val, tracaback):
        if isinstance(exc_val, requests.exceptions.HTTPError):
            if exc_val.response.status_code == 404:
                raise ClientError('Resource was not found, 404 returned')
            else:
                raise ClientError('Unexpected error for requested resource')

    def list_products(self, page: int) -> List[Product]:
        url = f'{self.API_BASE_URL}?page={page}'

        with self:
            response = self.session.get(url)
            response.raise_for_status()

        items = response.json().get("products", [])
        return [Product(**item) for item in items]

    def retrieve_product_details(self, id: str):
        # if the id is an integer, the request will be equivalent as list_products
        if str(id).isnumeric():
            raise ValueError('Invalid id for product')

        url = f'{self.API_BASE_URL}{id}/'
        with self:
            response = self.session.get(url)
            response.raise_for_status()

        item = response.json()
        return Product(**item)
