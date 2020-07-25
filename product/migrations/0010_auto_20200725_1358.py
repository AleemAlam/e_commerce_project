# Generated by Django 3.0.8 on 2020-07-25 08:28

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('product', '0009_auto_20200723_1640'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cart',
            name='item',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='item', to='product.Item'),
        ),
        migrations.AlterField(
            model_name='rating',
            name='item',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='product.Item'),
        ),
        migrations.CreateModel(
            name='Payments',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('razorpay_payment_id', models.CharField(max_length=200)),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('status', models.CharField(choices=[('APPROVED', 'APPROVED'), ('PENDING', 'PENDING')], max_length=50)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
