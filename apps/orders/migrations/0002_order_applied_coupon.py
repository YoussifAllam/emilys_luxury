# Generated by Django 5.0.6 on 2024-07-27 18:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='applied_coupon',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
    ]