# Generated by Django 5.0.6 on 2024-09-06 04:24

import django_ckeditor_5.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('FAQ_and_terms', '0005_alter_terms_and_condations_description'),
    ]

    operations = [
        migrations.AlterField(
            model_name='faq',
            name='answer',
            field=django_ckeditor_5.fields.CKEditor5Field(verbose_name='Text'),
        ),
    ]
