# Generated by Django 3.0.6 on 2020-05-07 16:38

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('mall', '0013_auto_20200508_0028'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='cart',
            name='cart_total_price',
        ),
        migrations.AddField(
            model_name='cart',
            name='last_update',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]
