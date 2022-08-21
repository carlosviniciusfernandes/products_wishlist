from rest_framework.serializers import (ModelSerializer,
                                        UniqueTogetherValidator,
                                        ValidationError)
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

        validators = [
            UniqueTogetherValidator(
                queryset=model.objects.all(),
                fields=('user', 'product_id'),
                message="User already have a wishlist item with this product id."
            )
        ]
