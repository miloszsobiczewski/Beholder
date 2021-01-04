from django.contrib import admin, messages
from django.db import models
from django.forms import TextInput
from django.utils import timezone

from moneyball.models import MoneyBall, Upcoming
from moneyball.tasks import collect_moneyball, refresh_upcoming_model


def refresh_upcoming(modeladmin, request, queryset):
    refresh_upcoming_model.delay()
    messages.info(
        request, f"Upcoming refresh task is scheduled and will start in a second."
    )


def calculate_upcoming(modeladmin, request, queryset):
    collect_moneyball.delay()
    messages.info(
        request, f"Collect Monayball task is scheduled and will start in a second."
    )


refresh_upcoming.short_description = "Refresh Upcoming Model"
calculate_upcoming.short_description = "Collect MonayBall NOW!"


@admin.register(Upcoming)
class UpcomingAdmin(admin.ModelAdmin):
    model = Upcoming
    list_display = (
        "hex_hash",
        "sport_key",
        "teams",
        "time_to_run",
        "last_run",
        "timestamp",
    )
    ordering = ("timestamp",)
    actions = (refresh_upcoming, calculate_upcoming)

    def time_to_run(self, obj):
        return obj.timestamp - timezone.now()


@admin.register(MoneyBall)
class MoneyBallAdmin(admin.ModelAdmin):
    formfield_overrides = {models.CharField: {"widget": TextInput(attrs={"size": "5"})}}
    model = MoneyBall
    search_fields = ("sport_key", "teams")
    readonly_fields = ("created",)
    list_editable = ("result",)
    ordering = ("-timestamp",)
    list_display = (
        "hex_hash",
        "teams",
        "result",
        "sport_key",
        "timestamp",
        "json_file",
        "created",
    )
    list_per_page = 20
