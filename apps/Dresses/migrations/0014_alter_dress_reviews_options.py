# Generated by Django 5.0.6 on 2024-09-10 08:55

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Dresses', '0013_dress_busy_days_order_uuid'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='dress_reviews',
            options={'ordering': ['-uploaded_at'], 'verbose_name': 'Dresses Reviews', 'verbose_name_plural': 'Dresses Reviews'},
        ),
    ]
