from django import forms
from .models import modelcalc, modelcalc_log, API_Keys
from Apps.aAppMechanical.models import FormFieldConfig
from Apps.aAppProject.models import APP_Project
from Apps.aAppMechanical.models import UserCompany



class FormCalculationSheet(forms.Form):
    project = forms.ModelChoiceField(
        queryset=APP_Project.objects.all(),
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
    oSec01Field21 = forms.CharField(required=False, widget=forms.TextInput(attrs={'class': 'form-control shadow-sm rounded', 'readonly': 'readonly', 'style': 'color: blue; font-weight: bold;'}))
    oSec01Field22 = forms.CharField(required=False, widget=forms.TextInput(attrs={'class': 'form-control shadow-sm rounded', 'style': 'color: blue;'}))
    oSec01Field23 = forms.CharField(required=False, widget=forms.TextInput(attrs={'class': 'form-control shadow-sm rounded', 'readonly': 'readonly', 'style': 'color: blue; font-weight: bold;'}))
    oSec01Field24 = forms.CharField(required=False, widget=forms.TextInput(attrs={'class': 'form-control shadow-sm rounded', 'style': 'color: blue;'}))
    oSec01Field25 = forms.CharField(required=False, widget=forms.TextInput(attrs={'class': 'form-control shadow-sm rounded', 'readonly': 'readonly', 'style': 'color: blue; font-weight: bold;'}))
    oSec01Field26 = forms.CharField(required=False, widget=forms.TextInput(attrs={'class': 'form-control shadow-sm rounded', 'style': 'color: blue;'}))
    oSec01Field27 = forms.CharField(required=False, widget=forms.TextInput(attrs={'class': 'form-control shadow-sm rounded', 'readonly': 'readonly', 'style': 'color: blue; font-weight: bold;'}))
    oSec01Field28 = forms.CharField(required=False, widget=forms.TextInput(attrs={'class': 'form-control shadow-sm rounded', 'style': 'color: blue;'}))
    oSec01Field29 = forms.CharField(required=False, widget=forms.TextInput(attrs={'class': 'form-control shadow-sm rounded', 'readonly': 'readonly', 'style': 'color: blue; font-weight: bold;'}))
    oSec01Field30 = forms.CharField(required=False, widget=forms.TextInput(attrs={'class': 'form-control shadow-sm rounded', 'style': 'color: blue;'}))
    
    
    oSec02Field01 = forms.CharField(required=False, widget=forms.TextInput(attrs={'class': 'form-control shadow-sm rounded', 'readonly': 'readonly', 'style': 'color: blue; font-weight: bold;'}))
    oSec02Field02 = forms.CharField(required=False, widget=forms.TextInput(attrs={'class': 'form-control shadow-sm rounded', 'readonly': 'readonly', 'style': 'color: blue; font-weight: bold;'}))
    oSec02Field03 = forms.CharField(required=False, widget=forms.TextInput(attrs={'class': 'form-control shadow-sm rounded', 'readonly': 'readonly', 'style': 'color: blue; font-weight: bold;'}))
    oSec02Field04 = forms.CharField(required=False, widget=forms.TextInput(attrs={'class': 'form-control shadow-sm rounded', 'readonly': 'readonly', 'style': 'color: blue; font-weight: bold;'}))
    oSec02Field05 = forms.CharField(required=False, widget=forms.TextInput(attrs={'class': 'form-control shadow-sm rounded', 'readonly': 'readonly', 'style': 'color: blue; font-weight: bold;'}))
    oSec02Field06 = forms.CharField(required=False, widget=forms.TextInput(attrs={'class': 'form-control shadow-sm rounded', 'readonly': 'readonly', 'style': 'color: blue; font-weight: bold;'}))
    oSec02Field07 = forms.CharField(required=False, widget=forms.TextInput(attrs={'class': 'form-control shadow-sm rounded', 'readonly': 'readonly', 'style': 'color: blue; font-weight: bold;'}))
    oSec02Field08 = forms.CharField(required=False, widget=forms.TextInput(attrs={'class': 'form-control shadow-sm rounded', 'readonly': 'readonly', 'style': 'color: blue; font-weight: bold;'}))
    oSec02Field09 = forms.CharField(required=False, widget=forms.TextInput(attrs={'class': 'form-control shadow-sm rounded', 'readonly': 'readonly', 'style': 'color: blue; font-weight: bold;'}))
    oSec02Field10 = forms.CharField(required=False, widget=forms.TextInput(attrs={'class': 'form-control shadow-sm rounded', 'readonly': 'readonly', 'style': 'color: blue; font-weight: bold;'}))
    oSec02Field11 = forms.CharField(required=False, widget=forms.TextInput(attrs={'class': 'form-control shadow-sm rounded', 'readonly': 'readonly', 'style': 'color: blue; font-weight: bold;'}))
    oSec02Field12 = forms.CharField(required=False, widget=forms.TextInput(attrs={'class': 'form-control shadow-sm rounded', 'readonly': 'readonly', 'style': 'color: blue; font-weight: bold;'}))
    oSec02Field13 = forms.CharField(required=False, widget=forms.TextInput(attrs={'class': 'form-control shadow-sm rounded', 'readonly': 'readonly', 'style': 'color: blue; font-weight: bold;'}))
    oSec02Field14 = forms.CharField(required=False, widget=forms.TextInput(attrs={'class': 'form-control shadow-sm rounded', 'readonly': 'readonly', 'style': 'color: blue; font-weight: bold;'}))
    oSec02Field15 = forms.CharField(required=False, widget=forms.TextInput(attrs={'class': 'form-control shadow-sm rounded', 'readonly': 'readonly', 'style': 'color: blue; font-weight: bold;'}))
    oSec02Field16 = forms.CharField(required=False, widget=forms.TextInput(attrs={'class': 'form-control shadow-sm rounded', 'readonly': 'readonly', 'style': 'color: blue; font-weight: bold;'}))
    oSec02Field17 = forms.CharField(required=False, widget=forms.TextInput(attrs={'class': 'form-control shadow-sm rounded', 'readonly': 'readonly', 'style': 'color: blue; font-weight: bold;'}))
    oSec02Field18 = forms.CharField(required=False, widget=forms.TextInput(attrs={'class': 'form-control shadow-sm rounded', 'readonly': 'readonly', 'style': 'color: blue; font-weight: bold;'}))
    oSec02Field19 = forms.CharField(required=False, widget=forms.TextInput(attrs={'class': 'form-control shadow-sm rounded', 'readonly': 'readonly', 'style': 'color: blue; font-weight: bold;'}))
    oSec02Field20 = forms.CharField(required=False, widget=forms.TextInput(attrs={'class': 'form-control shadow-sm rounded', 'readonly': 'readonly', 'style': 'color: blue; font-weight: bold;'}))
    oSec02Field21 = forms.CharField(required=False, widget=forms.TextInput(attrs={'class': 'form-control shadow-sm rounded', 'readonly': 'readonly', 'style': 'color: blue; font-weight: bold;'}))
    oSec02Field22 = forms.CharField(required=False, widget=forms.TextInput(attrs={'class': 'form-control shadow-sm rounded', 'readonly': 'readonly', 'style': 'color: blue; font-weight: bold;'}))
    oSec02Field23 = forms.CharField(required=False, widget=forms.TextInput(attrs={'class': 'form-control shadow-sm rounded', 'readonly': 'readonly', 'style': 'color: blue; font-weight: bold;'}))
    oSec02Field24 = forms.CharField(required=False, widget=forms.TextInput(attrs={'class': 'form-control shadow-sm rounded', 'readonly': 'readonly', 'style': 'color: blue; font-weight: bold;'}))
    oSec02Field25 = forms.CharField(required=False, widget=forms.TextInput(attrs={'class': 'form-control shadow-sm rounded', 'readonly': 'readonly', 'style': 'color: blue; font-weight: bold;'}))
    oSec02Field26 = forms.CharField(required=False, widget=forms.TextInput(attrs={'class': 'form-control shadow-sm rounded', 'readonly': 'readonly', 'style': 'color: blue; font-weight: bold;'}))
    oSec02Field27 = forms.CharField(required=False, widget=forms.TextInput(attrs={'class': 'form-control shadow-sm rounded', 'readonly': 'readonly', 'style': 'color: blue; font-weight: bold;'}))
    oSec02Field28 = forms.CharField(required=False, widget=forms.TextInput(attrs={'class': 'form-control shadow-sm rounded', 'readonly': 'readonly', 'style': 'color: blue; font-weight: bold;'}))
    oSec02Field29 = forms.CharField(required=False, widget=forms.TextInput(attrs={'class': 'form-control shadow-sm rounded', 'readonly': 'readonly', 'style': 'color: blue; font-weight: bold;'}))
    oSec02Field30 = forms.CharField(required=False, widget=forms.TextInput(attrs={'class': 'form-control shadow-sm rounded', 'readonly': 'readonly', 'style': 'color: blue; font-weight: bold;'}))

    
    
    
    
    
    

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

        
        # Fetch field configurations
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
        instance = modelcalc(
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
            oSec01Field21=self.cleaned_data.get('oSec01Field21', ''),  
            oSec01Field22=self.cleaned_data.get('oSec01Field22', ''),  
            oSec01Field23=self.cleaned_data.get('oSec01Field23', ''),  
            oSec01Field24=self.cleaned_data.get('oSec01Field24', ''),  
            oSec01Field25=self.cleaned_data.get('oSec01Field25', ''),  
            oSec01Field26=self.cleaned_data.get('oSec01Field26', ''),  
            oSec01Field27=self.cleaned_data.get('oSec01Field27', ''),  
            oSec01Field28=self.cleaned_data.get('oSec01Field28', ''),  
            oSec01Field29=self.cleaned_data.get('oSec01Field29', ''),  
            oSec01Field30=self.cleaned_data.get('oSec01Field30', ''),  
            
            
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
            oSec02Field21=self.cleaned_data.get('oSec02Field21', ''),  
            oSec02Field22=self.cleaned_data.get('oSec02Field22', ''),  
            oSec02Field23=self.cleaned_data.get('oSec02Field23', ''),  
            oSec02Field24=self.cleaned_data.get('oSec02Field24', ''),  
            oSec02Field25=self.cleaned_data.get('oSec02Field25', ''),  
            oSec02Field26=self.cleaned_data.get('oSec02Field26', ''),  
            oSec02Field27=self.cleaned_data.get('oSec02Field27', ''),  
            oSec02Field28=self.cleaned_data.get('oSec02Field28', ''),  
            oSec02Field29=self.cleaned_data.get('oSec02Field29', ''),  
            oSec02Field30=self.cleaned_data.get('oSec02Field30', ''),  
            
            
            
            
        )
        if commit:
            instance.save()
        return instance




class FormCalculationSheet_log(forms.Form):
    project = forms.ModelChoiceField(
        queryset=APP_Project.objects.all(),
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
    oSec01Field21 = forms.CharField(required=False, widget=forms.TextInput(attrs={'class': 'form-control shadow-sm rounded', 'readonly': 'readonly', 'style': 'color: blue; font-weight: bold;'}))
    oSec01Field22 = forms.CharField(required=False, widget=forms.TextInput(attrs={'class': 'form-control shadow-sm rounded', 'style': 'color: blue;'}))
    oSec01Field23 = forms.CharField(required=False, widget=forms.TextInput(attrs={'class': 'form-control shadow-sm rounded', 'readonly': 'readonly', 'style': 'color: blue; font-weight: bold;'}))
    oSec01Field24 = forms.CharField(required=False, widget=forms.TextInput(attrs={'class': 'form-control shadow-sm rounded', 'style': 'color: blue;'}))
    oSec01Field25 = forms.CharField(required=False, widget=forms.TextInput(attrs={'class': 'form-control shadow-sm rounded', 'readonly': 'readonly', 'style': 'color: blue; font-weight: bold;'}))
    oSec01Field26 = forms.CharField(required=False, widget=forms.TextInput(attrs={'class': 'form-control shadow-sm rounded', 'style': 'color: blue;'}))
    oSec01Field27 = forms.CharField(required=False, widget=forms.TextInput(attrs={'class': 'form-control shadow-sm rounded', 'readonly': 'readonly', 'style': 'color: blue; font-weight: bold;'}))
    oSec01Field28 = forms.CharField(required=False, widget=forms.TextInput(attrs={'class': 'form-control shadow-sm rounded', 'style': 'color: blue;'}))
    oSec01Field29 = forms.CharField(required=False, widget=forms.TextInput(attrs={'class': 'form-control shadow-sm rounded', 'readonly': 'readonly', 'style': 'color: blue; font-weight: bold;'}))
    oSec01Field30 = forms.CharField(required=False, widget=forms.TextInput(attrs={'class': 'form-control shadow-sm rounded', 'style': 'color: blue;'}))
    
    
    oSec02Field01 = forms.CharField(required=False, widget=forms.TextInput(attrs={'class': 'form-control shadow-sm rounded', 'readonly': 'readonly', 'style': 'color: blue; font-weight: bold;'}))
    oSec02Field02 = forms.CharField(required=False, widget=forms.TextInput(attrs={'class': 'form-control shadow-sm rounded', 'readonly': 'readonly', 'style': 'color: blue; font-weight: bold;'}))
    oSec02Field03 = forms.CharField(required=False, widget=forms.TextInput(attrs={'class': 'form-control shadow-sm rounded', 'readonly': 'readonly', 'style': 'color: blue; font-weight: bold;'}))
    oSec02Field04 = forms.CharField(required=False, widget=forms.TextInput(attrs={'class': 'form-control shadow-sm rounded', 'readonly': 'readonly', 'style': 'color: blue; font-weight: bold;'}))
    oSec02Field05 = forms.CharField(required=False, widget=forms.TextInput(attrs={'class': 'form-control shadow-sm rounded', 'readonly': 'readonly', 'style': 'color: blue; font-weight: bold;'}))
    oSec02Field06 = forms.CharField(required=False, widget=forms.TextInput(attrs={'class': 'form-control shadow-sm rounded', 'readonly': 'readonly', 'style': 'color: blue; font-weight: bold;'}))
    oSec02Field07 = forms.CharField(required=False, widget=forms.TextInput(attrs={'class': 'form-control shadow-sm rounded', 'readonly': 'readonly', 'style': 'color: blue; font-weight: bold;'}))
    oSec02Field08 = forms.CharField(required=False, widget=forms.TextInput(attrs={'class': 'form-control shadow-sm rounded', 'readonly': 'readonly', 'style': 'color: blue; font-weight: bold;'}))
    oSec02Field09 = forms.CharField(required=False, widget=forms.TextInput(attrs={'class': 'form-control shadow-sm rounded', 'readonly': 'readonly', 'style': 'color: blue; font-weight: bold;'}))
    oSec02Field10 = forms.CharField(required=False, widget=forms.TextInput(attrs={'class': 'form-control shadow-sm rounded', 'readonly': 'readonly', 'style': 'color: blue; font-weight: bold;'}))
    oSec02Field11 = forms.CharField(required=False, widget=forms.TextInput(attrs={'class': 'form-control shadow-sm rounded', 'readonly': 'readonly', 'style': 'color: blue; font-weight: bold;'}))
    oSec02Field12 = forms.CharField(required=False, widget=forms.TextInput(attrs={'class': 'form-control shadow-sm rounded', 'readonly': 'readonly', 'style': 'color: blue; font-weight: bold;'}))
    oSec02Field13 = forms.CharField(required=False, widget=forms.TextInput(attrs={'class': 'form-control shadow-sm rounded', 'readonly': 'readonly', 'style': 'color: blue; font-weight: bold;'}))
    oSec02Field14 = forms.CharField(required=False, widget=forms.TextInput(attrs={'class': 'form-control shadow-sm rounded', 'readonly': 'readonly', 'style': 'color: blue; font-weight: bold;'}))
    oSec02Field15 = forms.CharField(required=False, widget=forms.TextInput(attrs={'class': 'form-control shadow-sm rounded', 'readonly': 'readonly', 'style': 'color: blue; font-weight: bold;'}))
    oSec02Field16 = forms.CharField(required=False, widget=forms.TextInput(attrs={'class': 'form-control shadow-sm rounded', 'readonly': 'readonly', 'style': 'color: blue; font-weight: bold;'}))
    oSec02Field17 = forms.CharField(required=False, widget=forms.TextInput(attrs={'class': 'form-control shadow-sm rounded', 'readonly': 'readonly', 'style': 'color: blue; font-weight: bold;'}))
    oSec02Field18 = forms.CharField(required=False, widget=forms.TextInput(attrs={'class': 'form-control shadow-sm rounded', 'readonly': 'readonly', 'style': 'color: blue; font-weight: bold;'}))
    oSec02Field19 = forms.CharField(required=False, widget=forms.TextInput(attrs={'class': 'form-control shadow-sm rounded', 'readonly': 'readonly', 'style': 'color: blue; font-weight: bold;'}))
    oSec02Field20 = forms.CharField(required=False, widget=forms.TextInput(attrs={'class': 'form-control shadow-sm rounded', 'readonly': 'readonly', 'style': 'color: blue; font-weight: bold;'}))
    oSec02Field21 = forms.CharField(required=False, widget=forms.TextInput(attrs={'class': 'form-control shadow-sm rounded', 'readonly': 'readonly', 'style': 'color: blue; font-weight: bold;'}))
    oSec02Field22 = forms.CharField(required=False, widget=forms.TextInput(attrs={'class': 'form-control shadow-sm rounded', 'readonly': 'readonly', 'style': 'color: blue; font-weight: bold;'}))
    oSec02Field23 = forms.CharField(required=False, widget=forms.TextInput(attrs={'class': 'form-control shadow-sm rounded', 'readonly': 'readonly', 'style': 'color: blue; font-weight: bold;'}))
    oSec02Field24 = forms.CharField(required=False, widget=forms.TextInput(attrs={'class': 'form-control shadow-sm rounded', 'readonly': 'readonly', 'style': 'color: blue; font-weight: bold;'}))
    oSec02Field25 = forms.CharField(required=False, widget=forms.TextInput(attrs={'class': 'form-control shadow-sm rounded', 'readonly': 'readonly', 'style': 'color: blue; font-weight: bold;'}))
    oSec02Field26 = forms.CharField(required=False, widget=forms.TextInput(attrs={'class': 'form-control shadow-sm rounded', 'readonly': 'readonly', 'style': 'color: blue; font-weight: bold;'}))
    oSec02Field27 = forms.CharField(required=False, widget=forms.TextInput(attrs={'class': 'form-control shadow-sm rounded', 'readonly': 'readonly', 'style': 'color: blue; font-weight: bold;'}))
    oSec02Field28 = forms.CharField(required=False, widget=forms.TextInput(attrs={'class': 'form-control shadow-sm rounded', 'readonly': 'readonly', 'style': 'color: blue; font-weight: bold;'}))
    oSec02Field29 = forms.CharField(required=False, widget=forms.TextInput(attrs={'class': 'form-control shadow-sm rounded', 'readonly': 'readonly', 'style': 'color: blue; font-weight: bold;'}))
    oSec02Field30 = forms.CharField(required=False, widget=forms.TextInput(attrs={'class': 'form-control shadow-sm rounded', 'readonly': 'readonly', 'style': 'color: blue; font-weight: bold;'}))

    
    
    
    
    
    

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

        
        # Fetch field configurations
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
        instance = modelcalc_log(
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
            oSec01Field21=self.cleaned_data.get('oSec01Field21', ''),  
            oSec01Field22=self.cleaned_data.get('oSec01Field22', ''),  
            oSec01Field23=self.cleaned_data.get('oSec01Field23', ''),  
            oSec01Field24=self.cleaned_data.get('oSec01Field24', ''),  
            oSec01Field25=self.cleaned_data.get('oSec01Field25', ''),  
            oSec01Field26=self.cleaned_data.get('oSec01Field26', ''),  
            oSec01Field27=self.cleaned_data.get('oSec01Field27', ''),  
            oSec01Field28=self.cleaned_data.get('oSec01Field28', ''),  
            oSec01Field29=self.cleaned_data.get('oSec01Field29', ''),  
            oSec01Field30=self.cleaned_data.get('oSec01Field30', ''),  
            
            
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
            oSec02Field21=self.cleaned_data.get('oSec02Field21', ''),  
            oSec02Field22=self.cleaned_data.get('oSec02Field22', ''),  
            oSec02Field23=self.cleaned_data.get('oSec02Field23', ''),  
            oSec02Field24=self.cleaned_data.get('oSec02Field24', ''),  
            oSec02Field25=self.cleaned_data.get('oSec02Field25', ''),  
            oSec02Field26=self.cleaned_data.get('oSec02Field26', ''),  
            oSec02Field27=self.cleaned_data.get('oSec02Field27', ''),  
            oSec02Field28=self.cleaned_data.get('oSec02Field28', ''),  
            oSec02Field29=self.cleaned_data.get('oSec02Field29', ''),  
            oSec02Field30=self.cleaned_data.get('oSec02Field30', ''),  
            
            
            
            
        )
        if commit:
            instance.save()
        return instance

class APIkeyForm(forms.ModelForm):
    class Meta:
        model = API_Keys
        fields = ['sheetkey', 'calctype', 'fieldname', 'apikey']
        widgets = {
            'sheetkey': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter the machine sheetkey'}),
            'calctype': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter the API key type'}),
            'fieldname': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter the field name'}),
            'apikey': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter the API key'}),
        }