from rest_framework.serializers import (ModelSerializer, SerializerMethodField,
                                        UniqueTogetherValidator,
                                        ValidationError)
from wishlist.models import Wishlist


class WishlistSerializer(ModelSerializer):
    product = SerializerMethodField()

    def validate_product_id(self, value: str):
        try:
            Wishlist._get_product_data(value)
            return value
        except Exception:
            raise ValidationError('Could not validate product id.')

    def get_product(self, instance: Wishlist) -> dict:
        return instance.product_data.__dict__

    class Meta:
        model = Wishlist
        fields = '__all__'

        extra_kwargs = {'user': {'write_only': True}}

        validators = [
            UniqueTogetherValidator(
                queryset=model.objects.all(),
                fields=('user', 'product_id'),
                message="User already have a wishlist item with this product id."
            )
        ]
