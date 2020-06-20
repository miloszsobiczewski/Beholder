from django.utils import timezone
from django.contrib import admin, messages

from moneyball.models import Upcoming, MoneyBall
from moneyball.tasks import refresh_upcoming_model, collect_moneyball


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
    list_display = ("hex_hash", "time_to_run", "last_run", "timestamp")
    ordering = ("timestamp",)
    actions = (refresh_upcoming, calculate_upcoming)

    def time_to_run(self, obj):
        return obj.timestamp - timezone.now()


@admin.register(MoneyBall)
class MoneyBallAdmin(admin.ModelAdmin):
    model = MoneyBall
    list_display = ("hex_hash", "crated", "json_file")
