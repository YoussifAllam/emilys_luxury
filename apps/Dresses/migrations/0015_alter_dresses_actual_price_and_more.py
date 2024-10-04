# Generated by Django 5.0.6 on 2024-09-12 10:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("Dresses", "0014_alter_dress_reviews_options"),
    ]

    operations = [
        migrations.AlterField(
            model_name="dresses",
            name="actual_price",
            field=models.FloatField(),
        ),
        migrations.AlterField(
            model_name="dresses",
            name="delivery_information",
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name="dresses",
            name="description",
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name="dresses",
            name="price_for_3days",
            field=models.FloatField(),
        ),
        migrations.AlterField(
            model_name="dresses",
            name="price_for_6days",
            field=models.FloatField(),
        ),
        migrations.AlterField(
            model_name="dresses",
            name="price_for_8days",
            field=models.FloatField(),
        ),
    ]
