# Generated by Django 5.0.6 on 2024-06-30 09:52

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("Dresses", "0004_dresses_color"),
    ]

    operations = [
        migrations.AddField(
            model_name="dresses",
            name="uploaded_at",
            field=models.DateTimeField(
                auto_now_add=True, default=django.utils.timezone.now
            ),
            preserve_default=False,
        ),
    ]
