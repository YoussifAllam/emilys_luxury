# Generated by Django 5.0.6 on 2024-08-17 14:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("Dresses", "0012_dresses_num_of_rentals"),
    ]

    operations = [
        migrations.AddField(
            model_name="dress_busy_days",
            name="order_uuid",
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
    ]
