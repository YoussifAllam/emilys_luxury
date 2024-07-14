# Generated by Django 5.0.6 on 2024-07-09 12:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('FAQ_and_terms', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='faq',
            options={'verbose_name': 'F & Q', 'verbose_name_plural': 'F & Q'},
        ),
        migrations.AlterModelOptions(
            name='terms_and_condations',
            options={'verbose_name': 'Terms & Condations', 'verbose_name_plural': 'Terms & Condations'},
        ),
        migrations.AddField(
            model_name='faq',
            name='Which_Page',
            field=models.CharField(choices=[('Investor', 'Investor'), ('user', 'user')], default='user', max_length=200),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='terms_and_condations',
            name='Which_Page',
            field=models.CharField(choices=[('Investor', 'Investor'), ('user', 'user')], default='user', max_length=200),
            preserve_default=False,
        ),
    ]