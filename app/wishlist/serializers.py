from rest_framework.serializers import ModelSerializer, ValidationError
from wishlist.models import Wishlist


class WishlistSerializer(ModelSerializer):

    def validate_product_id(self, value):
        try:
            Wishlist._get_product_data(value)
            return value
        except Exception:
            raise ValidationError('Could not validate product id.')

    class Meta:
        model = Wishlist
        fields = '__all__'
