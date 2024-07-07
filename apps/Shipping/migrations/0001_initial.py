# Generated by Django 5.0.2 on 2024-06-20 15:50

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Shipping',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('flatRate', models.FloatField(default=0, verbose_name='Shipping Flat rate')),
            ],
            options={
                'verbose_name': 'Shipping Flat rate',
            },
        ),
    ]
