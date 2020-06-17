from django.db import models


class MoneyBall(models.Model):
    hex_hash = models.CharField(max_length=32, primary_key=True)
    timestamp = models.DateTimeField()
    json_file = models.FileField(upload_to="ready")
    crated = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.hex_hash


class Upcoming(models.Model):
    hex_hash = models.CharField(max_length=32, primary_key=True)
    timestamp = models.DateTimeField()
    json_file = models.FileField(upload_to="upcoming")
    last_run = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.hex_hash
