# Generated by Django 5.0.6 on 2024-07-31 20:24

import django.core.validators
import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='invitation_points_Trade',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('num_of_points_for_code', models.IntegerField(default=0, help_text='number of points that user need to change it with coupons', verbose_name='number of points for code')),
                ('discount', models.IntegerField(help_text='coupon discount Percentage value should be between 0 and 100', validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(100)], verbose_name='discount Percentage value')),
            ],
            options={
                'verbose_name': 'Trade points',
                'verbose_name_plural': 'Trade points',
            },
        ),
        migrations.CreateModel(
            name='user_invitation_points',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('num_of_points', models.IntegerField(default=0)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='user_invitation_points_set', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
