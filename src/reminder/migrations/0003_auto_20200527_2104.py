# Generated by Django 2.2.4 on 2020-05-27 21:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reminder', '0002_auto_20200507_0923'),
    ]

    operations = [
        migrations.CreateModel(
            name='Recipient',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=32)),
                ('email', models.EmailField(max_length=254)),
            ],
        ),
        migrations.AddField(
            model_name='memory',
            name='recipients',
            field=models.ManyToManyField(to='reminder.Recipient'),
        ),
    ]