from django.db import models

# Create your models here.
class Wallet(models.Model):
    cup = models.IntegerField()
    mlc = models.IntegerField()
    usd = models.IntegerField()