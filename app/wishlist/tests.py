from unittest.mock import Mock, patch

from django.contrib.auth import get_user_model
from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient, APITestCase
from wishlist.models import Wishlist, PRODUCT_API

User = get_user_model()


def create_test_user() -> User:
    user = User.objects.create(
        username='test_user',
        email='test_user@test.com',
    )
    return user


def get_user_token(user: User) -> Token.key:
    token, created = Token.objects.get_or_create(user=user)
    return f"Token {token.key}"


class TestWishlist(APITestCase):

    @classmethod
    def setUpClass(cls):
        cls.client = APIClient()
        cls.user = create_test_user()
        cls.headers = {
            'HTTP_AUTHORIZATION': get_user_token(cls.user)
        }
        return super().setUpClass()

    @patch.object(PRODUCT_API, 'retrieve_product_details')
    def test_add_product_to_user_wishlist_success(self, mock_get_product_data: Mock):
        product_id = '1bf0f365-fbdd-4e21-9786-da459d78dd1f'
        mock_get_product_data.return_value = Mock(product_id=product_id)

        response = self.client.post(
            '/wishlist',
            data={'product_id': product_id},
            format='json',
            **self.headers
        )

        self.assertEqual(response.status_code, 201)

    @patch.object(PRODUCT_API, 'retrieve_product_details')
    def test_add_product_to_user_wishlist_error__product_already_in_list(self, mock_get_product_data: Mock):
        product_id = '1bf0f365-fbdd-4e21-9786-da459d78dd1f'
        Wishlist.objects.create(user=self.user, product_id=product_id)
        mock_get_product_data.return_value = Mock(product_id=product_id)

        response = self.client.post(
            '/wishlist',
            data={'product_id': product_id},
            format='json',
            **self.headers
        )

        self.assertEqual(response.status_code, 400)
        self.assertIn('User already have a wishlist item with this product id.', str(response.data))

    @patch.object(PRODUCT_API, 'retrieve_product_details')
    def test_add_product_to_user_wishlist_error__invalid_product(self, mock_get_product_data: Mock):
        product_id = 'random_invalid_product_id'
        mock_get_product_data.side_effect = Exception

        response = self.client.post(
            '/wishlist',
            data={'product_id': product_id},
            format='json',
            **self.headers
        )

        self.assertEqual(response.status_code, 400)
        self.assertIn('Could not validate product id.', response.json().get('product_id'))

    def test_get_user_wishlist(self):
        pass

    def test_get_user_wishlist_item(self):
        # sub test for item with review
        pass
