from django.contrib.auth import get_user_model
from rest_framework.test import APIClient, APITestCase

User = get_user_model()


class TestWishlist(APITestCase):

    # TODO Mock the  PRODUCT_API.retrieve_product_details(product_id)
    @classmethod
    def setUpClass(cls):
        cls.client = APIClient()
        cls.user = User.objects.create(
            username='test_user',
            email='test_user@test.com',
        )
        return super().setUpClass()

    def test_add_product_to_user_wishlist_success(self):
        # TODO In progress
        product_id = '1bf0f365-fbdd-4e21-9786-da459d78dd1f'

        response = self.client.post(
            '/wishlist',
            data={'product_id': product_id},
            format='json'
        )

        self.assertEqual(response.status_code, 201)

    def test_add_product_to_user_wishlist_error__product_already_in_list(self):
        pass

    def test_add_product_to_user_wishlist_error__invalid_product(self):
        pass

    def test_get_user_wishlist(self):
        pass

    def test_get_user_wishlist_item(self):
        # sub test for item with review
        pass
