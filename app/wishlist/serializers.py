from product.serializers import ProductSerializer
from rest_framework.serializers import ModelSerializer, UniqueTogetherValidator
from wishlist.models import Wishlist


class WishlistSerializer(ModelSerializer):

    def to_representation(self, instance):
        return {
            'id': instance.id,
            'product_id': str(instance.product_id),
            'product':  ProductSerializer(instance.product).data
        }
    class Meta:
        model = Wishlist
        fields = '__all__'

        extra_kwargs = {'user': {'write_only': True}}

        validators = [
            UniqueTogetherValidator(
                queryset=model.objects.all(),
                fields=('user', 'product'),
                message="User already have a wishlist item with this product id."
            )
        ]
