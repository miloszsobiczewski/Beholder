# Generated by Django 2.2.17 on 2021-01-08 20:42

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("monitor", "0004_auto_20210104_2208"),
    ]

    operations = [
        migrations.RenameField(
            model_name="exchangerate",
            old_name="buy_gbp_exchange_rate",
            new_name="buy_gbp",
        ),
        migrations.RenameField(
            model_name="exchangerate",
            old_name="buy_usd_exchange_rate",
            new_name="buy_usd",
        ),
        migrations.RenameField(
            model_name="exchangerate",
            old_name="mid_gbp_exchange_rate",
            new_name="mid_gbp",
        ),
        migrations.RenameField(
            model_name="exchangerate",
            old_name="mid_usd_exchange_rate",
            new_name="mid_usd",
        ),
        migrations.RenameField(
            model_name="exchangerate",
            old_name="sell_gbp_exchange_rate",
            new_name="sell_gbp",
        ),
        migrations.RenameField(
            model_name="exchangerate",
            old_name="sell_usd_exchange_rate",
            new_name="sell_usd",
        ),
    ]
