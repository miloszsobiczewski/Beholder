from django.db import models


class MoneyBall(models.Model):
    hex_hash = models.CharField(max_length=32, primary_key=True)
    timestamp = models.DateTimeField()
    json_file = models.FileField(upload_to="ready")
    crated = models.DateTimeField(auto_now_add=True)
    teams = models.CharField(max_length=64, null=True, default="")
    sport_key = models.CharField(max_length=32, null=True, default="")
    result = models.CharField(max_length=8, blank=True, default="-")

    def __str__(self):
        return self.hex_hash


class Upcoming(models.Model):
    hex_hash = models.CharField(max_length=32, primary_key=True)
    timestamp = models.DateTimeField()
    json_file = models.FileField(upload_to="upcoming")
    last_run = models.DateTimeField(auto_now=True)
    teams = models.CharField(max_length=64, null=True, default="")
    sport_key = models.CharField(max_length=32, null=True, default="")

    def __str__(self):
        return self.hex_hash
