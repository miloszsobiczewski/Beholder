from django.utils import timezone
from django.contrib import admin

from moneyball.models import Upcoming, MoneyBall


@admin.register(Upcoming)
class UpcomingAdmin(admin.ModelAdmin):
    model = Upcoming
    list_display = ("hex_hash", "time_to_run", "last_run", "timestamp")
    ordering = ("timestamp",)

    def time_to_run(self, obj):
        return obj.timestamp - timezone.now()


@admin.register(MoneyBall)
class MoneyBallAdmin(admin.ModelAdmin):
    model = MoneyBall
    list_display = ("hex_hash", "crated", "json_file")
