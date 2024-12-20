# Generated by Django 5.0.6 on 2024-08-04 15:03

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("Dresses", "0012_dresses_num_of_rentals"),
        ("investment", "0003_investmenter_details_iban"),
    ]

    operations = [
        migrations.AlterField(
            model_name="investmenter_dresses",
            name="dress",
            field=models.OneToOneField(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="investmenter_dresses",
                to="Dresses.dresses",
            ),
        ),
    ]
