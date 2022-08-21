from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from wishlist.models import Wishlist
from wishlist.serializers import WishlistSerializer

User = get_user_model()
"""
O dispositivo que irá renderizar a resposta fornecida por essa nova API irá
apresentar o Título, Imagem, Preço e irá utilizar o ID do produto para formatar
o link que ele irá acessar. Quando existir um review para o produto, o mesmo
será exibido por este dispositivo. Não é necessário criar um frontend para
simular essa renderização (foque no desenvolvimento da API).

"""


class WishlistViewSet(ModelViewSet):
    queryset = Wishlist.objects.all()
    serializer_class = WishlistSerializer

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
