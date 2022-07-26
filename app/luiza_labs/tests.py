from unittest import TestCase
from unittest.mock import Mock

import requests
from luiza_labs.client import ClientError, LuizaLabsClient
from luiza_labs.models import Product


class TestLuizaLabsClient(TestCase):

    @classmethod
    def setUpClass(cls):
        cls.client = LuizaLabsClient()

        cls.mock_product_one = {
            "price": 1699.0,
            "image": "http://challenge-api.luizalabs.com/images/1bf0f365-fbdd-4e21-9786-da459d78dd1f.jpg",
            "brand": "bébé confort",
            "id": "1bf0f365-fbdd-4e21-9786-da459d78dd1f",
            "title": "Cadeira para Auto Iseos Bébé Confort Earth Brown"
        }

        cls.mock_product_two = {
            "reviewScore": 4.352941,
            "title": "Churrasqueira Elétrica Mondial 1800W",
            "price": 159.0,
            "brand": "mondial",
            "id": "571fa8cc-2ee7-5ab4-b388-06d55fd8ab2f",
            "image": "http://challenge-api.luizalabs.com/images/571fa8cc-2ee7-5ab4-b388-06d55fd8ab2f.jpg"
        }

        cls.mock_list_products_response_data = {
            'products': [cls.mock_product_one, cls.mock_product_two]
        }

        return super().setUpClass()

    def setUp(self):
        self.client.session = Mock()
        return super().setUp()

    def test_list_products_success(self):
        mock_response_data = self.mock_list_products_response_data
        self.client.session.get.return_value.json.return_value = mock_response_data

        products_list = self.client.list_products(1)

        self.assertIsInstance(products_list, list)
        self.assertEqual(len(products_list), len(self.mock_list_products_response_data['products']))

        for key, value in self.mock_product_one.items():
            self.assertIsInstance(products_list[0], Product)
            self.assertEqual(products_list[0].__dict__[key], value)

        for key, value in self.mock_product_two.items():
            self.assertIsInstance(products_list[1], Product)
            self.assertEqual(products_list[1].__dict__[key], value)

    def test_list_products_error__page_not_found(self):
        mock_response = Mock(status_code=404)
        mock_response.raise_for_status.side_effect = requests.exceptions.HTTPError(
            response=mock_response
        )
        self.client.session.get.return_value = mock_response

        with self.assertRaises(ClientError) as context:
            self.client.list_products('1234567')
        self.assertEqual(str(context.exception), 'Resource was not found, 404 returned')

    def test_retrive_product_details_success(self):
        for case, mock_product in {
            'product_without_score': self.mock_product_one,
            'product_with_score': self.mock_product_two,
        }.items():
            with self.subTest(case):
                mock_response_data = mock_product
                self.client.session.get.return_value.json.return_value = mock_response_data

                product_detailed = self.client.retrieve_product_details(mock_product.get('id'))

                for key, value in mock_product.items():
                    self.assertIsInstance(product_detailed, Product)
                    self.assertEqual(product_detailed.__dict__[key], value)

    def test_retrive_product_defatils_error__invalid_id_format(self):
        with self.assertRaises(ValueError) as context:
            self.client.retrieve_product_details('1234')
        self.assertEqual(str(context.exception), 'Invalid id for product')

    def test_retrive_product_defatils_error__product_not_found(self):
        mock_response = Mock(status_code=404)
        mock_response.raise_for_status.side_effect = requests.exceptions.HTTPError(
            response=mock_response
        )
        self.client.session.get.return_value = mock_response

        with self.assertRaises(ClientError) as context:
            self.client.retrieve_product_details('some_random_product_id_that_wont_work')
        self.assertEqual(str(context.exception), 'Resource was not found, 404 returned')

    def test_unexpected_error_from_product_api(self):
        product_id = self.mock_product_one.get('id')

        for status in [400, 408, 418, 429, 500, 503, 504]:
            with self.subTest(status):
                mock_response = Mock(status_code=status)
                mock_response.raise_for_status.side_effect = requests.exceptions.HTTPError(
                    response=mock_response
                )
                self.client.session.get.return_value = mock_response

                with self.assertRaises(ClientError) as context:
                    self.client.retrieve_product_details(product_id)
                self.assertEqual(str(context.exception), 'Unexpected error for requested resource')
