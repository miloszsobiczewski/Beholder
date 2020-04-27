from django.contrib import admin
from .models import Memory


@admin.register(Memory)
class MemoryAdmin(admin.ModelAdmin):
    model = Memory
    list_display = ("name", "day", "date", "deadline", "active")
