# Generated by Django 2.2.17 on 2021-01-04 16:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("monitor", "0002_auto_20200223_0755"),
    ]

    operations = [
        migrations.CreateModel(
            name="ExchangeRate",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("date", models.DateField(auto_now_add=True)),
                (
                    "buy_gbp_exchange_rate",
                    models.DecimalField(
                        blank=True, decimal_places=2, max_digits=4, null=True
                    ),
                ),
                (
                    "mid_gbp_exchange_rate",
                    models.DecimalField(
                        blank=True, decimal_places=2, max_digits=4, null=True
                    ),
                ),
                (
                    "sell_gbp_exchange_rate",
                    models.DecimalField(
                        blank=True, decimal_places=2, max_digits=4, null=True
                    ),
                ),
                (
                    "buy_usd_exchange_rate",
                    models.DecimalField(
                        blank=True, decimal_places=2, max_digits=4, null=True
                    ),
                ),
                (
                    "mid_usd_exchange_rate",
                    models.DecimalField(
                        blank=True, decimal_places=2, max_digits=4, null=True
                    ),
                ),
                (
                    "sell_usd_exchange_rate",
                    models.DecimalField(
                        blank=True, decimal_places=2, max_digits=4, null=True
                    ),
                ),
            ],
        ),
    ]
