# Generated by Django 3.0.8 on 2020-07-23 06:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0006_auto_20200722_1713'),
    ]

    operations = [
        migrations.AddField(
            model_name='item',
            name='status',
            field=models.CharField(choices=[('OK', 'OK'), ('NOT_OK', 'NOT_OK')], default='OK', max_length=10),
        ),
    ]