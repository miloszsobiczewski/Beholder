from django.db import models


class Usage(models.Model):
    date = models.DateField(auto_now_add=True)
    amount = models.DecimalField(max_digits=8, decimal_places=2)


class Config(models.Model):
    key = models.CharField(max_length=16)
    value = models.CharField(max_length=256)


class ExchangeRate(models.Model):
    date = models.DateTimeField(auto_now_add=True)
    buy_gbp = models.DecimalField(
        max_digits=4, decimal_places=2, null=True, blank=True, verbose_name="Buy GBP"
    )
    mid_gbp = models.DecimalField(
        max_digits=4, decimal_places=2, null=True, blank=True, verbose_name="Mid GBP"
    )
    sell_gbp = models.DecimalField(
        max_digits=4, decimal_places=2, null=True, blank=True, verbose_name="Sell GBP"
    )
    buy_usd = models.DecimalField(
        max_digits=4, decimal_places=2, null=True, blank=True, verbose_name="Buy USD"
    )
    mid_usd = models.DecimalField(
        max_digits=4, decimal_places=2, null=True, blank=True, verbose_name="Mid USD"
    )
    sell_usd = models.DecimalField(
        max_digits=4, decimal_places=2, null=True, blank=True, verbose_name="Sell USD"
    )
