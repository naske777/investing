from rest_framework import viewsets, status
from rest_framework.response import Response
from .models import *
from .serializer import *


class WalletViewSet(viewsets.ModelViewSet):
    queryset = Wallet.objects.all()
    serializer_class = WalletSerializer

class TransactionViewSet(viewsets.ModelViewSet):
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)

        # Obtén la instancia de la transacción para acceder a la wallet asociada
        transaction_instance = serializer.instance
        wallet_instance = transaction_instance.wallet

        # Utiliza WalletSerializer para serializar los datos de la wallet
        wallet_serializer = WalletSerializer(wallet_instance)

        # Devuelve los datos de la wallet en lugar de los de la transacción
        return Response(wallet_serializer.data, status=status.HTTP_201_CREATED, headers=headers)
    
    def destroy(self, request, *pk, **kwargs):
        transaction = self.get_object()
        wallet_instance = transaction.wallet
        transaction.delete()
        wallet_serializer = WalletSerializer(wallet_instance)
        return Response(wallet_serializer.data, status=status.HTTP_200_OK)