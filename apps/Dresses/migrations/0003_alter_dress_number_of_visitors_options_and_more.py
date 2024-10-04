# Generated by Django 5.0.6 on 2024-06-30 08:37

import django.core.validators
import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("Dresses", "0002_remove_dresses_number_of_vesitors_and_more"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="dress_number_of_visitors",
            options={
                "verbose_name": "Dress number of visitors",
                "verbose_name_plural": "Dress number of visitors",
            },
        ),
        migrations.AlterModelOptions(
            name="dresses",
            options={"verbose_name": "Dresses", "verbose_name_plural": "Dresses"},
        ),
        migrations.CreateModel(
            name="dress_reviews",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "Rating_stars",
                    models.IntegerField(
                        validators=[
                            django.core.validators.MinValueValidator(1),
                            django.core.validators.MaxValueValidator(5),
                        ],
                        verbose_name="Rating stars",
                    ),
                ),
                ("uploaded_at", models.DateTimeField(auto_now_add=True)),
                ("feedback", models.TextField()),
                (
                    "dress",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="review_set",
                        to="Dresses.dresses",
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="User_review_set",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                "verbose_name": "Dresses Ratings",
                "verbose_name_plural": "Dresses Ratings",
                "ordering": ["-uploaded_at"],
                "unique_together": {("user", "dress")},
                "index_together": {("user", "dress")},
            },
        ),
    ]
