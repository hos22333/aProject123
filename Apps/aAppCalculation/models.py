from django.db import models
from Apps.aAppMechanical.models import Companies
from Apps.aAppProject.models import APP_Project


# Create your models here.
class modelcalc(models.Model):
    project         = models.ForeignKey(APP_Project, on_delete=models.CASCADE, related_name='calcmachines', null=True, blank=True)
    company = models.ForeignKey(Companies, on_delete=models.CASCADE, null=True, blank=True)

    
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
    oSec01Field10 = models.CharField(max_length=100, default='')
    oSec01Field21 = models.CharField(max_length=100, default='')
    oSec01Field22 = models.CharField(max_length=100, default='')
    oSec01Field23 = models.CharField(max_length=100, default='')
    oSec01Field24 = models.CharField(max_length=100, default='')
    oSec01Field25 = models.CharField(max_length=100, default='')
    oSec01Field26 = models.CharField(max_length=100, default='')
    oSec01Field27 = models.CharField(max_length=100, default='')
    oSec01Field28 = models.CharField(max_length=100, default='')
    oSec01Field29 = models.CharField(max_length=100, default='')
    oSec01Field30 = models.CharField(max_length=100, default='') 
       
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
    oSec02Field21 = models.CharField(max_length=100, default='')
    oSec02Field22 = models.CharField(max_length=100, default='')
    oSec02Field23 = models.CharField(max_length=100, default='')
    oSec02Field24 = models.CharField(max_length=100, default='')
    oSec02Field25 = models.CharField(max_length=100, default='')
    oSec02Field26 = models.CharField(max_length=100, default='')
    oSec02Field27 = models.CharField(max_length=100, default='')
    oSec02Field28 = models.CharField(max_length=100, default='')
    oSec02Field29 = models.CharField(max_length=100, default='')
    oSec02Field30 = models.CharField(max_length=100, default='') 
          

    def __str__(self):
        project_name = self.project.name if self.project and self.project.name else 'No Project'
        return f"{project_name} ({self.oSec00Field03})"



class modelcalc_log(models.Model):
    project         = models.ForeignKey(APP_Project, on_delete=models.CASCADE, related_name='calcmachines_log', null=True, blank=True)
    company = models.ForeignKey(Companies, on_delete=models.CASCADE, null=True, blank=True)

    
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
    oSec01Field10 = models.CharField(max_length=100, default='')
    oSec01Field21 = models.CharField(max_length=100, default='')
    oSec01Field22 = models.CharField(max_length=100, default='')
    oSec01Field23 = models.CharField(max_length=100, default='')
    oSec01Field24 = models.CharField(max_length=100, default='')
    oSec01Field25 = models.CharField(max_length=100, default='')
    oSec01Field26 = models.CharField(max_length=100, default='')
    oSec01Field27 = models.CharField(max_length=100, default='')
    oSec01Field28 = models.CharField(max_length=100, default='')
    oSec01Field29 = models.CharField(max_length=100, default='')
    oSec01Field30 = models.CharField(max_length=100, default='') 
       
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
    oSec02Field21 = models.CharField(max_length=100, default='')
    oSec02Field22 = models.CharField(max_length=100, default='')
    oSec02Field23 = models.CharField(max_length=100, default='')
    oSec02Field24 = models.CharField(max_length=100, default='')
    oSec02Field25 = models.CharField(max_length=100, default='')
    oSec02Field26 = models.CharField(max_length=100, default='')
    oSec02Field27 = models.CharField(max_length=100, default='')
    oSec02Field28 = models.CharField(max_length=100, default='')
    oSec02Field29 = models.CharField(max_length=100, default='')
    oSec02Field30 = models.CharField(max_length=100, default='') 
          

    def __str__(self):
        project_name = self.project.name if self.project and self.project.name else 'No Project'
        return f"{project_name} ({self.oSec00Field03})"


class API_Keys(models.Model):
    sheetkey = models.CharField(max_length=255)
    calctype = models.CharField(max_length=255)
    fieldname = models.CharField(max_length=255)
    apikey = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.sheetkey}__{self.calctype}__{self.fieldname}"