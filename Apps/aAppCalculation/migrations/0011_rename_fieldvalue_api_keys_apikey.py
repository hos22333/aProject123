# Generated by Django 4.2 on 2025-05-20 06:11

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('aAppCalculation', '0010_rename_type_api_keys_calctype'),
    ]

    operations = [
        migrations.RenameField(
            model_name='api_keys',
            old_name='fieldvalue',
            new_name='apikey',
        ),
    ]
