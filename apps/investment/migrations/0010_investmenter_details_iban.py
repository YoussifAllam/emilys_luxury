# Generated by Django 5.0.6 on 2024-09-11 08:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('investment', '0009_alter_investmenter_details_options'),
    ]

    operations = [
        migrations.AddField(
            model_name='investmenter_details',
            name='iban',
            field=models.CharField(default=1, max_length=50),
            preserve_default=False,
        ),
    ]
