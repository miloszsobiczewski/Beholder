# Generated by Django 2.2.4 on 2020-06-17 22:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [("moneyball", "0002_auto_20200617_2147")]

    operations = [
        migrations.AddField(
            model_name="upcoming",
            name="last_run",
            field=models.DateTimeField(auto_now=True),
        )
    ]
