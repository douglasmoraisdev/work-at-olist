# Generated by Django 2.1 on 2018-08-27 20:38

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('records', '0001_initial'),
        ('bills', '0002_auto_20180827_2016'),
    ]

    operations = [
        migrations.CreateModel(
            name='BillRecord',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('call_price', models.FloatField()),
                ('bill_origin', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='bills.Bill')),
                ('end_call', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='end_call', to='records.Record')),
                ('start_call', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='start_call', to='records.Record')),
            ],
        ),
    ]
