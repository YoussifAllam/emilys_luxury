# Generated by Django 5.0.6 on 2024-09-03 10:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Users', '0003_alter_user_user_type'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='created_Date',
            field=models.DateField(auto_now_add=True),
        ),
    ]