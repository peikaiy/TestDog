# Generated by Django 2.2 on 2020-06-22 13:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0012_auto_20200622_1318'),
    ]

    operations = [
        migrations.AddField(
            model_name='lottery',
            name='t_lottery',
            field=models.DateTimeField(auto_now=True, verbose_name='开奖时间'),
        ),
    ]
