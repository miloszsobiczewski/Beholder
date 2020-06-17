from django.contrib import admin
from moneyball.models import Upcoming, MoneyBall


@admin.register(Upcoming)
class UpcomingAdmin(admin.ModelAdmin):
    model = Upcoming
    list_display = ("hex_hash", "last_run")


@admin.register(MoneyBall)
class MoneyBallAdmin(admin.ModelAdmin):
    model = MoneyBall
    list_display = ("hex_hash", "crated", "json_file")
