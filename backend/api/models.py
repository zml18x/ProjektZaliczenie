from django.db import models
from django.utils import timezone

class Currency(models.Model):
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=3, unique=True)
    country = models.CharField(max_length=100, blank=True, null=True)

class CurrencyRate(models.Model):
    currency = models.ForeignKey('Currency', on_delete=models.CASCADE)
    rate_date = models.DateField(default=timezone.now)
    rate = models.DecimalField(max_digits=10, decimal_places=4)