# Generated by Django 3.0.6 on 2020-05-05 18:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mall', '0010_auto_20200506_0131'),
    ]

    operations = [
        migrations.RenameField(
            model_name='userlogin',
            old_name='acive',
            new_name='activate',
        ),
        migrations.AlterField(
            model_name='productcatagory',
            name='catagory',
            field=models.CharField(max_length=20, unique=True),
        ),
    ]
