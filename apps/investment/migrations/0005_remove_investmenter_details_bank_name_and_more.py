# Generated by Django 5.0.6 on 2024-08-04 21:39

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('investment', '0004_alter_investmenter_dresses_dress'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='investmenter_details',
            name='bank_name',
        ),
        migrations.RemoveField(
            model_name='investmenter_details',
            name='credit_card_number',
        ),
        migrations.RemoveField(
            model_name='investmenter_details',
            name='iban',
        ),
    ]
