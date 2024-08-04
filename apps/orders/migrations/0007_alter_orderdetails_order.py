# Generated by Django 5.0.6 on 2024-08-04 15:03

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0006_order_arrival_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orderdetails',
            name='order',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='order_details_set', to='orders.order'),
        ),
    ]
