# Generated by Django 5.0.6 on 2024-07-27 18:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("Cart", "0004_alter_cart_items_booking_for_n_days"),
    ]

    operations = [
        migrations.AlterField(
            model_name="cart_items",
            name="booking_for_n_days",
            field=models.CharField(
                choices=[("3", 3), ("6", 6), ("8", 8)], max_length=2
            ),
        ),
    ]
