# Generated by Django 5.0.6 on 2024-07-27 18:29

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Cart', '0007_cart_applied_coupon'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='cart',
            name='applied_coupon',
        ),
    ]