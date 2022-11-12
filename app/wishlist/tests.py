from django.contrib.auth import get_user_model
from product.models import Product
from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient, APITestCase
from wishlist.models import Wishlist

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


class TestWishlist(APITestCase):


    @classmethod
    def setUpTestData(cls):
        cls.product_id = '1bf0f365-fbdd-4e21-9786-da459d78dd1f'
        Product.objects.create(**{
            "price": 1699.0,
            "image": "http://challenge-api.luizalabs.com/images/1bf0f365-fbdd-4e21-9786-da459d78dd1f.jpg",
            "brand": "bébé confort",
            "id": "1bf0f365-fbdd-4e21-9786-da459d78dd1f",
            "title": "Cadeira para Auto Iseos Bébé Confort Earth Brown",
            "reviewScore": 3.98
        })
        cls.other_product_id = '6a512e6c-6627-d286-5d18-583558359ab6'
        Product.objects.create(**{
            "price": 1149.0,
            "image": "http://challenge-api.luizalabs.com/images/6a512e6c-6627-d286-5d18-583558359ab6.jpg",
            "brand": "bébé confort",
            "id": "6a512e6c-6627-d286-5d18-583558359ab6",
            "title": "Moisés Dorel Windoo 1529",
            "reviewScore": 4.98
        })
        cls.another_product_id = '4bd442b1-4a7d-2475-be97-a7b22a08a024'
        Product.objects.create(**{
            "price": 1999.0,
            "image": "http://challenge-api.luizalabs.com/images/4bd442b1-4a7d-2475-be97-a7b22a08a024.jpg",
            "brand": "bébé confort",
            "id": "4bd442b1-4a7d-2475-be97-a7b22a08a024",
            "title": "Cadeira para Auto Axiss Bébé Confort Robin Red"
        })

    @classmethod
    def setUpClass(cls):
        cls.client = APIClient()
        cls.user = create_test_user()
        cls.headers = {
            'HTTP_AUTHORIZATION': get_user_token(cls.user)
        }
        return super().setUpClass()

    def test_add_product_to_user_wishlist_success(self):
        product_id = self.product_id

        response = self.client.post(
            '/wishlist',
            data={'product_id': product_id},
            format='json',
            **self.headers
        )

        self.assertEqual(response.status_code, 201)

    def test_add_product_to_user_wishlist_error__product_already_in_list(self):
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

    def test_add_product_to_user_wishlist_error__invalid_product(self):
        product_id = 'random_invalid_product_id'

        response = self.client.post(
            '/wishlist',
            data={'product_id': product_id},
            format='json',
            **self.headers
        )

        self.assertEqual(response.status_code, 400)

    def test_get_user_wishlist__empty_list(self):
        response = self.client.get(
            '/wishlist',
            format='json',
            **self.headers
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 0)

    def test_get_user_wishlist__list_has_only_current_user_items(self):
        product_id = self.product_id
        other_product_id = self.other_product_id
        another_product_id = self.another_product_id

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

    def test_get_user_wishlist__list_filtered_items(self):
        product_id = self.product_id
        other_product_id = self.other_product_id
        another_product_id = self.another_product_id

        # Add item to test user wishlist
        Wishlist.objects.create(user=self.user, product_id=product_id)
        Wishlist.objects.create(user=self.user, product_id=other_product_id)
        Wishlist.objects.create(user=self.user, product_id=another_product_id)

        for case, result in {
            f'product_id={product_id}': [product_id],
            f'product_id__in={product_id},{another_product_id}': [product_id, another_product_id],
            'product__reviewScore__lte=4': [product_id],
            'product__reviewScore__gte=4': [other_product_id],
            'product__title__icontains=Robin Red': [another_product_id]
        }.items():
            with self.subTest(case):
                response = self.client.get(
                    f'/wishlist?{case}',
                    format='json',
                    **self.headers
                )

                # list has only the filtered wishlist item(s)
                self.assertEqual(response.status_code, 200)
                self.assertEqual([item.get('product_id') for item in response.data], result)


    def test_get_user_wishlist_item_success(self):
        product_id = self.product_id

        wishlist_item = Wishlist.objects.create(user=self.user, product_id=product_id)

        response = self.client.get(
            f'/wishlist/{wishlist_item.id}',
            format='json',
            **self.headers
        )

        expected_data = {
            'id': wishlist_item.id,
            'product_id': product_id,
        }

        self.assertEqual(response.status_code, 200)
        self.assertTrue(expected_data.items() <= response.data.items())

    def test_get_user_wishlist_item_error__not_found(self):
        other_user = create_test_user('other_test_user')
        product_id = self.product_id
        wishlist_item = Wishlist.objects.create(user=other_user, product_id=product_id)

        response = self.client.get(
            f'/wishlist/{wishlist_item.id}',
            format='json',
            **self.headers
        )

        self.assertEqual(response.status_code, 404)

    def test_delete_user_wishlist_item_success(self):
        product_id = self.product_id
        wishlist_item = Wishlist.objects.create(user=self.user, product_id=product_id)

        response = self.client.delete(
            f'/wishlist/{wishlist_item.id}',
            format='json',
            **self.headers
        )

        self.assertEqual(response.status_code, 204)

    def test_delete_user_wishlist_item_error__not_found(self):
        other_user = create_test_user('other_test_user')
        product_id = self.product_id
        wishlist_item = Wishlist.objects.create(user=other_user, product_id=product_id)

        response = self.client.delete(
            f'/wishlist/{wishlist_item.id}',
            format='json',
            **self.headers
        )

        self.assertEqual(response.status_code, 404)

    def test_update_wishlist_item_not_allowed(self):
        response = self.client.put(
            f'/wishlist/random_id',
            format='json',
            data={'random_data': 'to be updated'},
            **self.headers
        )

        self.assertEqual(response.status_code, 405)

    def test_partial_update_wishlist_item_not_allowed(self):
        response = self.client.patch(
            f'/wishlist/random_id',
            format='json',
            data={'random_data': 'to be partially updated'},
            **self.headers
        )

        self.assertEqual(response.status_code, 405)
