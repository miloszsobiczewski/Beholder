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
    readonly_fields = ("date",)
    list_display = [
        "date",
        "buy_gbp",
        "mid_gbp",
        "sell_gbp",
        "buy_usd",
        "mid_usd",
        "sell_usd",
    ]
