from django.db import models

class Wallet(models.Model):
    cup = models.IntegerField()
    mlc = models.IntegerField()
    usd = models.IntegerField()

class TransactionType(models.TextChoices):
    SELL = 'sell', 'Sell'
    SHOP = 'shop', 'Shop'

class Transaction(models.Model):
    wallet = models.ForeignKey(Wallet, on_delete=models.CASCADE)
    inputCurrency = models.FloatField()
    outputCurrency = models.FloatField()
    moneyEntryType = models.CharField(max_length=3)
    moneyExitType = models.CharField(max_length=3)
    type = models.CharField(max_length=4, choices=TransactionType.choices)
    date = models.DateTimeField(auto_now_add=True)

    def _update_wallet_balance(self, currency_type, amount):
        if currency_type == 'USD':
            self.wallet.usd += amount
        elif currency_type == 'CUP':
            self.wallet.cup += amount
        elif currency_type == 'MLC':
            self.wallet.mlc += amount

    def save(self, *args, **kwargs):
        if self.type == TransactionType.SELL:
            self._update_wallet_balance(self.moneyEntryType, -self.inputCurrency)
            self._update_wallet_balance(self.moneyExitType, self.outputCurrency)
        elif self.type == TransactionType.SHOP:
            self._update_wallet_balance(self.moneyExitType, -self.outputCurrency)
            self._update_wallet_balance(self.moneyEntryType, self.inputCurrency)

        self.wallet.save()
        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        # Revertir la operación de la transacción antes de eliminarla
        if self.type == TransactionType.SELL:
            # Invertir las operaciones realizadas en save
            self._update_wallet_balance(self.moneyEntryType, self.inputCurrency)
            self._update_wallet_balance(self.moneyExitType, -self.outputCurrency)
        elif self.type == TransactionType.SHOP:
            # Invertir las operaciones realizadas en save
            self._update_wallet_balance(self.moneyExitType, self.outputCurrency)
            self._update_wallet_balance(self.moneyEntryType, -self.inputCurrency)

        # Guardar los cambios en la wallet antes de eliminar la transacción
        self.wallet.save()

        # Llamar al método delete original para eliminar la transacción
        super().delete(*args, **kwargs)