# Generated by Django 5.0.6 on 2025-03-13 10:07

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('aAppMechanical', '0011_formfieldconfig_company'),
    ]

    operations = [
        migrations.AddField(
            model_name='machine',
            name='company',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='aAppMechanical.companies'),
        ),
    ]
