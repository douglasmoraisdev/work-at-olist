# Generated by Django 2.1 on 2018-08-27 20:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bills', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bill',
            name='period',
            field=models.CharField(max_length=7),
        ),
        migrations.AlterField(
            model_name='bill',
            name='subscriber',
            field=models.CharField(max_length=11),
        ),
    ]
