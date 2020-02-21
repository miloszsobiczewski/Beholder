from django.db import models


class Usage(models.Model):
    date = models.DateField(auto_now_add=True)
    amount = models.DecimalField(max_digits=8, decimal_places=2)


class Config(models.Model):
    key = models.CharField(max_length=16)
    value = models.CharField(max_length=65)
