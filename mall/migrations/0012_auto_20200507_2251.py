# Generated by Django 3.0.6 on 2020-05-07 14:51

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mall', '0011_auto_20200506_0217'),
    ]

    operations = [
        migrations.RenameField(
            model_name='orders',
            old_name='last_update_time',
            new_name='create_time',
        ),
    ]