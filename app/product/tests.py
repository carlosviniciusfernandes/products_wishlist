from product.serializers import ProductSerializer
from rest_framework.test import APITestCase


class TestProductSerializer(APITestCase):

    def test_add_product_error__reviewScore_out_of_range(self):
        product_data = {
            "price": 1699.0,
            "image": "http://challenge-api.luizalabs.com/images/1bf0f365-fbdd-4e21-9786-da459d78dd1f.jpg",
            "brand": "bébé confort",
            "id": "1bf0f365-fbdd-4e21-9786-da459d78dd1f",
            "title": "Cadeira para Auto Iseos Bébé Confort Earth Brown",
        }

        for case, value in {
            'negative': -1,
            'empty': '',
            'over_five': 5.1
        }.items():
            with self.subTest(case):
                serializer = ProductSerializer(data={ **product_data, 'reviewScore': value })
                self.assertFalse(serializer.is_valid())
