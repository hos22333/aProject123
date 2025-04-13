from django import forms
from Apps.aAppMechanical.models import modelcalc
from Apps.aAppMechanical.models import FormFieldConfig
from Apps.aAppMechanical.models import Project, Machine
from Apps.aAppMechanical.models import UserCompany



class FormCalculationsSheet(forms.Form):
    project = forms.ModelChoiceField(
        queryset=Project.objects.all(),
        required=False,  # Allows an empty selection
        widget=forms.Select(attrs={'class': 'form-control shadow-sm rounded'})
    )
    
    oSec01Field01 = forms.CharField(required=False, widget=forms.TextInput(attrs={'class': 'form-control shadow-sm rounded', 'readonly': 'readonly', 'style': 'color: blue; font-weight: bold;'}))
    oSec01Field02 = forms.CharField(required=False, widget=forms.TextInput(attrs={'class': 'form-control shadow-sm rounded', 'style': 'color: blue;'}))
    oSec01Field03 = forms.CharField(required=False, widget=forms.TextInput(attrs={'class': 'form-control shadow-sm rounded', 'readonly': 'readonly', 'style': 'color: blue; font-weight: bold;'}))
    oSec01Field04 = forms.CharField(required=False, widget=forms.TextInput(attrs={'class': 'form-control shadow-sm rounded', 'style': 'color: blue;'}))
    oSec01Field05 = forms.CharField(required=False, widget=forms.TextInput(attrs={'class': 'form-control shadow-sm rounded', 'readonly': 'readonly', 'style': 'color: blue; font-weight: bold;'}))
    oSec01Field06 = forms.CharField(required=False, widget=forms.TextInput(attrs={'class': 'form-control shadow-sm rounded', 'style': 'color: blue;'}))
    oSec01Field07 = forms.CharField(required=False, widget=forms.TextInput(attrs={'class': 'form-control shadow-sm rounded', 'readonly': 'readonly', 'style': 'color: blue; font-weight: bold;'}))
    oSec01Field08 = forms.CharField(required=False, widget=forms.TextInput(attrs={'class': 'form-control shadow-sm rounded', 'style': 'color: blue;'}))
    oSec01Field09 = forms.CharField(required=False, widget=forms.TextInput(attrs={'class': 'form-control shadow-sm rounded', 'readonly': 'readonly', 'style': 'color: blue; font-weight: bold;'}))
    oSec01Field10 = forms.CharField(required=False, widget=forms.TextInput(attrs={'class': 'form-control shadow-sm rounded', 'style': 'color: blue;'}))
    oSec01Field11 = forms.CharField(required=False, widget=forms.TextInput(attrs={'class': 'form-control shadow-sm rounded', 'readonly': 'readonly', 'style': 'color: blue; font-weight: bold;'}))
    oSec01Field12 = forms.CharField(required=False, widget=forms.TextInput(attrs={'class': 'form-control shadow-sm rounded', 'style': 'color: blue;'}))
    oSec01Field13 = forms.CharField(required=False, widget=forms.TextInput(attrs={'class': 'form-control shadow-sm rounded', 'readonly': 'readonly', 'style': 'color: blue; font-weight: bold;'}))
    oSec01Field14 = forms.CharField(required=False, widget=forms.TextInput(attrs={'class': 'form-control shadow-sm rounded', 'style': 'color: blue;'}))
    oSec01Field15 = forms.CharField(required=False, widget=forms.TextInput(attrs={'class': 'form-control shadow-sm rounded', 'readonly': 'readonly', 'style': 'color: blue; font-weight: bold;'}))
    oSec01Field16 = forms.CharField(required=False, widget=forms.TextInput(attrs={'class': 'form-control shadow-sm rounded', 'style': 'color: blue;'}))
    oSec01Field17 = forms.CharField(required=False, widget=forms.TextInput(attrs={'class': 'form-control shadow-sm rounded', 'readonly': 'readonly', 'style': 'color: blue; font-weight: bold;'}))
    oSec01Field18 = forms.CharField(required=False, widget=forms.TextInput(attrs={'class': 'form-control shadow-sm rounded', 'style': 'color: blue;'}))
    oSec01Field19 = forms.CharField(required=False, widget=forms.TextInput(attrs={'class': 'form-control shadow-sm rounded', 'readonly': 'readonly', 'style': 'color: blue; font-weight: bold;'}))
    oSec01Field20 = forms.CharField(required=False, widget=forms.TextInput(attrs={'class': 'form-control shadow-sm rounded', 'style': 'color: blue;'}))
    
    
    oSec02Field01 = forms.CharField(required=False, widget=forms.TextInput(attrs={'class': 'form-control shadow-sm rounded', 'readonly': 'readonly', 'style': 'color: blue; font-weight: bold;'}))
    oSec02Field02 = forms.CharField(required=False, widget=forms.TextInput(attrs={'class': 'form-control shadow-sm rounded', 'style': 'color: blue;'}))
    oSec02Field03 = forms.CharField(required=False, widget=forms.TextInput(attrs={'class': 'form-control shadow-sm rounded', 'readonly': 'readonly', 'style': 'color: blue; font-weight: bold;'}))
    oSec02Field04 = forms.CharField(required=False, widget=forms.TextInput(attrs={'class': 'form-control shadow-sm rounded', 'style': 'color: blue;'}))
    oSec02Field05 = forms.CharField(required=False, widget=forms.TextInput(attrs={'class': 'form-control shadow-sm rounded', 'readonly': 'readonly', 'style': 'color: blue; font-weight: bold;'}))
    oSec02Field06 = forms.CharField(required=False, widget=forms.TextInput(attrs={'class': 'form-control shadow-sm rounded', 'style': 'color: blue;'}))
    oSec02Field07 = forms.CharField(required=False, widget=forms.TextInput(attrs={'class': 'form-control shadow-sm rounded', 'readonly': 'readonly', 'style': 'color: blue; font-weight: bold;'}))
    oSec02Field08 = forms.CharField(required=False, widget=forms.TextInput(attrs={'class': 'form-control shadow-sm rounded', 'style': 'color: blue;'}))
    oSec02Field09 = forms.CharField(required=False, widget=forms.TextInput(attrs={'class': 'form-control shadow-sm rounded', 'readonly': 'readonly', 'style': 'color: blue; font-weight: bold;'}))
    oSec02Field10 = forms.CharField(required=False, widget=forms.TextInput(attrs={'class': 'form-control shadow-sm rounded', 'style': 'color: blue;'}))
    oSec02Field11 = forms.CharField(required=False, widget=forms.TextInput(attrs={'class': 'form-control shadow-sm rounded', 'readonly': 'readonly', 'style': 'color: blue; font-weight: bold;'}))
    oSec02Field12 = forms.CharField(required=False, widget=forms.TextInput(attrs={'class': 'form-control shadow-sm rounded', 'style': 'color: blue;'}))
    oSec02Field13 = forms.CharField(required=False, widget=forms.TextInput(attrs={'class': 'form-control shadow-sm rounded', 'readonly': 'readonly', 'style': 'color: blue; font-weight: bold;'}))
    oSec02Field14 = forms.CharField(required=False, widget=forms.TextInput(attrs={'class': 'form-control shadow-sm rounded', 'style': 'color: blue;'}))
    oSec02Field15 = forms.CharField(required=False, widget=forms.TextInput(attrs={'class': 'form-control shadow-sm rounded', 'readonly': 'readonly', 'style': 'color: blue; font-weight: bold;'}))
    oSec02Field16 = forms.CharField(required=False, widget=forms.TextInput(attrs={'class': 'form-control shadow-sm rounded', 'style': 'color: blue;'}))
    oSec02Field17 = forms.CharField(required=False, widget=forms.TextInput(attrs={'class': 'form-control shadow-sm rounded', 'readonly': 'readonly', 'style': 'color: blue; font-weight: bold;'}))
    oSec02Field18 = forms.CharField(required=False, widget=forms.TextInput(attrs={'class': 'form-control shadow-sm rounded', 'style': 'color: blue;'}))
    oSec02Field19 = forms.CharField(required=False, widget=forms.TextInput(attrs={'class': 'form-control shadow-sm rounded', 'readonly': 'readonly', 'style': 'color: blue; font-weight: bold;'}))
    oSec02Field20 = forms.CharField(required=False, widget=forms.TextInput(attrs={'class': 'form-control shadow-sm rounded', 'style': 'color: blue;'}))
    
    
    oSec03Field01 = forms.CharField(required=False, widget=forms.TextInput(attrs={'class': 'form-control shadow-sm rounded', 'readonly': 'readonly', 'style': 'color: blue; font-weight: bold;'}))
    oSec03Field02 = forms.CharField(required=False, widget=forms.TextInput(attrs={'class': 'form-control shadow-sm rounded', 'style': 'color: blue;'}))
    oSec03Field03 = forms.CharField(required=False, widget=forms.TextInput(attrs={'class': 'form-control shadow-sm rounded', 'readonly': 'readonly', 'style': 'color: blue; font-weight: bold;'}))
    oSec03Field04 = forms.CharField(required=False, widget=forms.TextInput(attrs={'class': 'form-control shadow-sm rounded', 'style': 'color: blue;'}))
    oSec03Field05 = forms.CharField(required=False, widget=forms.TextInput(attrs={'class': 'form-control shadow-sm rounded', 'readonly': 'readonly', 'style': 'color: blue; font-weight: bold;'}))
    oSec03Field06 = forms.CharField(required=False, widget=forms.TextInput(attrs={'class': 'form-control shadow-sm rounded', 'style': 'color: blue;'}))
    oSec03Field07 = forms.CharField(required=False, widget=forms.TextInput(attrs={'class': 'form-control shadow-sm rounded', 'readonly': 'readonly', 'style': 'color: blue; font-weight: bold;'}))
    oSec03Field08 = forms.CharField(required=False, widget=forms.TextInput(attrs={'class': 'form-control shadow-sm rounded', 'style': 'color: blue;'}))
    oSec03Field09 = forms.CharField(required=False, widget=forms.TextInput(attrs={'class': 'form-control shadow-sm rounded', 'readonly': 'readonly', 'style': 'color: blue; font-weight: bold;'}))
    oSec03Field10 = forms.CharField(required=False, widget=forms.TextInput(attrs={'class': 'form-control shadow-sm rounded', 'style': 'color: blue;'}))
    oSec03Field11 = forms.CharField(required=False, widget=forms.TextInput(attrs={'class': 'form-control shadow-sm rounded', 'readonly': 'readonly', 'style': 'color: blue; font-weight: bold;'}))
    oSec03Field12 = forms.CharField(required=False, widget=forms.TextInput(attrs={'class': 'form-control shadow-sm rounded', 'style': 'color: blue;'}))
    oSec03Field13 = forms.CharField(required=False, widget=forms.TextInput(attrs={'class': 'form-control shadow-sm rounded', 'readonly': 'readonly', 'style': 'color: blue; font-weight: bold;'}))
    oSec03Field14 = forms.CharField(required=False, widget=forms.TextInput(attrs={'class': 'form-control shadow-sm rounded', 'style': 'color: blue;'}))
    oSec03Field15 = forms.CharField(required=False, widget=forms.TextInput(attrs={'class': 'form-control shadow-sm rounded', 'readonly': 'readonly', 'style': 'color: blue; font-weight: bold;'}))
    oSec03Field16 = forms.CharField(required=False, widget=forms.TextInput(attrs={'class': 'form-control shadow-sm rounded', 'style': 'color: blue;'}))
    oSec03Field17 = forms.CharField(required=False, widget=forms.TextInput(attrs={'class': 'form-control shadow-sm rounded', 'readonly': 'readonly', 'style': 'color: blue; font-weight: bold;'}))
    oSec03Field18 = forms.CharField(required=False, widget=forms.TextInput(attrs={'class': 'form-control shadow-sm rounded', 'style': 'color: blue;'}))
    oSec03Field19 = forms.CharField(required=False, widget=forms.TextInput(attrs={'class': 'form-control shadow-sm rounded', 'readonly': 'readonly', 'style': 'color: blue; font-weight: bold;'}))
    oSec03Field20 = forms.CharField(required=False, widget=forms.TextInput(attrs={'class': 'form-control shadow-sm rounded', 'style': 'color: blue;'}))
    
    
    oSec04Field01 = forms.CharField(required=False, widget=forms.TextInput(attrs={'class': 'form-control shadow-sm rounded', 'readonly': 'readonly', 'style': 'color: blue; font-weight: bold;'}))
    oSec04Field02 = forms.CharField(required=False, widget=forms.TextInput(attrs={'class': 'form-control shadow-sm rounded', 'style': 'color: blue;'}))
    oSec04Field03 = forms.CharField(required=False, widget=forms.TextInput(attrs={'class': 'form-control shadow-sm rounded', 'readonly': 'readonly', 'style': 'color: blue; font-weight: bold;'}))
    oSec04Field04 = forms.CharField(required=False, widget=forms.TextInput(attrs={'class': 'form-control shadow-sm rounded', 'style': 'color: blue;'}))
    oSec04Field05 = forms.CharField(required=False, widget=forms.TextInput(attrs={'class': 'form-control shadow-sm rounded', 'readonly': 'readonly', 'style': 'color: blue; font-weight: bold;'}))
    oSec04Field06 = forms.CharField(required=False, widget=forms.TextInput(attrs={'class': 'form-control shadow-sm rounded', 'style': 'color: blue;'}))
    oSec04Field07 = forms.CharField(required=False, widget=forms.TextInput(attrs={'class': 'form-control shadow-sm rounded', 'readonly': 'readonly', 'style': 'color: blue; font-weight: bold;'}))
    oSec04Field08 = forms.CharField(required=False, widget=forms.TextInput(attrs={'class': 'form-control shadow-sm rounded', 'style': 'color: blue;'}))
    oSec04Field09 = forms.CharField(required=False, widget=forms.TextInput(attrs={'class': 'form-control shadow-sm rounded', 'readonly': 'readonly', 'style': 'color: blue; font-weight: bold;'}))
    oSec04Field10 = forms.CharField(required=False, widget=forms.TextInput(attrs={'class': 'form-control shadow-sm rounded', 'style': 'color: blue;'}))
    oSec04Field11 = forms.CharField(required=False, widget=forms.TextInput(attrs={'class': 'form-control shadow-sm rounded', 'readonly': 'readonly', 'style': 'color: blue; font-weight: bold;'}))
    oSec04Field12 = forms.CharField(required=False, widget=forms.TextInput(attrs={'class': 'form-control shadow-sm rounded', 'style': 'color: blue;'}))
    oSec04Field13 = forms.CharField(required=False, widget=forms.TextInput(attrs={'class': 'form-control shadow-sm rounded', 'readonly': 'readonly', 'style': 'color: blue; font-weight: bold;'}))
    oSec04Field14 = forms.CharField(required=False, widget=forms.TextInput(attrs={'class': 'form-control shadow-sm rounded', 'style': 'color: blue;'}))
    oSec04Field15 = forms.CharField(required=False, widget=forms.TextInput(attrs={'class': 'form-control shadow-sm rounded', 'readonly': 'readonly', 'style': 'color: blue; font-weight: bold;'}))
    oSec04Field16 = forms.CharField(required=False, widget=forms.TextInput(attrs={'class': 'form-control shadow-sm rounded', 'style': 'color: blue;'}))
    oSec04Field17 = forms.CharField(required=False, widget=forms.TextInput(attrs={'class': 'form-control shadow-sm rounded', 'readonly': 'readonly', 'style': 'color: blue; font-weight: bold;'}))
    oSec04Field18 = forms.CharField(required=False, widget=forms.TextInput(attrs={'class': 'form-control shadow-sm rounded', 'style': 'color: blue;'}))
    oSec04Field19 = forms.CharField(required=False, widget=forms.TextInput(attrs={'class': 'form-control shadow-sm rounded', 'readonly': 'readonly', 'style': 'color: blue; font-weight: bold;'}))
    oSec04Field20 = forms.CharField(required=False, widget=forms.TextInput(attrs={'class': 'form-control shadow-sm rounded', 'style': 'color: blue;'}))
    
    
    oSec05Field01 = forms.CharField(required=False, widget=forms.TextInput(attrs={'class': 'form-control shadow-sm rounded', 'readonly': 'readonly', 'style': 'color: blue; font-weight: bold;'}))
    oSec05Field02 = forms.CharField(required=False, widget=forms.TextInput(attrs={'class': 'form-control shadow-sm rounded', 'style': 'color: blue;'}))
    oSec05Field03 = forms.CharField(required=False, widget=forms.TextInput(attrs={'class': 'form-control shadow-sm rounded', 'readonly': 'readonly', 'style': 'color: blue; font-weight: bold;'}))
    oSec05Field04 = forms.CharField(required=False, widget=forms.TextInput(attrs={'class': 'form-control shadow-sm rounded', 'style': 'color: blue;'}))
    oSec05Field05 = forms.CharField(required=False, widget=forms.TextInput(attrs={'class': 'form-control shadow-sm rounded', 'readonly': 'readonly', 'style': 'color: blue; font-weight: bold;'}))
    oSec05Field06 = forms.CharField(required=False, widget=forms.TextInput(attrs={'class': 'form-control shadow-sm rounded', 'style': 'color: blue;'}))
    oSec05Field07 = forms.CharField(required=False, widget=forms.TextInput(attrs={'class': 'form-control shadow-sm rounded', 'readonly': 'readonly', 'style': 'color: blue; font-weight: bold;'}))
    oSec05Field08 = forms.CharField(required=False, widget=forms.TextInput(attrs={'class': 'form-control shadow-sm rounded', 'style': 'color: blue;'}))
    oSec05Field09 = forms.CharField(required=False, widget=forms.TextInput(attrs={'class': 'form-control shadow-sm rounded', 'readonly': 'readonly', 'style': 'color: blue; font-weight: bold;'}))
    oSec05Field10 = forms.CharField(required=False, widget=forms.TextInput(attrs={'class': 'form-control shadow-sm rounded', 'style': 'color: blue;'}))
    oSec05Field11 = forms.CharField(required=False, widget=forms.TextInput(attrs={'class': 'form-control shadow-sm rounded', 'readonly': 'readonly', 'style': 'color: blue; font-weight: bold;'}))
    oSec05Field12 = forms.CharField(required=False, widget=forms.TextInput(attrs={'class': 'form-control shadow-sm rounded', 'style': 'color: blue;'}))
    oSec05Field13 = forms.CharField(required=False, widget=forms.TextInput(attrs={'class': 'form-control shadow-sm rounded', 'readonly': 'readonly', 'style': 'color: blue; font-weight: bold;'}))
    oSec05Field14 = forms.CharField(required=False, widget=forms.TextInput(attrs={'class': 'form-control shadow-sm rounded', 'style': 'color: blue;'}))
    oSec05Field15 = forms.CharField(required=False, widget=forms.TextInput(attrs={'class': 'form-control shadow-sm rounded', 'readonly': 'readonly', 'style': 'color: blue; font-weight: bold;'}))
    oSec05Field16 = forms.CharField(required=False, widget=forms.TextInput(attrs={'class': 'form-control shadow-sm rounded', 'style': 'color: blue;'}))
    oSec05Field17 = forms.CharField(required=False, widget=forms.TextInput(attrs={'class': 'form-control shadow-sm rounded', 'readonly': 'readonly', 'style': 'color: blue; font-weight: bold;'}))
    oSec05Field18 = forms.CharField(required=False, widget=forms.TextInput(attrs={'class': 'form-control shadow-sm rounded', 'style': 'color: blue;'}))
    oSec05Field19 = forms.CharField(required=False, widget=forms.TextInput(attrs={'class': 'form-control shadow-sm rounded', 'readonly': 'readonly', 'style': 'color: blue; font-weight: bold;'}))
    oSec05Field20 = forms.CharField(required=False, widget=forms.TextInput(attrs={'class': 'form-control shadow-sm rounded', 'style': 'color: blue;'}))
    
    
    oSec06Field01 = forms.CharField(required=False, widget=forms.TextInput(attrs={'class': 'form-control shadow-sm rounded', 'readonly': 'readonly', 'style': 'color: blue; font-weight: bold;'}))
    oSec06Field02 = forms.CharField(required=False, widget=forms.TextInput(attrs={'class': 'form-control shadow-sm rounded', 'style': 'color: blue;'}))
    oSec06Field03 = forms.CharField(required=False, widget=forms.TextInput(attrs={'class': 'form-control shadow-sm rounded', 'readonly': 'readonly', 'style': 'color: blue; font-weight: bold;'}))
    oSec06Field04 = forms.CharField(required=False, widget=forms.TextInput(attrs={'class': 'form-control shadow-sm rounded', 'style': 'color: blue;'}))
    oSec06Field05 = forms.CharField(required=False, widget=forms.TextInput(attrs={'class': 'form-control shadow-sm rounded', 'readonly': 'readonly', 'style': 'color: blue; font-weight: bold;'}))
    oSec06Field06 = forms.CharField(required=False, widget=forms.TextInput(attrs={'class': 'form-control shadow-sm rounded', 'style': 'color: blue;'}))
    oSec06Field07 = forms.CharField(required=False, widget=forms.TextInput(attrs={'class': 'form-control shadow-sm rounded', 'readonly': 'readonly', 'style': 'color: blue; font-weight: bold;'}))
    oSec06Field08 = forms.CharField(required=False, widget=forms.TextInput(attrs={'class': 'form-control shadow-sm rounded', 'style': 'color: blue;'}))
    oSec06Field09 = forms.CharField(required=False, widget=forms.TextInput(attrs={'class': 'form-control shadow-sm rounded', 'readonly': 'readonly', 'style': 'color: blue; font-weight: bold;'}))
    oSec06Field10 = forms.CharField(required=False, widget=forms.TextInput(attrs={'class': 'form-control shadow-sm rounded', 'style': 'color: blue;'}))
    oSec06Field11 = forms.CharField(required=False, widget=forms.TextInput(attrs={'class': 'form-control shadow-sm rounded', 'readonly': 'readonly', 'style': 'color: blue; font-weight: bold;'}))
    oSec06Field12 = forms.CharField(required=False, widget=forms.TextInput(attrs={'class': 'form-control shadow-sm rounded', 'style': 'color: blue;'}))
    oSec06Field13 = forms.CharField(required=False, widget=forms.TextInput(attrs={'class': 'form-control shadow-sm rounded', 'readonly': 'readonly', 'style': 'color: blue; font-weight: bold;'}))
    oSec06Field14 = forms.CharField(required=False, widget=forms.TextInput(attrs={'class': 'form-control shadow-sm rounded', 'style': 'color: blue;'}))
    oSec06Field15 = forms.CharField(required=False, widget=forms.TextInput(attrs={'class': 'form-control shadow-sm rounded', 'readonly': 'readonly', 'style': 'color: blue; font-weight: bold;'}))
    oSec06Field16 = forms.CharField(required=False, widget=forms.TextInput(attrs={'class': 'form-control shadow-sm rounded', 'style': 'color: blue;'}))
    oSec06Field17 = forms.CharField(required=False, widget=forms.TextInput(attrs={'class': 'form-control shadow-sm rounded', 'readonly': 'readonly', 'style': 'color: blue; font-weight: bold;'}))
    oSec06Field18 = forms.CharField(required=False, widget=forms.TextInput(attrs={'class': 'form-control shadow-sm rounded', 'style': 'color: blue;'}))
    oSec06Field19 = forms.CharField(required=False, widget=forms.TextInput(attrs={'class': 'form-control shadow-sm rounded', 'readonly': 'readonly', 'style': 'color: blue; font-weight: bold;'}))
    oSec06Field20 = forms.CharField(required=False, widget=forms.TextInput(attrs={'class': 'form-control shadow-sm rounded', 'style': 'color: blue;'}))
    
    
    oSec07Field01 = forms.CharField(required=False, widget=forms.TextInput(attrs={'class': 'form-control shadow-sm rounded', 'readonly': 'readonly', 'style': 'color: blue; font-weight: bold;'}))
    oSec07Field02 = forms.CharField(required=False, widget=forms.TextInput(attrs={'class': 'form-control shadow-sm rounded', 'style': 'color: blue;'}))
    oSec07Field03 = forms.CharField(required=False, widget=forms.TextInput(attrs={'class': 'form-control shadow-sm rounded', 'readonly': 'readonly', 'style': 'color: blue; font-weight: bold;'}))
    oSec07Field04 = forms.CharField(required=False, widget=forms.TextInput(attrs={'class': 'form-control shadow-sm rounded', 'style': 'color: blue;'}))
    oSec07Field05 = forms.CharField(required=False, widget=forms.TextInput(attrs={'class': 'form-control shadow-sm rounded', 'readonly': 'readonly', 'style': 'color: blue; font-weight: bold;'}))
    oSec07Field06 = forms.CharField(required=False, widget=forms.TextInput(attrs={'class': 'form-control shadow-sm rounded', 'style': 'color: blue;'}))
    oSec07Field07 = forms.CharField(required=False, widget=forms.TextInput(attrs={'class': 'form-control shadow-sm rounded', 'readonly': 'readonly', 'style': 'color: blue; font-weight: bold;'}))
    oSec07Field08 = forms.CharField(required=False, widget=forms.TextInput(attrs={'class': 'form-control shadow-sm rounded', 'style': 'color: blue;'}))
    oSec07Field09 = forms.CharField(required=False, widget=forms.TextInput(attrs={'class': 'form-control shadow-sm rounded', 'readonly': 'readonly', 'style': 'color: blue; font-weight: bold;'}))
    oSec07Field10 = forms.CharField(required=False, widget=forms.TextInput(attrs={'class': 'form-control shadow-sm rounded', 'style': 'color: blue;'}))    
    oSec07Field11 = forms.CharField(required=False, widget=forms.TextInput(attrs={'class': 'form-control shadow-sm rounded', 'readonly': 'readonly', 'style': 'color: blue; font-weight: bold;'}))
    oSec07Field12 = forms.CharField(required=False, widget=forms.TextInput(attrs={'class': 'form-control shadow-sm rounded', 'style': 'color: blue;'}))
    oSec07Field13 = forms.CharField(required=False, widget=forms.TextInput(attrs={'class': 'form-control shadow-sm rounded', 'readonly': 'readonly', 'style': 'color: blue; font-weight: bold;'}))
    oSec07Field14 = forms.CharField(required=False, widget=forms.TextInput(attrs={'class': 'form-control shadow-sm rounded', 'style': 'color: blue;'}))
    oSec07Field15 = forms.CharField(required=False, widget=forms.TextInput(attrs={'class': 'form-control shadow-sm rounded', 'readonly': 'readonly', 'style': 'color: blue; font-weight: bold;'}))
    oSec07Field16 = forms.CharField(required=False, widget=forms.TextInput(attrs={'class': 'form-control shadow-sm rounded', 'style': 'color: blue;'}))
    oSec07Field17 = forms.CharField(required=False, widget=forms.TextInput(attrs={'class': 'form-control shadow-sm rounded', 'readonly': 'readonly', 'style': 'color: blue; font-weight: bold;'}))
    oSec07Field18 = forms.CharField(required=False, widget=forms.TextInput(attrs={'class': 'form-control shadow-sm rounded', 'style': 'color: blue;'}))
    oSec07Field19 = forms.CharField(required=False, widget=forms.TextInput(attrs={'class': 'form-control shadow-sm rounded', 'readonly': 'readonly', 'style': 'color: blue; font-weight: bold;'}))
    oSec07Field20 = forms.CharField(required=False, widget=forms.TextInput(attrs={'class': 'form-control shadow-sm rounded', 'style': 'color: blue;'}))
    
    oSec08Field01 = forms.CharField(required=False, widget=forms.TextInput(attrs={'class': 'form-control shadow-sm rounded', 'readonly': 'readonly', 'style': 'color: blue; font-weight: bold;'}))
    oSec08Field02 = forms.CharField(required=False, widget=forms.TextInput(attrs={'class': 'form-control shadow-sm rounded', 'style': 'color: blue;'}))
    oSec08Field03 = forms.CharField(required=False, widget=forms.TextInput(attrs={'class': 'form-control shadow-sm rounded', 'readonly': 'readonly', 'style': 'color: blue; font-weight: bold;'}))
    oSec08Field04 = forms.CharField(required=False, widget=forms.TextInput(attrs={'class': 'form-control shadow-sm rounded', 'style': 'color: blue;'}))
    oSec08Field05 = forms.CharField(required=False, widget=forms.TextInput(attrs={'class': 'form-control shadow-sm rounded', 'readonly': 'readonly', 'style': 'color: blue; font-weight: bold;'}))
    oSec08Field06 = forms.CharField(required=False, widget=forms.TextInput(attrs={'class': 'form-control shadow-sm rounded', 'style': 'color: blue;'}))
    oSec08Field07 = forms.CharField(required=False, widget=forms.TextInput(attrs={'class': 'form-control shadow-sm rounded', 'readonly': 'readonly', 'style': 'color: blue; font-weight: bold;'}))
    oSec08Field08 = forms.CharField(required=False, widget=forms.TextInput(attrs={'class': 'form-control shadow-sm rounded', 'style': 'color: blue;'}))
    oSec08Field09 = forms.CharField(required=False, widget=forms.TextInput(attrs={'class': 'form-control shadow-sm rounded', 'readonly': 'readonly', 'style': 'color: blue; font-weight: bold;'}))
    oSec08Field10 = forms.CharField(required=False, widget=forms.TextInput(attrs={'class': 'form-control shadow-sm rounded', 'style': 'color: blue;'}))    
    oSec08Field11 = forms.CharField(required=False, widget=forms.TextInput(attrs={'class': 'form-control shadow-sm rounded', 'readonly': 'readonly', 'style': 'color: blue; font-weight: bold;'}))
    oSec08Field12 = forms.CharField(required=False, widget=forms.TextInput(attrs={'class': 'form-control shadow-sm rounded', 'style': 'color: blue;'}))
    oSec08Field13 = forms.CharField(required=False, widget=forms.TextInput(attrs={'class': 'form-control shadow-sm rounded', 'readonly': 'readonly', 'style': 'color: blue; font-weight: bold;'}))
    oSec08Field14 = forms.CharField(required=False, widget=forms.TextInput(attrs={'class': 'form-control shadow-sm rounded', 'style': 'color: blue;'}))
    oSec08Field15 = forms.CharField(required=False, widget=forms.TextInput(attrs={'class': 'form-control shadow-sm rounded', 'readonly': 'readonly', 'style': 'color: blue; font-weight: bold;'}))
    oSec08Field16 = forms.CharField(required=False, widget=forms.TextInput(attrs={'class': 'form-control shadow-sm rounded', 'style': 'color: blue;'}))
    oSec08Field17 = forms.CharField(required=False, widget=forms.TextInput(attrs={'class': 'form-control shadow-sm rounded', 'readonly': 'readonly', 'style': 'color: blue; font-weight: bold;'}))
    oSec08Field18 = forms.CharField(required=False, widget=forms.TextInput(attrs={'class': 'form-control shadow-sm rounded', 'style': 'color: blue;'}))
    oSec08Field19 = forms.CharField(required=False, widget=forms.TextInput(attrs={'class': 'form-control shadow-sm rounded', 'readonly': 'readonly', 'style': 'color: blue; font-weight: bold;'}))
    oSec08Field20 = forms.CharField(required=False, widget=forms.TextInput(attrs={'class': 'form-control shadow-sm rounded', 'style': 'color: blue;'}))
    
    oSec09Field01 = forms.CharField(required=False, widget=forms.TextInput(attrs={'class': 'form-control shadow-sm rounded', 'readonly': 'readonly', 'style': 'color: blue; font-weight: bold;'}))
    oSec09Field02 = forms.CharField(required=False, widget=forms.TextInput(attrs={'class': 'form-control shadow-sm rounded', 'style': 'color: blue;'}))
    oSec09Field03 = forms.CharField(required=False, widget=forms.TextInput(attrs={'class': 'form-control shadow-sm rounded', 'readonly': 'readonly', 'style': 'color: blue; font-weight: bold;'}))
    oSec09Field04 = forms.CharField(required=False, widget=forms.TextInput(attrs={'class': 'form-control shadow-sm rounded', 'style': 'color: blue;'}))
    oSec09Field05 = forms.CharField(required=False, widget=forms.TextInput(attrs={'class': 'form-control shadow-sm rounded', 'readonly': 'readonly', 'style': 'color: blue; font-weight: bold;'}))
    oSec09Field06 = forms.CharField(required=False, widget=forms.TextInput(attrs={'class': 'form-control shadow-sm rounded', 'style': 'color: blue;'}))
    oSec09Field07 = forms.CharField(required=False, widget=forms.TextInput(attrs={'class': 'form-control shadow-sm rounded', 'readonly': 'readonly', 'style': 'color: blue; font-weight: bold;'}))
    oSec09Field08 = forms.CharField(required=False, widget=forms.TextInput(attrs={'class': 'form-control shadow-sm rounded', 'style': 'color: blue;'}))
    oSec09Field09 = forms.CharField(required=False, widget=forms.TextInput(attrs={'class': 'form-control shadow-sm rounded', 'readonly': 'readonly', 'style': 'color: blue; font-weight: bold;'}))
    oSec09Field10 = forms.CharField(required=False, widget=forms.TextInput(attrs={'class': 'form-control shadow-sm rounded', 'style': 'color: blue;'}))    
    oSec09Field11 = forms.CharField(required=False, widget=forms.TextInput(attrs={'class': 'form-control shadow-sm rounded', 'readonly': 'readonly', 'style': 'color: blue; font-weight: bold;'}))
    oSec09Field12 = forms.CharField(required=False, widget=forms.TextInput(attrs={'class': 'form-control shadow-sm rounded', 'style': 'color: blue;'}))
    oSec09Field13 = forms.CharField(required=False, widget=forms.TextInput(attrs={'class': 'form-control shadow-sm rounded', 'readonly': 'readonly', 'style': 'color: blue; font-weight: bold;'}))
    oSec09Field14 = forms.CharField(required=False, widget=forms.TextInput(attrs={'class': 'form-control shadow-sm rounded', 'style': 'color: blue;'}))
    oSec09Field15 = forms.CharField(required=False, widget=forms.TextInput(attrs={'class': 'form-control shadow-sm rounded', 'readonly': 'readonly', 'style': 'color: blue; font-weight: bold;'}))
    oSec09Field16 = forms.CharField(required=False, widget=forms.TextInput(attrs={'class': 'form-control shadow-sm rounded', 'style': 'color: blue;'}))
    oSec09Field17 = forms.CharField(required=False, widget=forms.TextInput(attrs={'class': 'form-control shadow-sm rounded', 'readonly': 'readonly', 'style': 'color: blue; font-weight: bold;'}))
    oSec09Field18 = forms.CharField(required=False, widget=forms.TextInput(attrs={'class': 'form-control shadow-sm rounded', 'style': 'color: blue;'}))
    oSec09Field19 = forms.CharField(required=False, widget=forms.TextInput(attrs={'class': 'form-control shadow-sm rounded', 'readonly': 'readonly', 'style': 'color: blue; font-weight: bold;'}))
    oSec09Field20 = forms.CharField(required=False, widget=forms.TextInput(attrs={'class': 'form-control shadow-sm rounded', 'style': 'color: blue;'}))
    
    oSec10Field01 = forms.CharField(required=False, widget=forms.TextInput(attrs={'class': 'form-control shadow-sm rounded', 'readonly': 'readonly', 'style': 'color: blue; font-weight: bold;'}))
    oSec10Field02 = forms.CharField(required=False, widget=forms.TextInput(attrs={'class': 'form-control shadow-sm rounded', 'style': 'color: blue;'}))
    oSec10Field03 = forms.CharField(required=False, widget=forms.TextInput(attrs={'class': 'form-control shadow-sm rounded', 'readonly': 'readonly', 'style': 'color: blue; font-weight: bold;'}))
    oSec10Field04 = forms.CharField(required=False, widget=forms.TextInput(attrs={'class': 'form-control shadow-sm rounded', 'style': 'color: blue;'}))
    oSec10Field05 = forms.CharField(required=False, widget=forms.TextInput(attrs={'class': 'form-control shadow-sm rounded', 'readonly': 'readonly', 'style': 'color: blue; font-weight: bold;'}))
    oSec10Field06 = forms.CharField(required=False, widget=forms.TextInput(attrs={'class': 'form-control shadow-sm rounded', 'style': 'color: blue;'}))
    oSec10Field07 = forms.CharField(required=False, widget=forms.TextInput(attrs={'class': 'form-control shadow-sm rounded', 'readonly': 'readonly', 'style': 'color: blue; font-weight: bold;'}))
    oSec10Field08 = forms.CharField(required=False, widget=forms.TextInput(attrs={'class': 'form-control shadow-sm rounded', 'style': 'color: blue;'}))
    oSec10Field09 = forms.CharField(required=False, widget=forms.TextInput(attrs={'class': 'form-control shadow-sm rounded', 'readonly': 'readonly', 'style': 'color: blue; font-weight: bold;'}))
    oSec10Field10 = forms.CharField(required=False, widget=forms.TextInput(attrs={'class': 'form-control shadow-sm rounded', 'style': 'color: blue;'}))    
    oSec10Field11 = forms.CharField(required=False, widget=forms.TextInput(attrs={'class': 'form-control shadow-sm rounded', 'readonly': 'readonly', 'style': 'color: blue; font-weight: bold;'}))
    oSec10Field12 = forms.CharField(required=False, widget=forms.TextInput(attrs={'class': 'form-control shadow-sm rounded', 'style': 'color: blue;'}))
    oSec10Field13 = forms.CharField(required=False, widget=forms.TextInput(attrs={'class': 'form-control shadow-sm rounded', 'readonly': 'readonly', 'style': 'color: blue; font-weight: bold;'}))
    oSec10Field14 = forms.CharField(required=False, widget=forms.TextInput(attrs={'class': 'form-control shadow-sm rounded', 'style': 'color: blue;'}))
    oSec10Field15 = forms.CharField(required=False, widget=forms.TextInput(attrs={'class': 'form-control shadow-sm rounded', 'readonly': 'readonly', 'style': 'color: blue; font-weight: bold;'}))
    oSec10Field16 = forms.CharField(required=False, widget=forms.TextInput(attrs={'class': 'form-control shadow-sm rounded', 'style': 'color: blue;'}))
    oSec10Field17 = forms.CharField(required=False, widget=forms.TextInput(attrs={'class': 'form-control shadow-sm rounded', 'readonly': 'readonly', 'style': 'color: blue; font-weight: bold;'}))
    oSec10Field18 = forms.CharField(required=False, widget=forms.TextInput(attrs={'class': 'form-control shadow-sm rounded', 'style': 'color: blue;'}))
    oSec10Field19 = forms.CharField(required=False, widget=forms.TextInput(attrs={'class': 'form-control shadow-sm rounded', 'readonly': 'readonly', 'style': 'color: blue; font-weight: bold;'}))
    oSec10Field20 = forms.CharField(required=False, widget=forms.TextInput(attrs={'class': 'form-control shadow-sm rounded', 'style': 'color: blue;'}))
    
    
    
    
    
    

    def __init__(self, form_type=None, *args, **kwargs):
        user = kwargs.pop('user', None)  # Get the logged-in user
        super().__init__(*args, **kwargs)
        
        form_name = form_type

        # Determine the user's company
        user_company = None
        if user:
            user_company_instance = UserCompany.objects.filter(user=user).first()
            if user_company_instance:
                user_company = user_company_instance.company

        # Fetch field configurations for the specific company
        field_configs = FormFieldConfig.objects.filter(form_name=form_name)
        
        if user_company:
            field_configs = field_configs.filter(company=user_company)  # Filter by company

        config_dict = {config.field_name: config for config in field_configs}

        for field_name, field in self.fields.items():
            if field_name in config_dict:
                field.label = config_dict[field_name].label  # Set label from DB
                if not field.initial:  # Only set if no initial value is passed
                    field.initial = config_dict[field_name].initial_value
                
                # Hide field if its visibility is set to "Hide"
                if config_dict[field_name].visibility == "Hide":
                    field.widget.attrs.update({'style': 'display: none;'})

    def save(self, commit=True):
        instance = Machine(
            project=self.cleaned_data.get('project', None),  # Allow None for empty field
            oSec01Field01=self.cleaned_data.get('oSec01Field01', ''),  
            oSec01Field02=self.cleaned_data.get('oSec01Field02', ''),  
            oSec01Field03=self.cleaned_data.get('oSec01Field03', ''),  
            oSec01Field04=self.cleaned_data.get('oSec01Field04', ''),  
            oSec01Field05=self.cleaned_data.get('oSec01Field05', ''),  
            oSec01Field06=self.cleaned_data.get('oSec01Field06', ''),  
            oSec01Field07=self.cleaned_data.get('oSec01Field07', ''),  
            oSec01Field08=self.cleaned_data.get('oSec01Field08', ''),  
            oSec01Field09=self.cleaned_data.get('oSec01Field09', ''),  
            oSec01Field10=self.cleaned_data.get('oSec01Field10', ''),  
            oSec01Field11=self.cleaned_data.get('oSec01Field11', ''),  
            oSec01Field12=self.cleaned_data.get('oSec01Field12', ''),  
            oSec01Field13=self.cleaned_data.get('oSec01Field13', ''),  
            oSec01Field14=self.cleaned_data.get('oSec01Field14', ''),  
            oSec01Field15=self.cleaned_data.get('oSec01Field15', ''),  
            oSec01Field16=self.cleaned_data.get('oSec01Field16', ''),  
            oSec01Field17=self.cleaned_data.get('oSec01Field17', ''),  
            oSec01Field18=self.cleaned_data.get('oSec01Field18', ''),  
            oSec01Field19=self.cleaned_data.get('oSec01Field19', ''),  
            oSec01Field20=self.cleaned_data.get('oSec01Field20', ''),  
            
            
            oSec02Field01=self.cleaned_data.get('oSec02Field01', ''),  
            oSec02Field02=self.cleaned_data.get('oSec02Field02', ''),  
            oSec02Field03=self.cleaned_data.get('oSec02Field03', ''),  
            oSec02Field04=self.cleaned_data.get('oSec02Field04', ''),  
            oSec02Field05=self.cleaned_data.get('oSec02Field05', ''),  
            oSec02Field06=self.cleaned_data.get('oSec02Field06', ''),  
            oSec02Field07=self.cleaned_data.get('oSec02Field07', ''),  
            oSec02Field08=self.cleaned_data.get('oSec02Field08', ''),  
            oSec02Field09=self.cleaned_data.get('oSec02Field09', ''),  
            oSec02Field10=self.cleaned_data.get('oSec02Field10', ''),  
            oSec02Field11=self.cleaned_data.get('oSec02Field11', ''),  
            oSec02Field12=self.cleaned_data.get('oSec02Field12', ''),  
            oSec02Field13=self.cleaned_data.get('oSec02Field13', ''),  
            oSec02Field14=self.cleaned_data.get('oSec02Field14', ''),  
            oSec02Field15=self.cleaned_data.get('oSec02Field15', ''),  
            oSec02Field16=self.cleaned_data.get('oSec02Field16', ''),  
            oSec02Field17=self.cleaned_data.get('oSec02Field17', ''),  
            oSec02Field18=self.cleaned_data.get('oSec02Field18', ''),  
            oSec02Field19=self.cleaned_data.get('oSec02Field19', ''),  
            oSec02Field20=self.cleaned_data.get('oSec02Field20', ''),  
            
            
            oSec03Field01=self.cleaned_data.get('oSec03Field01', ''),  
            oSec03Field02=self.cleaned_data.get('oSec03Field02', ''),  
            oSec03Field03=self.cleaned_data.get('oSec03Field03', ''),  
            oSec03Field04=self.cleaned_data.get('oSec03Field04', ''),  
            oSec03Field05=self.cleaned_data.get('oSec03Field05', ''),  
            oSec03Field06=self.cleaned_data.get('oSec03Field06', ''),  
            oSec03Field07=self.cleaned_data.get('oSec03Field07', ''),  
            oSec03Field08=self.cleaned_data.get('oSec03Field08', ''),  
            oSec03Field09=self.cleaned_data.get('oSec03Field09', ''),  
            oSec03Field10=self.cleaned_data.get('oSec03Field10', ''),  
            oSec03Field11=self.cleaned_data.get('oSec03Field11', ''),  
            oSec03Field12=self.cleaned_data.get('oSec03Field12', ''),  
            oSec03Field13=self.cleaned_data.get('oSec03Field13', ''),  
            oSec03Field14=self.cleaned_data.get('oSec03Field14', ''),  
            oSec03Field15=self.cleaned_data.get('oSec03Field15', ''),  
            oSec03Field16=self.cleaned_data.get('oSec03Field16', ''),  
            oSec03Field17=self.cleaned_data.get('oSec03Field17', ''),  
            oSec03Field18=self.cleaned_data.get('oSec03Field18', ''),  
            oSec03Field19=self.cleaned_data.get('oSec03Field19', ''),  
            oSec03Field20=self.cleaned_data.get('oSec03Field20', ''),  
            
            
            oSec04Field01=self.cleaned_data.get('oSec04Field01', ''),  
            oSec04Field02=self.cleaned_data.get('oSec04Field02', ''),  
            oSec04Field03=self.cleaned_data.get('oSec04Field03', ''),  
            oSec04Field04=self.cleaned_data.get('oSec04Field04', ''),  
            oSec04Field05=self.cleaned_data.get('oSec04Field05', ''),  
            oSec04Field06=self.cleaned_data.get('oSec04Field06', ''),  
            oSec04Field07=self.cleaned_data.get('oSec04Field07', ''),  
            oSec04Field08=self.cleaned_data.get('oSec04Field08', ''),  
            oSec04Field09=self.cleaned_data.get('oSec04Field09', ''),  
            oSec04Field10=self.cleaned_data.get('oSec04Field10', ''),  
            oSec04Field11=self.cleaned_data.get('oSec04Field11', ''),  
            oSec04Field12=self.cleaned_data.get('oSec04Field12', ''),  
            oSec04Field13=self.cleaned_data.get('oSec04Field13', ''),  
            oSec04Field14=self.cleaned_data.get('oSec04Field14', ''),  
            oSec04Field15=self.cleaned_data.get('oSec04Field15', ''),  
            oSec04Field16=self.cleaned_data.get('oSec04Field16', ''),  
            oSec04Field17=self.cleaned_data.get('oSec04Field17', ''),  
            oSec04Field18=self.cleaned_data.get('oSec04Field18', ''),  
            oSec04Field19=self.cleaned_data.get('oSec04Field19', ''),  
            oSec04Field20=self.cleaned_data.get('oSec04Field20', ''),  
            
            
            oSec05Field01=self.cleaned_data.get('oSec05Field01', ''),  
            oSec05Field02=self.cleaned_data.get('oSec05Field02', ''),  
            oSec05Field03=self.cleaned_data.get('oSec05Field03', ''),  
            oSec05Field04=self.cleaned_data.get('oSec05Field04', ''),  
            oSec05Field05=self.cleaned_data.get('oSec05Field05', ''),  
            oSec05Field06=self.cleaned_data.get('oSec05Field06', ''),  
            oSec05Field07=self.cleaned_data.get('oSec05Field07', ''),  
            oSec05Field08=self.cleaned_data.get('oSec05Field08', ''),  
            oSec05Field09=self.cleaned_data.get('oSec05Field09', ''),  
            oSec05Field10=self.cleaned_data.get('oSec05Field10', ''),  
            oSec05Field11=self.cleaned_data.get('oSec05Field11', ''),  
            oSec05Field12=self.cleaned_data.get('oSec05Field12', ''),  
            oSec05Field13=self.cleaned_data.get('oSec05Field13', ''),  
            oSec05Field14=self.cleaned_data.get('oSec05Field14', ''),  
            oSec05Field15=self.cleaned_data.get('oSec05Field15', ''),  
            oSec05Field16=self.cleaned_data.get('oSec05Field16', ''),  
            oSec05Field17=self.cleaned_data.get('oSec05Field17', ''),  
            oSec05Field18=self.cleaned_data.get('oSec05Field18', ''),  
            oSec05Field19=self.cleaned_data.get('oSec05Field19', ''),  
            oSec05Field20=self.cleaned_data.get('oSec05Field20', ''),  
            
            
            oSec06Field01=self.cleaned_data.get('oSec06Field01', ''),  
            oSec06Field02=self.cleaned_data.get('oSec06Field02', ''),  
            oSec06Field03=self.cleaned_data.get('oSec06Field03', ''),  
            oSec06Field04=self.cleaned_data.get('oSec06Field04', ''),  
            oSec06Field05=self.cleaned_data.get('oSec06Field05', ''),  
            oSec06Field06=self.cleaned_data.get('oSec06Field06', ''),  
            oSec06Field07=self.cleaned_data.get('oSec06Field07', ''),  
            oSec06Field08=self.cleaned_data.get('oSec06Field08', ''),  
            oSec06Field09=self.cleaned_data.get('oSec06Field09', ''),  
            oSec06Field10=self.cleaned_data.get('oSec06Field10', ''),  
            oSec06Field11=self.cleaned_data.get('oSec06Field11', ''),  
            oSec06Field12=self.cleaned_data.get('oSec06Field12', ''),  
            oSec06Field13=self.cleaned_data.get('oSec06Field13', ''),  
            oSec06Field14=self.cleaned_data.get('oSec06Field14', ''),  
            oSec06Field15=self.cleaned_data.get('oSec06Field15', ''),  
            oSec06Field16=self.cleaned_data.get('oSec06Field16', ''),  
            oSec06Field17=self.cleaned_data.get('oSec06Field17', ''),  
            oSec06Field18=self.cleaned_data.get('oSec06Field18', ''),  
            oSec06Field19=self.cleaned_data.get('oSec06Field19', ''),  
            oSec06Field20=self.cleaned_data.get('oSec06Field20', ''),  
            
            
            oSec07Field01=self.cleaned_data.get('oSec07Field01', ''),  
            oSec07Field02=self.cleaned_data.get('oSec07Field02', ''),  
            oSec07Field03=self.cleaned_data.get('oSec07Field03', ''),  
            oSec07Field04=self.cleaned_data.get('oSec07Field04', ''),  
            oSec07Field05=self.cleaned_data.get('oSec07Field05', ''),  
            oSec07Field06=self.cleaned_data.get('oSec07Field06', ''),  
            oSec07Field07=self.cleaned_data.get('oSec07Field07', ''),  
            oSec07Field08=self.cleaned_data.get('oSec07Field08', ''),  
            oSec07Field09=self.cleaned_data.get('oSec07Field09', ''),  
            oSec07Field10=self.cleaned_data.get('oSec07Field10', ''),  
            oSec07Field11=self.cleaned_data.get('oSec07Field11', ''),  
            oSec07Field12=self.cleaned_data.get('oSec07Field12', ''),  
            oSec07Field13=self.cleaned_data.get('oSec07Field13', ''),  
            oSec07Field14=self.cleaned_data.get('oSec07Field14', ''),  
            oSec07Field15=self.cleaned_data.get('oSec07Field15', ''),  
            oSec07Field16=self.cleaned_data.get('oSec07Field16', ''),  
            oSec07Field17=self.cleaned_data.get('oSec07Field17', ''),  
            oSec07Field18=self.cleaned_data.get('oSec07Field18', ''),  
            oSec07Field19=self.cleaned_data.get('oSec07Field19', ''),  
            oSec07Field20=self.cleaned_data.get('oSec07Field20', ''),  
            
            
            oSec08Field01=self.cleaned_data.get('oSec08Field01', ''),  
            oSec08Field02=self.cleaned_data.get('oSec08Field02', ''),  
            oSec08Field03=self.cleaned_data.get('oSec08Field03', ''),  
            oSec08Field04=self.cleaned_data.get('oSec08Field04', ''),  
            oSec08Field05=self.cleaned_data.get('oSec08Field05', ''),  
            oSec08Field06=self.cleaned_data.get('oSec08Field06', ''),  
            oSec08Field07=self.cleaned_data.get('oSec08Field07', ''),  
            oSec08Field08=self.cleaned_data.get('oSec08Field08', ''),  
            oSec08Field09=self.cleaned_data.get('oSec08Field09', ''),  
            oSec08Field10=self.cleaned_data.get('oSec08Field10', ''),  
            oSec08Field11=self.cleaned_data.get('oSec08Field11', ''),  
            oSec08Field12=self.cleaned_data.get('oSec08Field12', ''),  
            oSec08Field13=self.cleaned_data.get('oSec08Field13', ''),  
            oSec08Field14=self.cleaned_data.get('oSec08Field14', ''),  
            oSec08Field15=self.cleaned_data.get('oSec08Field15', ''),  
            oSec08Field16=self.cleaned_data.get('oSec08Field16', ''),  
            oSec08Field17=self.cleaned_data.get('oSec08Field17', ''),  
            oSec08Field18=self.cleaned_data.get('oSec08Field18', ''),  
            oSec08Field19=self.cleaned_data.get('oSec08Field19', ''),  
            oSec08Field20=self.cleaned_data.get('oSec08Field20', ''),  
            
            
            oSec09Field01=self.cleaned_data.get('oSec09Field01', ''),  
            oSec09Field02=self.cleaned_data.get('oSec09Field02', ''),  
            oSec09Field03=self.cleaned_data.get('oSec09Field03', ''),  
            oSec09Field04=self.cleaned_data.get('oSec09Field04', ''),  
            oSec09Field05=self.cleaned_data.get('oSec09Field05', ''),  
            oSec09Field06=self.cleaned_data.get('oSec09Field06', ''),  
            oSec09Field07=self.cleaned_data.get('oSec09Field07', ''),  
            oSec09Field08=self.cleaned_data.get('oSec09Field08', ''),  
            oSec09Field09=self.cleaned_data.get('oSec09Field09', ''),  
            oSec09Field10=self.cleaned_data.get('oSec09Field10', ''),  
            oSec09Field11=self.cleaned_data.get('oSec09Field11', ''),  
            oSec09Field12=self.cleaned_data.get('oSec09Field12', ''),  
            oSec09Field13=self.cleaned_data.get('oSec09Field13', ''),  
            oSec09Field14=self.cleaned_data.get('oSec09Field14', ''),  
            oSec09Field15=self.cleaned_data.get('oSec09Field15', ''),  
            oSec09Field16=self.cleaned_data.get('oSec09Field16', ''),  
            oSec09Field17=self.cleaned_data.get('oSec09Field17', ''),  
            oSec09Field18=self.cleaned_data.get('oSec09Field18', ''),  
            oSec09Field19=self.cleaned_data.get('oSec09Field19', ''),  
            oSec09Field20=self.cleaned_data.get('oSec09Field20', ''),  
            
            
            oSec10Field01=self.cleaned_data.get('oSec10Field01', ''),  
            oSec10Field02=self.cleaned_data.get('oSec10Field02', ''),  
            oSec10Field03=self.cleaned_data.get('oSec10Field03', ''),  
            oSec10Field04=self.cleaned_data.get('oSec10Field04', ''),  
            oSec10Field05=self.cleaned_data.get('oSec10Field05', ''),  
            oSec10Field06=self.cleaned_data.get('oSec10Field06', ''),  
            oSec10Field07=self.cleaned_data.get('oSec10Field07', ''),  
            oSec10Field08=self.cleaned_data.get('oSec10Field08', ''),  
            oSec10Field09=self.cleaned_data.get('oSec10Field09', ''),  
            oSec10Field10=self.cleaned_data.get('oSec10Field10', ''),  
            oSec10Field11=self.cleaned_data.get('oSec10Field11', ''),  
            oSec10Field12=self.cleaned_data.get('oSec10Field12', ''),  
            oSec10Field13=self.cleaned_data.get('oSec10Field13', ''),  
            oSec10Field14=self.cleaned_data.get('oSec10Field14', ''),  
            oSec10Field15=self.cleaned_data.get('oSec10Field15', ''),  
            oSec10Field16=self.cleaned_data.get('oSec10Field16', ''),  
            oSec10Field17=self.cleaned_data.get('oSec10Field17', ''),  
            oSec10Field18=self.cleaned_data.get('oSec10Field18', ''),  
            oSec10Field19=self.cleaned_data.get('oSec10Field19', ''),  
            oSec10Field20=self.cleaned_data.get('oSec10Field20', ''),  
            
            
            
        )
        if commit:
            instance.save()
        return instance