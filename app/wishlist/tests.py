from unittest.mock import Mock, patch

from django.contrib.auth import get_user_model
from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient, APITestCase
from wishlist.models import Wishlist, PRODUCT_API

User = get_user_model()


def create_test_user(username: str ='test_user') -> User:
    user = User.objects.create(
        username=username,
        email=f'{username}@test.com',
    )
    return user


def get_user_token(user: User) -> Token.key:
    token, created = Token.objects.get_or_create(user=user)
    return f"Token {token.key}"


@patch.object(PRODUCT_API, 'retrieve_product_details')
class TestWishlist(APITestCase):

    @classmethod
    def setUpClass(cls):
        cls.client = APIClient()
        cls.user = create_test_user()
        cls.headers = {
            'HTTP_AUTHORIZATION': get_user_token(cls.user)
        }
        return super().setUpClass()

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

    def test_add_product_to_user_wishlist_error__product_already_in_list(self, mock_get_product_data: Mock):
        product_id = '1bf0f365-fbdd-4e21-9786-da459d78dd1f'
        Wishlist.objects.create(user=self.user, product_id=product_id)

        response = self.client.post(
            '/wishlist',
            data={'product_id': product_id},
            format='json',
            **self.headers
        )

        self.assertEqual(response.status_code, 400)
        self.assertIn('User already have a wishlist item with this product id.', str(response.data))

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

    def test_get_user_wishlist(self, mock_get_product_data: Mock):
        other_user = create_test_user('other_test_user')
        product_ids = ['1bf0f365-fbdd-4e21-9786-da459d78dd1f', '6a512e6c-6627-d286-5d18-583558359ab6']
        for id in product_ids:
            # Add item to test user wishlist
            Wishlist.objects.create(user=self.user, product_id=id)
            # Add item to other user wishlist , should not return together with test user items
            Wishlist.objects.create(user=other_user, product_id=id)

        response = self.client.get(
            '/wishlist',
            format='json',
            **self.headers
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 2) # only test user wishlist items
        self.assertEqual(Wishlist.objects.all().count(), 4) # All wishlist items

    def test_get_user_wishlist_item(self, mock_get_product_data: Mock):
        product_id = '1bf0f365-fbdd-4e21-9786-da459d78dd1f'
        wishlist_item = Wishlist.objects.create(user=self.user, product_id=product_id)

        response = self.client.get(
            f'/wishlist/{wishlist_item.id}',
            format='json',
            **self.headers
        )

        expected_data = {
            'id': {wishlist_item.id},
            'product_id': f'{wishlist_item.product_id}'
        }

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, expected_data)

    def test_get_user_wishlist_item_error__not_found(self, mock_get_product_data: Mock):
        other_user = create_test_user('other_test_user')
        product_id = '1bf0f365-fbdd-4e21-9786-da459d78dd1f'
        wishlist_item = Wishlist.objects.create(user=other_user, product_id=product_id)

        response = self.client.get(
            f'/wishlist/{wishlist_item.id}',
            format='json',
            **self.headers
        )

        self.assertEqual(response.status_code, 404)
