# Generated by Django 5.0.6 on 2024-07-07 20:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Shipping', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='INSURANCE',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('INSURANCE', models.FloatField(default=0, verbose_name='INSURANCE amount')),
            ],
            options={
                'verbose_name': 'INSURANCE',
                'verbose_name_plural': 'INSURANCE',
            },
        ),
        migrations.AlterModelOptions(
            name='shipping',
            options={'verbose_name': 'Shipping Flat rate', 'verbose_name_plural': 'Shipping Flat rate'},
        ),
    ]