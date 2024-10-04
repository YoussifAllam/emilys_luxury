# Generated by Django 5.0.6 on 2024-08-19 07:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("Users", "0002_user_user_type"),
    ]

    operations = [
        migrations.AlterField(
            model_name="user",
            name="user_type",
            field=models.CharField(
                choices=[
                    ("Customer", "Customer"),
                    ("Investor", "Investor"),
                    ("unset", "Unset"),
                ],
                default="unset",
                max_length=20,
            ),
        ),
    ]
