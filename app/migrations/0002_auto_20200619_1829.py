# Generated by Django 2.2 on 2020-06-19 18:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userbet',
            name='u_id',
            field=models.IntegerField(verbose_name='玩家id'),
        ),
    ]