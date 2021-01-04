from django.contrib import admin

from .models import Config, ExchangeRate, Usage


@admin.register(Config)
class ConfigAdmin(admin.ModelAdmin):
    model = Config
    list_display = ["key", "value"]


@admin.register(Usage)
class UsageAdmin(admin.ModelAdmin):
    model = Usage
    list_display = ["date", "amount"]


@admin.register(ExchangeRate)
class ExchangeRateAdmin(admin.ModelAdmin):
    model = ExchangeRate
    list_display = ["date", "mid_gbp_exchange_rate", "mid_usd_exchange_rate"]
