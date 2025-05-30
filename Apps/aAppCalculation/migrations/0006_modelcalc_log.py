# Generated by Django 5.0.9 on 2025-04-29 06:29

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('aAppCalculation', '0005_modelcalc_osec01field21_modelcalc_osec01field22_and_more'),
        ('aAppMechanical', '0017_delete_modelcalc'),
        ('aAppProject', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='modelcalc_log',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('oSec00Field01', models.CharField(default='', max_length=100)),
                ('oSec00Field02', models.CharField(default='', max_length=100)),
                ('oSec00Field03', models.CharField(default='', max_length=100)),
                ('oSec01Field01', models.CharField(default='', max_length=100)),
                ('oSec01Field02', models.CharField(default='', max_length=100)),
                ('oSec01Field03', models.CharField(default='', max_length=100)),
                ('oSec01Field04', models.CharField(default='', max_length=100)),
                ('oSec01Field05', models.CharField(default='', max_length=100)),
                ('oSec01Field06', models.CharField(default='', max_length=100)),
                ('oSec01Field07', models.CharField(default='', max_length=100)),
                ('oSec01Field08', models.CharField(default='', max_length=100)),
                ('oSec01Field09', models.CharField(default='', max_length=100)),
                ('oSec01Field11', models.CharField(default='', max_length=100)),
                ('oSec01Field12', models.CharField(default='', max_length=100)),
                ('oSec01Field13', models.CharField(default='', max_length=100)),
                ('oSec01Field14', models.CharField(default='', max_length=100)),
                ('oSec01Field15', models.CharField(default='', max_length=100)),
                ('oSec01Field16', models.CharField(default='', max_length=100)),
                ('oSec01Field17', models.CharField(default='', max_length=100)),
                ('oSec01Field18', models.CharField(default='', max_length=100)),
                ('oSec01Field19', models.CharField(default='', max_length=100)),
                ('oSec01Field20', models.CharField(default='', max_length=100)),
                ('oSec01Field10', models.CharField(default='', max_length=100)),
                ('oSec01Field21', models.CharField(default='', max_length=100)),
                ('oSec01Field22', models.CharField(default='', max_length=100)),
                ('oSec01Field23', models.CharField(default='', max_length=100)),
                ('oSec01Field24', models.CharField(default='', max_length=100)),
                ('oSec01Field25', models.CharField(default='', max_length=100)),
                ('oSec01Field26', models.CharField(default='', max_length=100)),
                ('oSec01Field27', models.CharField(default='', max_length=100)),
                ('oSec01Field28', models.CharField(default='', max_length=100)),
                ('oSec01Field29', models.CharField(default='', max_length=100)),
                ('oSec01Field30', models.CharField(default='', max_length=100)),
                ('oSec02Field01', models.CharField(blank=True, default='', max_length=100)),
                ('oSec02Field02', models.CharField(blank=True, default='', max_length=100)),
                ('oSec02Field03', models.CharField(blank=True, default='', max_length=100)),
                ('oSec02Field04', models.CharField(default='', max_length=100)),
                ('oSec02Field05', models.CharField(default='', max_length=100)),
                ('oSec02Field06', models.CharField(default='', max_length=100)),
                ('oSec02Field07', models.CharField(default='', max_length=100)),
                ('oSec02Field08', models.CharField(default='', max_length=100)),
                ('oSec02Field09', models.CharField(default='', max_length=100)),
                ('oSec02Field10', models.CharField(default='', max_length=100)),
                ('oSec02Field11', models.CharField(default='', max_length=100)),
                ('oSec02Field12', models.CharField(default='', max_length=100)),
                ('oSec02Field13', models.CharField(default='', max_length=100)),
                ('oSec02Field14', models.CharField(default='', max_length=100)),
                ('oSec02Field15', models.CharField(default='', max_length=100)),
                ('oSec02Field16', models.CharField(default='', max_length=100)),
                ('oSec02Field17', models.CharField(default='', max_length=100)),
                ('oSec02Field18', models.CharField(default='', max_length=100)),
                ('oSec02Field19', models.CharField(default='', max_length=100)),
                ('oSec02Field20', models.CharField(default='', max_length=100)),
                ('oSec02Field21', models.CharField(default='', max_length=100)),
                ('oSec02Field22', models.CharField(default='', max_length=100)),
                ('oSec02Field23', models.CharField(default='', max_length=100)),
                ('oSec02Field24', models.CharField(default='', max_length=100)),
                ('oSec02Field25', models.CharField(default='', max_length=100)),
                ('oSec02Field26', models.CharField(default='', max_length=100)),
                ('oSec02Field27', models.CharField(default='', max_length=100)),
                ('oSec02Field28', models.CharField(default='', max_length=100)),
                ('oSec02Field29', models.CharField(default='', max_length=100)),
                ('oSec02Field30', models.CharField(default='', max_length=100)),
                ('company', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='aAppMechanical.companies')),
                ('project', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='aAppProject.app_project')),
            ],
        ),
    ]
