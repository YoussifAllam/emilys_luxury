# Generated by Django 5.0.6 on 2024-07-07 20:35

import django.db.models.deletion
import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('Dresses', '0007_alter_dresses_actual_price_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Cart',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Cart_Items',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('date_added', models.DateField(auto_now_add=True)),
                ('cart', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='items', to='Cart.cart')),
                ('dress', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Dresses.dresses')),
            ],
            options={
                'db_table': 'Cart',
                'ordering': ['-date_added'],
            },
        ),
    ]