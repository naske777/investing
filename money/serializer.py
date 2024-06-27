from rest_framework import serializers
from .models import Wallet, Transaction

class WalletSerializer(serializers.ModelSerializer):
    class Meta:
        model = Wallet
        fields = '__all__'

class TransactionSerializer(serializers.ModelSerializer):
    date = serializers.DateTimeField(format="%d-%m-%Y")  

    class Meta:
        model = Transaction
        fields = '__all__'        