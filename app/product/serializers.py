from rest_framework.serializers import ModelSerializer
from rest_framework.exceptions import ValidationError

from .models import Product


class ProductSerializer(ModelSerializer):

   def validate_reviewScore(self, value):
      if value is not None or (value < 0 or value > 5):
         raise ValidationError('A product must have a review score between 0.0 and 5.0')

      return value

   class Meta:
      model = Product
      fields = '__all__'
