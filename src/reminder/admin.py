from django.contrib import admin
from .models import Memory, Recipient


@admin.register(Memory)
class MemoryAdmin(admin.ModelAdmin):
    model = Memory
    list_display = ("name", "day", "date", "deadline", "active")


@admin.register(Recipient)
class RecipientAdmin(admin.ModelAdmin):
    model = Recipient
    list_display = ("name", "email")
