from unittest.mock import Mock, patch

from django.contrib.auth import get_user_model
from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient, APITestCase
from wishlist.models import PRODUCT_API, Wishlist

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

    product_id = '1bf0f365-fbdd-4e21-9786-da459d78dd1f'

    product_data = {
        "price": 1699.0,
        "image": "http://challenge-api.luizalabs.com/images/1bf0f365-fbdd-4e21-9786-da459d78dd1f.jpg",
        "brand": "bébé confort",
        "id": "1bf0f365-fbdd-4e21-9786-da459d78dd1f",
        "title": "Cadeira para Auto Iseos Bébé Confort Earth Brown",
        "reviewScore": 3.98
    }

    @classmethod
    def setUpClass(cls):
        cls.client = APIClient()
        cls.user = create_test_user()
        cls.headers = {
            'HTTP_AUTHORIZATION': get_user_token(cls.user)
        }
        return super().setUpClass()

    def test_add_product_to_user_wishlist_success(self, mock_get_product_data: Mock):
        product_id = self.product_id
        mock_get_product_data.return_value = Mock(product_id=product_id)

        response = self.client.post(
            '/wishlist',
            data={'product_id': product_id},
            format='json',
            **self.headers
        )

        self.assertEqual(response.status_code, 201)

    def test_add_product_to_user_wishlist_error__product_already_in_list(self, mock_get_product_data: Mock):
        product_id = self.product_id
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

    def test_get_user_wishlist__empty_list(self, mock_get_product_data: Mock):
        response = self.client.get(
            '/wishlist',
            format='json',
            **self.headers
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 0)

    def test_get_user_wishlist__list_has_only_current_user_items(self, mock_get_product_data: Mock):
        product_id = self.product_id
        other_product_id = '6a512e6c-6627-d286-5d18-583558359ab6'
        another_product_id = '4bd442b1-4a7d-2475-be97-a7b22a08a024'
        mock_get_product_data.return_value.__dict__ = {}

        # Add item to test user wishlist
        Wishlist.objects.create(user=self.user, product_id=product_id)
        Wishlist.objects.create(user=self.user, product_id=other_product_id)

        # Add item to other user wishlist , should not return together with test user items
        other_user = create_test_user('other_test_user')
        Wishlist.objects.create(user=other_user, product_id=another_product_id)

        response = self.client.get(
            '/wishlist',
            format='json',
            **self.headers
        )

        self.assertEqual(response.status_code, 200)

        # only test user wishlist items
        self.assertEqual(len(response.data), 2)
        self.assertEqual([item.get('product_id') for item in response.data], [product_id, other_product_id])

        # All wishlist items
        self.assertEqual(Wishlist.objects.all().count(), 3)

    def test_get_user_wishlist__list_filtered_items(self, mock_get_product_data: Mock):
        product_id = self.product_id
        other_product_id = '6a512e6c-6627-d286-5d18-583558359ab6'
        mock_get_product_data.return_value.__dict__ = {}

        # Add item to test user wishlist
        Wishlist.objects.create(user=self.user, product_id=product_id)
        Wishlist.objects.create(user=self.user, product_id=other_product_id)

        # TODO create subtest for the different lookup expression of the different fields
        response = self.client.get(
            '/wishlist?product_id__icontains=1bf0f365',
            format='json',
            **self.headers
        )

        self.assertEqual(response.status_code, 200)

        # list has only the filtered wishlist item(s)
        self.assertEqual(len(response.data), 1)

    def test_get_user_wishlist_item_success(self, mock_get_product_data: Mock):
        product_id = self.product_id
        mock_get_product_data.return_value.__dict__ = self.product_data

        wishlist_item = Wishlist.objects.create(user=self.user, product_id=product_id)

        response = self.client.get(
            f'/wishlist/{wishlist_item.id}',
            format='json',
            **self.headers
        )

        expected_data = {
            'id': wishlist_item.id,
            'product_id': f'{wishlist_item.product_id}',
            'product': self.product_data
        }

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, expected_data)

    def test_get_user_wishlist_item_error__not_found(self, mock_get_product_data: Mock):
        other_user = create_test_user('other_test_user')
        product_id = self.product_id
        wishlist_item = Wishlist.objects.create(user=other_user, product_id=product_id)

        response = self.client.get(
            f'/wishlist/{wishlist_item.id}',
            format='json',
            **self.headers
        )

        self.assertEqual(response.status_code, 404)

    def test_delete_user_wishlist_item_success(self, *args):
        product_id = self.product_id
        wishlist_item = Wishlist.objects.create(user=self.user, product_id=product_id)

        response = self.client.delete(
            f'/wishlist/{wishlist_item.id}',
            format='json',
            **self.headers
        )

        self.assertEqual(response.status_code, 204)

    def test_delete_user_wishlist_item_error__not_found(self, *args):
        other_user = create_test_user('other_test_user')
        product_id = self.product_id
        wishlist_item = Wishlist.objects.create(user=other_user, product_id=product_id)

        response = self.client.delete(
            f'/wishlist/{wishlist_item.id}',
            format='json',
            **self.headers
        )

        self.assertEqual(response.status_code, 404)

    def test_update_wishlist_item_not_allowed(self, *args):
        response = self.client.put(
            f'/wishlist/random_id',
            format='json',
            data={'random_data': 'to be updated'},
            **self.headers
        )

        self.assertEqual(response.status_code, 405)

    def test_partial_update_wishlist_item_not_allowed(self, *args):
        response = self.client.patch(
            f'/wishlist/random_id',
            format='json',
            data={'random_data': 'to be partially updated'},
            **self.headers
        )

        self.assertEqual(response.status_code, 405)
