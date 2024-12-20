# Generated by Django 5.0.6 on 2024-07-27 20:58

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("orders", "0003_remove_order_dress_booking_days_order_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="orderitem",
            name="booking_end_date",
            field=models.DateField(default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="orderitem",
            name="booking_for_n_days",
            field=models.IntegerField(default=1),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="orderitem",
            name="booking_start_date",
            field=models.DateField(default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]
