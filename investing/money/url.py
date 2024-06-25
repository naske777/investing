from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .api import WalletViewSet

router = DefaultRouter()
router.register(r'wallets', WalletViewSet)

urlpatterns = [
    path('', include(router.urls)),
]