# Generated by Django 2.2.4 on 2020-05-07 09:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [("reminder", "0001_initial")]

    operations = [
        migrations.AlterField(
            model_name="memory", name="active", field=models.BooleanField(default=True)
        )
    ]
