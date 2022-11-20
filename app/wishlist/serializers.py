from rest_framework.exceptions import ValidationError
from rest_framework.serializers import ModelSerializer, UniqueTogetherValidator
from wishlist.models import Wishlist
from product.repositories import ProductRepository


class WishlistSerializer(ModelSerializer):

    def validate_product_id(self, value):
        try:
            return ProductRepository.get_by_id(value).get('id')
        except Exception as e:
            raise ValidationError(str(e))

    def to_representation(self, instance):
        return {
            'id': instance.id,
            'product_id': str(instance.product_id),
            'product':  ProductRepository.get_by_id(instance.product_id)
        }
    class Meta:
        model = Wishlist
        fields = '__all__'

        extra_kwargs = {'user': {'write_only': True}}

        validators = [
            UniqueTogetherValidator(
                queryset=model.objects.all(),
                # fields=('user', 'product'),
                fields=('user', 'product_id'),
                message="User already have a wishlist item with this product id."
            )
        ]
