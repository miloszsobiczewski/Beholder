from django.db import models


class Recipient(models.Model):
    name = models.CharField(max_length=32)
    email = models.EmailField()

    def __str__(self):
        return f"{self.name} ({self.email})"


class Memory(models.Model):
    name = models.CharField(max_length=100)
    text = models.TextField()
    day = models.PositiveIntegerField()
    deadline = models.CharField(max_length=100)
    active = models.BooleanField(default=True)
    date = models.DateField(null=True, blank=True)
    recipients = models.ManyToManyField(Recipient)
