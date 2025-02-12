from django.db import models


class FormFieldConfig(models.Model):
    form_name = models.CharField(max_length=100)
    field_name = models.CharField(max_length=100)
    label = models.CharField(max_length=100, blank=True, null=True)
    initial_value = models.CharField(max_length=255, blank=True, null=True)
    VISIBILITY_CHOICES = [
        ('Show', 'Show'),
        ('Hide', 'Hide'),
    ]
    visibility = models.CharField(max_length=10, choices=VISIBILITY_CHOICES, default='Show')

    def __str__(self):
        return f"{self.form_name} - {self.field_name}"


class modelcalc(models.Model):
    oSec00Field01 = models.CharField(max_length=100, default='') #username
    oSec00Field02 = models.CharField(max_length=100, default='') #created at
    oSec00Field03 = models.CharField(max_length=100, default='') #type 
       
    oSec01Field01 = models.CharField(max_length=100, default='')   
    oSec01Field02 = models.CharField(max_length=100, default='')
    oSec01Field03 = models.CharField(max_length=100, default='')
    oSec01Field04 = models.CharField(max_length=100, default='')
    oSec01Field05 = models.CharField(max_length=100, default='')
    oSec01Field06 = models.CharField(max_length=100, default='')
    oSec01Field07 = models.CharField(max_length=100, default='')
    oSec01Field08 = models.CharField(max_length=100, default='')
    oSec01Field09 = models.CharField(max_length=100, default='')
    oSec01Field10 = models.CharField(max_length=100, default='')
    oSec01Field11 = models.CharField(max_length=100, default='')
    oSec01Field12 = models.CharField(max_length=100, default='')
    oSec01Field13 = models.CharField(max_length=100, default='')
    oSec01Field14 = models.CharField(max_length=100, default='')
    oSec01Field15 = models.CharField(max_length=100, default='')
    oSec01Field16 = models.CharField(max_length=100, default='')
    oSec01Field17 = models.CharField(max_length=100, default='')
    oSec01Field18 = models.CharField(max_length=100, default='')
    oSec01Field19 = models.CharField(max_length=100, default='')
    oSec01Field20 = models.CharField(max_length=100, default='') 
       
    oSec02Field01 = models.CharField(max_length=100, default='', blank=True)
    oSec02Field02 = models.CharField(max_length=100, default='', blank=True)
    oSec02Field03 = models.CharField(max_length=100, default='', blank=True)
    oSec02Field04 = models.CharField(max_length=100, default='')
    oSec02Field05 = models.CharField(max_length=100, default='')
    oSec02Field06 = models.CharField(max_length=100, default='')
    oSec02Field07 = models.CharField(max_length=100, default='')
    oSec02Field08 = models.CharField(max_length=100, default='')
    oSec02Field09 = models.CharField(max_length=100, default='')
    oSec02Field10 = models.CharField(max_length=100, default='')
    oSec02Field11 = models.CharField(max_length=100, default='')
    oSec02Field12 = models.CharField(max_length=100, default='')
    oSec02Field13 = models.CharField(max_length=100, default='')
    oSec02Field14 = models.CharField(max_length=100, default='')
    oSec02Field15 = models.CharField(max_length=100, default='')
    oSec02Field16 = models.CharField(max_length=100, default='')
    oSec02Field17 = models.CharField(max_length=100, default='')
    oSec02Field18 = models.CharField(max_length=100, default='')
    oSec02Field19 = models.CharField(max_length=100, default='')
    oSec02Field20 = models.CharField(max_length=100, default='')

    

    def __str__(self):
        return self.oSec01Field01
