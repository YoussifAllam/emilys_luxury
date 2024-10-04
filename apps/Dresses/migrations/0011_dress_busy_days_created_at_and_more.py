# Generated by Django 5.0.6 on 2024-07-31 20:57

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("Dresses", "0010_alter_dress_busy_days_unique_together"),
    ]

    operations = [
        migrations.AddField(
            model_name="dress_busy_days",
            name="created_at",
            field=models.DateTimeField(
                auto_now_add=True, default=django.utils.timezone.now
            ),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="dress_busy_days",
            name="is_temporary",
            field=models.BooleanField(default=True),
        ),
    ]
