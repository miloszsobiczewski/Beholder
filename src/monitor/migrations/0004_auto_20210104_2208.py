# Generated by Django 2.2.17 on 2021-01-04 21:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("monitor", "0003_exchangerate"),
    ]

    operations = [
        migrations.AlterField(
            model_name="exchangerate",
            name="buy_gbp_exchange_rate",
            field=models.DecimalField(
                blank=True,
                decimal_places=2,
                max_digits=4,
                null=True,
                verbose_name="Buy GBP",
            ),
        ),
        migrations.AlterField(
            model_name="exchangerate",
            name="buy_usd_exchange_rate",
            field=models.DecimalField(
                blank=True,
                decimal_places=2,
                max_digits=4,
                null=True,
                verbose_name="Buy USD",
            ),
        ),
        migrations.AlterField(
            model_name="exchangerate",
            name="mid_gbp_exchange_rate",
            field=models.DecimalField(
                blank=True,
                decimal_places=2,
                max_digits=4,
                null=True,
                verbose_name="Mid GBP",
            ),
        ),
        migrations.AlterField(
            model_name="exchangerate",
            name="mid_usd_exchange_rate",
            field=models.DecimalField(
                blank=True,
                decimal_places=2,
                max_digits=4,
                null=True,
                verbose_name="Mid USD",
            ),
        ),
        migrations.AlterField(
            model_name="exchangerate",
            name="sell_gbp_exchange_rate",
            field=models.DecimalField(
                blank=True,
                decimal_places=2,
                max_digits=4,
                null=True,
                verbose_name="Sell GBP",
            ),
        ),
        migrations.AlterField(
            model_name="exchangerate",
            name="sell_usd_exchange_rate",
            field=models.DecimalField(
                blank=True,
                decimal_places=2,
                max_digits=4,
                null=True,
                verbose_name="Sell USD",
            ),
        ),
    ]
