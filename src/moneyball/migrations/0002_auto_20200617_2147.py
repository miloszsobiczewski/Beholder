# Generated by Django 2.2.4 on 2020-06-17 21:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [("moneyball", "0001_initial")]

    operations = [
        migrations.RemoveField(model_name="moneyball", name="id"),
        migrations.RemoveField(model_name="upcoming", name="id"),
        migrations.AlterField(
            model_name="moneyball",
            name="hex_hash",
            field=models.CharField(max_length=32, primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name="moneyball",
            name="json_file",
            field=models.FileField(upload_to="ready"),
        ),
        migrations.AlterField(
            model_name="upcoming",
            name="hex_hash",
            field=models.CharField(max_length=32, primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name="upcoming",
            name="json_file",
            field=models.FileField(upload_to="upcoming"),
        ),
    ]
