from django.contrib.auth import get_user_model
from rest_framework import status
from django_filters import rest_framework as filters
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from wishlist.models import Wishlist
from wishlist.serializers import WishlistSerializer

User = get_user_model()


class WishlistViewSet(ModelViewSet):
    queryset = Wishlist.objects.all()
    serializer_class = WishlistSerializer
    filter_backends = [filters.DjangoFilterBackend]
    filterset_fields = {
        'id': ['exact', 'in'],
        'product_id': ['exact', 'in', 'icontains']
    }

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)

    def create(self, request):
        user = request.user
        serializer: WishlistSerializer = self.get_serializer(
            data={'user': user.id, 'product_id': request.data.get('product_id')}
        )
        serializer.is_valid(raise_exception=True)
        serializer.create(serializer.validated_data)
        return Response(None, status=status.HTTP_201_CREATED)

    def update(self, *args, **kwargs):
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

    def patch(self, *args, **kwargs):
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
