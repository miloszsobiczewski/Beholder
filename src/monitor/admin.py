from django.contrib import admin
from .models import Config, Usage


@admin.register(Config)
class ConfigAdmin(admin.ModelAdmin):
    model = Config
    list_display = ["key", "value"]


@admin.register(Usage)
class UsageAdmin(admin.ModelAdmin):
    model = Usage
    list_display = ["date", "amount"]
