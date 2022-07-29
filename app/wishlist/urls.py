from rest_framework import routers
from wishlist.views import WishlistViewSet

router = routers.SimpleRouter(trailing_slash=False)
router.register(r'wishlist', WishlistViewSet)
