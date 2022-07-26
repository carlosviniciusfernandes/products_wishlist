from rest_framework.test import APITestCase, APIClient
from django.contrib.auth import get_user_model

from wishlist.models import Wishlist

User = get_user_model()

# Mock the  PRODUCT_API.retrieve_product_details(product_id)
# setup test user

class TestWishlist(APITestCase):

    @classmethod
    def setUpClass(cls):
        cls.client = APIClient()
        cls.user = User.objects.create(
            username='test_user',
            email='test_user@test.com',
        )
        return super().setUpClass()

    def test_add_product_to_user_wishlist_success(self):
        pass

    def test_add_product_to_user_wishlist_error__product_already_in_list(self):
        pass

    def test_add_product_to_user_wishlist_error__invalid_product(self):
        pass

    def test_get_user_wishlist(self):
        pass

    def test_get_user_wishlist_item(self):
        # sub test for item with review
        pass