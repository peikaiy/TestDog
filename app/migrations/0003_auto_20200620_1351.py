# Generated by Django 2.2 on 2020-06-20 13:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0002_auto_20200619_1829'),
    ]

    operations = [
        migrations.AlterField(
            model_name='users',
            name='share_moeny_today',
            field=models.IntegerField(default=0, verbose_name='当日推广金'),
        ),
    ]
