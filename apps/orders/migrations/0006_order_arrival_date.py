# Generated by Django 5.0.6 on 2024-08-03 10:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0005_rename_days_order_dress_booking_days_day_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='arrival_date',
            field=models.DateField(blank=True, null=True),
        ),
    ]