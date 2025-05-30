# Generated by Django 5.0.9 on 2025-04-24 10:37

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('aAppMechanical', '0017_delete_modelcalc'),
        ('aAppSubmittal', '0002_addmachine'),
    ]

    operations = [
        migrations.AddField(
            model_name='addmachine',
            name='company',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='aAppMechanical.companies'),
        ),
        migrations.AddField(
            model_name='addmachine',
            name='nameFormCalcXX',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='addmachine',
            name='nameForm',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
