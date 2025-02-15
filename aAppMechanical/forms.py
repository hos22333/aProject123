from django import forms
from .models import modelcalc
from .models import FormFieldConfig
#######################################


class formCalcMS(forms.Form):
    oSec01Field01 = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control shadow-sm rounded', 'style': 'color: blue;'}))
    oSec01Field02 = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control shadow-sm rounded', 'style': 'color: blue;'}))
    oSec01Field03 = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control shadow-sm rounded', 'style': 'color: blue;'}))
    oSec01Field04 = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control shadow-sm rounded', 'style': 'color: blue;'}))
    oSec01Field05 = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control shadow-sm rounded', 'style': 'color: blue;'}))
    oSec01Field06 = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control shadow-sm rounded', 'style': 'color: blue;'}))
    oSec01Field07 = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control shadow-sm rounded', 'style': 'color: blue;'}))
    oSec01Field08 = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control shadow-sm rounded', 'style': 'color: blue;'}))
    oSec01Field09 = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control shadow-sm rounded', 'style': 'color: blue;'}))
    oSec01Field10 = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control shadow-sm rounded', 'style': 'color: blue;'}))
    oSec01Field11 = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control shadow-sm rounded', 'style': 'color: blue;'}))

    oSec02Field01 = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control shadow-sm rounded', 'readonly': 'readonly', 'style': 'color: blue; font-weight: bold;'}))
    oSec02Field02 = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control shadow-sm rounded', 'readonly': 'readonly', 'style': 'color: blue; font-weight: bold;'}))
    oSec02Field03 = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control shadow-sm rounded', 'readonly': 'readonly', 'style': 'color: blue; font-weight: bold;'}))

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        form_name = 'formCalcMS'
        
        # Fetch field configurations from the database
        field_configs = FormFieldConfig.objects.filter(form_name=form_name)
        config_dict = {config.field_name: config for config in field_configs}

        for field_name, field in self.fields.items():
            if field_name in config_dict:
                field.label = config_dict[field_name].label  # Set label from DB
                if not field.initial:  # Only set if no initial value is passed
                    field.initial = config_dict[field_name].initial_value

    def save(self, commit=True):
        instance = modelcalc(
            oSec01Field01=self.cleaned_data['oSec01Field01'],
            oSec01Field02=self.cleaned_data['oSec01Field02'],
            oSec01Field03=self.cleaned_data['oSec01Field03'],
            oSec01Field04=self.cleaned_data['oSec01Field04'],
            oSec01Field05=self.cleaned_data['oSec01Field05'],
            oSec01Field06=self.cleaned_data['oSec01Field06'],
            oSec01Field07=self.cleaned_data['oSec01Field07'],
            oSec01Field08=self.cleaned_data['oSec01Field08'],
            oSec01Field09=self.cleaned_data['oSec01Field09'],
            oSec01Field10=self.cleaned_data['oSec01Field10'],
            oSec01Field11=self.cleaned_data['oSec01Field11'],
            
            oSec02Field01=self.cleaned_data['oSec02Field01'],
            oSec02Field02=self.cleaned_data['oSec02Field02'],
            oSec02Field03=self.cleaned_data['oSec02Field03'],
        )
        if commit:
            instance.save()
        return instance


class formCalcBC(forms.Form):
    oSec01Field01 = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control shadow-sm rounded', 'style': 'color: blue;'}))
    oSec01Field02 = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control shadow-sm rounded', 'style': 'color: blue;'}))
    oSec01Field03 = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control shadow-sm rounded', 'style': 'color: blue;'}))
    oSec01Field04 = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control shadow-sm rounded', 'style': 'color: blue;'}))
    oSec01Field05 = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control shadow-sm rounded', 'style': 'color: blue;'}))
    oSec01Field06 = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control shadow-sm rounded', 'style': 'color: blue;'}))
    oSec01Field07 = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control shadow-sm rounded', 'style': 'color: blue;'}))

    oSec02Field01 = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control shadow-sm rounded', 'readonly': 'readonly', 'style': 'color: blue; font-weight: bold;'}))
    oSec02Field02 = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control shadow-sm rounded', 'readonly': 'readonly', 'style': 'color: blue; font-weight: bold;'}))
    oSec02Field03 = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control shadow-sm rounded', 'readonly': 'readonly', 'style': 'color: blue; font-weight: bold;'}))

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        form_name = 'formCalcBC'
        
        # Fetch field configurations from the database
        field_configs = FormFieldConfig.objects.filter(form_name=form_name)
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
            oSec01Field01=self.cleaned_data['oSec01Field01'],
            oSec01Field02=self.cleaned_data['oSec01Field02'],
            oSec01Field03=self.cleaned_data['oSec01Field03'],
            oSec01Field04=self.cleaned_data['oSec01Field04'],
            oSec01Field05=self.cleaned_data['oSec01Field05'],
            oSec01Field06=self.cleaned_data['oSec01Field06'],
            oSec01Field07=self.cleaned_data['oSec01Field07'],
            
            oSec02Field01=self.cleaned_data['oSec02Field01'],
            oSec02Field02=self.cleaned_data['oSec02Field02'],
            oSec02Field03=self.cleaned_data['oSec02Field03'],
        )
        if commit:
            instance.save()
        return instance


class formCalcGR(forms.Form):
    oSec01Field01 = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control shadow-sm rounded', 'style': 'color: blue;'}))
    oSec01Field02 = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control shadow-sm rounded', 'style': 'color: blue;'}))
    oSec01Field03 = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control shadow-sm rounded', 'style': 'color: blue;'}))
    oSec01Field04 = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control shadow-sm rounded', 'style': 'color: blue;'}))
    oSec01Field05 = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control shadow-sm rounded', 'style': 'color: blue;'}))
    oSec01Field06 = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control shadow-sm rounded', 'style': 'color: blue;'}))
    oSec01Field07 = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control shadow-sm rounded', 'style': 'color: blue;'}))
    oSec01Field08 = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control shadow-sm rounded', 'style': 'color: blue;'}))

    oSec02Field01 = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control shadow-sm rounded', 'readonly': 'readonly', 'style': 'color: blue; font-weight: bold;'}))
    oSec02Field02 = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control shadow-sm rounded', 'readonly': 'readonly', 'style': 'color: blue; font-weight: bold;'}))
    oSec02Field03 = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control shadow-sm rounded', 'readonly': 'readonly', 'style': 'color: blue; font-weight: bold;'}))
    oSec02Field04 = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control shadow-sm rounded', 'readonly': 'readonly', 'style': 'color: blue; font-weight: bold;'}))
    oSec02Field05 = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control shadow-sm rounded', 'readonly': 'readonly', 'style': 'color: blue; font-weight: bold;'}))
    oSec02Field06 = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control shadow-sm rounded', 'readonly': 'readonly', 'style': 'color: blue; font-weight: bold;'}))

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        form_name = 'formCalcGR'
        
        # Fetch field configurations from the database
        field_configs = FormFieldConfig.objects.filter(form_name=form_name)
        config_dict = {config.field_name: config for config in field_configs}

        for field_name, field in self.fields.items():
            if field_name in config_dict:
                field.label = config_dict[field_name].label  # Set label from DB
                if not field.initial:  # Only set if no initial value is passed
                    field.initial = config_dict[field_name].initial_value

    def save(self, commit=True):
        instance = modelcalc(
            oSec01Field01=self.cleaned_data['oSec01Field01'],
            oSec01Field02=self.cleaned_data['oSec01Field02'],
            oSec01Field03=self.cleaned_data['oSec01Field03'],
            oSec01Field04=self.cleaned_data['oSec01Field04'],
            oSec01Field05=self.cleaned_data['oSec01Field05'],
            oSec01Field06=self.cleaned_data['oSec01Field06'],
            oSec01Field07=self.cleaned_data['oSec01Field07'],
            oSec01Field08=self.cleaned_data['oSec01Field08'],
            
            oSec02Field01=self.cleaned_data['oSec02Field01'],
            oSec02Field02=self.cleaned_data['oSec02Field02'],
            oSec02Field03=self.cleaned_data['oSec02Field03'],
            oSec02Field04=self.cleaned_data['oSec02Field04'],
            oSec02Field05=self.cleaned_data['oSec02Field05'],
            oSec02Field06=self.cleaned_data['oSec02Field06'],
        )
        if commit:
            instance.save()
        return instance

        

class formCalcPS(forms.Form):
    oSec01Field01 = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control shadow-sm rounded', 'style': 'color: blue;'}))
    oSec01Field02 = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control shadow-sm rounded', 'style': 'color: blue;'}))
    oSec01Field03 = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control shadow-sm rounded', 'style': 'color: blue;'}))
    oSec01Field04 = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control shadow-sm rounded', 'style': 'color: blue;'}))

    oSec02Field01 = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control shadow-sm rounded', 'readonly': 'readonly', 'style': 'color: blue; font-weight: bold;'}))
    oSec02Field02 = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control shadow-sm rounded', 'readonly': 'readonly', 'style': 'color: blue; font-weight: bold;'}))
    oSec02Field03 = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control shadow-sm rounded', 'readonly': 'readonly', 'style': 'color: blue; font-weight: bold;'}))
    oSec02Field04 = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control shadow-sm rounded', 'readonly': 'readonly', 'style': 'color: blue; font-weight: bold;'}))
    oSec02Field05 = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control shadow-sm rounded', 'readonly': 'readonly', 'style': 'color: blue; font-weight: bold;'}))

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        form_name = 'formCalcPS'
        
        # Fetch field configurations from the database
        field_configs = FormFieldConfig.objects.filter(form_name=form_name)
        config_dict = {config.field_name: config for config in field_configs}

        for field_name, field in self.fields.items():
            if field_name in config_dict:
                field.label = config_dict[field_name].label  # Set label from DB
                if not field.initial:  # Only set if no initial value is passed
                    field.initial = config_dict[field_name].initial_value

    def save(self, commit=True):
        instance = modelcalc(
            oSec01Field01=self.cleaned_data['oSec01Field01'],
            oSec01Field02=self.cleaned_data['oSec01Field02'],
            oSec01Field03=self.cleaned_data['oSec01Field03'],
            oSec01Field04=self.cleaned_data['oSec01Field04'],
            
            oSec02Field01=self.cleaned_data['oSec02Field01'],
            oSec02Field02=self.cleaned_data['oSec02Field02'],
            oSec02Field03=self.cleaned_data['oSec02Field03'],
            oSec02Field04=self.cleaned_data['oSec02Field04'],
            oSec02Field05=self.cleaned_data['oSec02Field05'],
        )
        if commit:
            instance.save()
        return instance

#######################################

    

class formCalcTH(forms.Form):
    oSec01Field01 = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control shadow-sm rounded', 'style': 'color: blue;'}))
    oSec01Field02 = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control shadow-sm rounded', 'style': 'color: blue;'}))
    oSec01Field03 = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control shadow-sm rounded', 'style': 'color: blue;'}))
    oSec01Field04 = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control shadow-sm rounded', 'style': 'color: blue;'}))

    oSec02Field01 = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control shadow-sm rounded', 'readonly': 'readonly', 'style': 'color: blue; font-weight: bold;'}))
    oSec02Field02 = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control shadow-sm rounded', 'readonly': 'readonly', 'style': 'color: blue; font-weight: bold;'}))
    oSec02Field03 = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control shadow-sm rounded', 'readonly': 'readonly', 'style': 'color: blue; font-weight: bold;'}))
    oSec02Field04 = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control shadow-sm rounded', 'readonly': 'readonly', 'style': 'color: blue; font-weight: bold;'}))
    oSec02Field05 = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control shadow-sm rounded', 'readonly': 'readonly', 'style': 'color: blue; font-weight: bold;'}))

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        form_name = 'formCalcTH'
        
        # Fetch field configurations from the database
        field_configs = FormFieldConfig.objects.filter(form_name=form_name)
        config_dict = {config.field_name: config for config in field_configs}

        for field_name, field in self.fields.items():
            if field_name in config_dict:
                field.label = config_dict[field_name].label  # Set label from DB
                if not field.initial:  # Only set if no initial value is passed
                    field.initial = config_dict[field_name].initial_value

    def save(self, commit=True):
        instance = modelcalc(
            oSec01Field01=self.cleaned_data['oSec01Field01'],
            oSec01Field02=self.cleaned_data['oSec01Field02'],
            oSec01Field03=self.cleaned_data['oSec01Field03'],
            oSec01Field04=self.cleaned_data['oSec01Field04'],
            
            oSec02Field01=self.cleaned_data['oSec02Field01'],
            oSec02Field02=self.cleaned_data['oSec02Field02'],
            oSec02Field03=self.cleaned_data['oSec02Field03'],
            oSec02Field04=self.cleaned_data['oSec02Field04'],
            oSec02Field05=self.cleaned_data['oSec02Field05'],
        )
        if commit:
            instance.save()
        return instance



    

class formCalcMX(forms.Form):
    oSec01Field01 = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control shadow-sm rounded', 'style': 'color: blue;'}))
    oSec01Field02 = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control shadow-sm rounded', 'style': 'color: blue;'}))
    oSec01Field03 = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control shadow-sm rounded', 'style': 'color: blue;'}))
    oSec01Field04 = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control shadow-sm rounded', 'style': 'color: blue;'}))
    oSec01Field05 = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control shadow-sm rounded', 'style': 'color: blue;'}))
    oSec01Field06 = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control shadow-sm rounded', 'style': 'color: blue;'}))
    oSec01Field07 = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control shadow-sm rounded', 'style': 'color: blue;'}))
    oSec01Field08 = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control shadow-sm rounded', 'style': 'color: blue;'}))

    oSec02Field01 = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control shadow-sm rounded', 'readonly': 'readonly', 'style': 'color: blue; font-weight: bold;'}))
    oSec02Field02 = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control shadow-sm rounded', 'readonly': 'readonly', 'style': 'color: blue; font-weight: bold;'}))
    oSec02Field03 = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control shadow-sm rounded', 'readonly': 'readonly', 'style': 'color: blue; font-weight: bold;'}))
    oSec02Field04 = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control shadow-sm rounded', 'readonly': 'readonly', 'style': 'color: blue; font-weight: bold;'}))
    oSec02Field05 = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control shadow-sm rounded', 'readonly': 'readonly', 'style': 'color: blue; font-weight: bold;'}))
    oSec02Field06 = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control shadow-sm rounded', 'readonly': 'readonly', 'style': 'color: blue; font-weight: bold;'}))
    oSec02Field07 = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control shadow-sm rounded', 'readonly': 'readonly', 'style': 'color: blue; font-weight: bold;'}))

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        form_name = 'formCalcMX'
        
        # Fetch field configurations from the database
        field_configs = FormFieldConfig.objects.filter(form_name=form_name)
        config_dict = {config.field_name: config for config in field_configs}

        for field_name, field in self.fields.items():
            if field_name in config_dict:
                field.label = config_dict[field_name].label  # Set label from DB
                if not field.initial:  # Only set if no initial value is passed
                    field.initial = config_dict[field_name].initial_value

    def save(self, commit=True):
        instance = modelcalc(
            oSec01Field01=self.cleaned_data['oSec01Field01'],
            oSec01Field02=self.cleaned_data['oSec01Field02'],
            oSec01Field03=self.cleaned_data['oSec01Field03'],
            oSec01Field04=self.cleaned_data['oSec01Field04'],
            oSec01Field05=self.cleaned_data['oSec01Field05'],
            oSec01Field06=self.cleaned_data['oSec01Field06'],
            oSec01Field07=self.cleaned_data['oSec01Field07'],
            oSec01Field08=self.cleaned_data['oSec01Field08'],
            
            oSec02Field01=self.cleaned_data['oSec02Field01'],
            oSec02Field02=self.cleaned_data['oSec02Field02'],
            oSec02Field03=self.cleaned_data['oSec02Field03'],
            oSec02Field04=self.cleaned_data['oSec02Field04'],
            oSec02Field05=self.cleaned_data['oSec02Field05'],
            oSec02Field06=self.cleaned_data['oSec02Field06'],
            oSec02Field07=self.cleaned_data['oSec02Field07'],
        )
        if commit:
            instance.save()
        return instance


    

class formCalcRT(forms.Form):
    oSec01Field01 = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control shadow-sm rounded', 'style': 'color: blue;'}))
    oSec01Field02 = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control shadow-sm rounded', 'style': 'color: blue;'}))
    oSec01Field03 = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control shadow-sm rounded', 'style': 'color: blue;'}))
    oSec01Field04 = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control shadow-sm rounded', 'style': 'color: blue;'}))
    oSec01Field05 = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control shadow-sm rounded', 'style': 'color: blue;'}))
    oSec01Field06 = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control shadow-sm rounded', 'style': 'color: blue;'}))

    oSec02Field01 = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control shadow-sm rounded', 'readonly': 'readonly', 'style': 'color: blue; font-weight: bold;'}))

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        form_name = 'formCalcRT'
        
        # Fetch field configurations from the database
        field_configs = FormFieldConfig.objects.filter(form_name=form_name)
        config_dict = {config.field_name: config for config in field_configs}

        for field_name, field in self.fields.items():
            if field_name in config_dict:
                field.label = config_dict[field_name].label  # Set label from DB
                if not field.initial:  # Only set if no initial value is passed
                    field.initial = config_dict[field_name].initial_value

    def save(self, commit=True):
        instance = modelcalc(
            oSec01Field01=self.cleaned_data['oSec01Field01'],
            oSec01Field02=self.cleaned_data['oSec01Field02'],
            oSec01Field03=self.cleaned_data['oSec01Field03'],
            oSec01Field04=self.cleaned_data['oSec01Field04'],
            oSec01Field05=self.cleaned_data['oSec01Field05'],
            oSec01Field06=self.cleaned_data['oSec01Field06'],
            
            oSec02Field01=self.cleaned_data['oSec02Field01'],
        )
        if commit:
            instance.save()
        return instance


  

class formCalcCT(forms.Form):
    oSec01Field01 = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control shadow-sm rounded', 'style': 'color: blue;'}))
    oSec01Field02 = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control shadow-sm rounded', 'style': 'color: blue;'}))

    oSec02Field01 = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control shadow-sm rounded', 'readonly': 'readonly', 'style': 'color: blue; font-weight: bold;'}))
    oSec02Field02 = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control shadow-sm rounded', 'readonly': 'readonly', 'style': 'color: blue; font-weight: bold;'}))
    oSec02Field03 = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control shadow-sm rounded', 'readonly': 'readonly', 'style': 'color: blue; font-weight: bold;'}))
    oSec02Field04 = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control shadow-sm rounded', 'readonly': 'readonly', 'style': 'color: blue; font-weight: bold;'}))
    oSec02Field05 = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control shadow-sm rounded', 'readonly': 'readonly', 'style': 'color: blue; font-weight: bold;'}))
    oSec02Field06 = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control shadow-sm rounded', 'readonly': 'readonly', 'style': 'color: blue; font-weight: bold;'}))
    oSec02Field07 = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control shadow-sm rounded', 'readonly': 'readonly', 'style': 'color: blue; font-weight: bold;'}))
    oSec02Field08 = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control shadow-sm rounded', 'readonly': 'readonly', 'style': 'color: blue; font-weight: bold;'}))

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        form_name = 'formCalcCT'
        
        # Fetch field configurations from the database
        field_configs = FormFieldConfig.objects.filter(form_name=form_name)
        config_dict = {config.field_name: config for config in field_configs}

        for field_name, field in self.fields.items():
            if field_name in config_dict:
                field.label = config_dict[field_name].label  # Set label from DB
                if not field.initial:  # Only set if no initial value is passed
                    field.initial = config_dict[field_name].initial_value

    def save(self, commit=True):
        instance = modelcalc(
            oSec01Field01=self.cleaned_data['oSec01Field01'],
            oSec01Field02=self.cleaned_data['oSec01Field02'],
            
            oSec02Field01=self.cleaned_data['oSec02Field01'],
            oSec02Field02=self.cleaned_data['oSec02Field02'],
            oSec02Field03=self.cleaned_data['oSec02Field03'],
            oSec02Field04=self.cleaned_data['oSec02Field04'],
            oSec02Field05=self.cleaned_data['oSec02Field05'],
            oSec02Field06=self.cleaned_data['oSec02Field06'],
            oSec02Field07=self.cleaned_data['oSec02Field07'],
            oSec02Field08=self.cleaned_data['oSec02Field08'],
        )
        if commit:
            instance.save()
        return instance


       
   


class formCalcSC(forms.Form):
    oSec01Field01 = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control shadow-sm rounded', 'style': 'color: blue;'}))
    oSec01Field02 = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control shadow-sm rounded', 'style': 'color: blue;'}))
    oSec01Field03 = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control shadow-sm rounded', 'style': 'color: blue;'}))
    oSec01Field04 = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control shadow-sm rounded', 'style': 'color: blue;'}))

    oSec02Field01 = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control shadow-sm rounded', 'readonly': 'readonly', 'style': 'color: blue; font-weight: bold;'}))
    oSec02Field02 = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control shadow-sm rounded', 'readonly': 'readonly', 'style': 'color: blue; font-weight: bold;'}))
    oSec02Field03 = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control shadow-sm rounded', 'readonly': 'readonly', 'style': 'color: blue; font-weight: bold;'}))
    oSec02Field04 = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control shadow-sm rounded', 'readonly': 'readonly', 'style': 'color: blue; font-weight: bold;'}))
    oSec02Field05 = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control shadow-sm rounded', 'readonly': 'readonly', 'style': 'color: blue; font-weight: bold;'}))
    oSec02Field06 = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control shadow-sm rounded', 'readonly': 'readonly', 'style': 'color: blue; font-weight: bold;'}))

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        form_name = 'formCalcSC'
        
        # Fetch field configurations from the database
        field_configs = FormFieldConfig.objects.filter(form_name=form_name)
        config_dict = {config.field_name: config for config in field_configs}

        for field_name, field in self.fields.items():
            if field_name in config_dict:
                field.label = config_dict[field_name].label  # Set label from DB
                if not field.initial:  # Only set if no initial value is passed
                    field.initial = config_dict[field_name].initial_value

    def save(self, commit=True):
        instance = modelcalc(
            oSec01Field01=self.cleaned_data['oSec01Field01'],
            oSec01Field02=self.cleaned_data['oSec01Field02'],
            oSec01Field03=self.cleaned_data['oSec01Field03'],
            oSec01Field04=self.cleaned_data['oSec01Field04'],
            
            oSec02Field01=self.cleaned_data['oSec02Field01'],
            oSec02Field02=self.cleaned_data['oSec02Field02'],
            oSec02Field03=self.cleaned_data['oSec02Field03'],
            oSec02Field04=self.cleaned_data['oSec02Field04'],
            oSec02Field05=self.cleaned_data['oSec02Field05'],
            oSec02Field06=self.cleaned_data['oSec02Field06'],
        )
        if commit:
            instance.save()
        return instance


class formCalcBS(forms.Form):
    oSec01Field01 = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control shadow-sm rounded', 'style': 'color: blue;'}))
    oSec01Field02 = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control shadow-sm rounded', 'style': 'color: blue;'}))
    oSec01Field03 = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control shadow-sm rounded', 'style': 'color: blue;'}))
    oSec01Field04 = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control shadow-sm rounded', 'style': 'color: blue;'}))
    oSec01Field05 = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control shadow-sm rounded', 'style': 'color: blue;'}))
    oSec01Field06 = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control shadow-sm rounded', 'style': 'color: blue;'}))

    oSec02Field01 = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control shadow-sm rounded', 'readonly': 'readonly', 'style': 'color: blue; font-weight: bold;'}))
    oSec02Field02 = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control shadow-sm rounded', 'readonly': 'readonly', 'style': 'color: blue; font-weight: bold;'}))
    oSec02Field03 = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control shadow-sm rounded', 'readonly': 'readonly', 'style': 'color: blue; font-weight: bold;'}))

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        form_name = 'formCalcBS'
        
        # Fetch field configurations from the database
        field_configs = FormFieldConfig.objects.filter(form_name=form_name)
        config_dict = {config.field_name: config for config in field_configs}

        for field_name, field in self.fields.items():
            if field_name in config_dict:
                field.label = config_dict[field_name].label  # Set label from DB
                if not field.initial:  # Only set if no initial value is passed
                    field.initial = config_dict[field_name].initial_value

    def save(self, commit=True):
        instance = modelcalc(
            oSec01Field01=self.cleaned_data['oSec01Field01'],
            oSec01Field02=self.cleaned_data['oSec01Field02'],
            oSec01Field03=self.cleaned_data['oSec01Field03'],
            oSec01Field04=self.cleaned_data['oSec01Field04'],
            oSec01Field05=self.cleaned_data['oSec01Field05'],
            oSec01Field06=self.cleaned_data['oSec01Field06'],
            
            oSec02Field01=self.cleaned_data['oSec02Field01'],
            oSec02Field02=self.cleaned_data['oSec02Field02'],
            oSec02Field03=self.cleaned_data['oSec02Field03'],
        )
        if commit:
            instance.save()
        return instance


class formCalcNS(forms.Form):
    oSec01Field01 = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control shadow-sm rounded', 'style': 'color: blue;'}))
    oSec01Field02 = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control shadow-sm rounded', 'style': 'color: blue;'}))
    oSec01Field03 = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control shadow-sm rounded', 'style': 'color: blue;'}))
    oSec01Field04 = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control shadow-sm rounded', 'style': 'color: blue;'}))
    oSec01Field05 = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control shadow-sm rounded', 'style': 'color: blue;'}))
    oSec01Field06 = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control shadow-sm rounded', 'style': 'color: blue;'}))
    oSec01Field07 = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control shadow-sm rounded', 'style': 'color: blue;'}))
    oSec01Field08 = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control shadow-sm rounded', 'style': 'color: blue;'}))

    oSec02Field01 = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control shadow-sm rounded', 'readonly': 'readonly', 'style': 'color: blue; font-weight: bold;'}))

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        form_name = 'formCalcNS'
        
        # Fetch field configurations from the database
        field_configs = FormFieldConfig.objects.filter(form_name=form_name)
        config_dict = {config.field_name: config for config in field_configs}

        for field_name, field in self.fields.items():
            if field_name in config_dict:
                field.label = config_dict[field_name].label  # Set label from DB
                if not field.initial:  # Only set if no initial value is passed
                    field.initial = config_dict[field_name].initial_value

    def save(self, commit=True):
        instance = modelcalc(
            oSec01Field01=self.cleaned_data['oSec01Field01'],
            oSec01Field02=self.cleaned_data['oSec01Field02'],
            oSec01Field03=self.cleaned_data['oSec01Field03'],
            oSec01Field04=self.cleaned_data['oSec01Field04'],
            oSec01Field05=self.cleaned_data['oSec01Field05'],
            oSec01Field06=self.cleaned_data['oSec01Field06'],
            oSec01Field07=self.cleaned_data['oSec01Field07'],
            oSec01Field08=self.cleaned_data['oSec01Field08'],
            
            oSec02Field01=self.cleaned_data['oSec02Field01'],
        )
        if commit:
            instance.save()
        return instance




class formCalcPNch(forms.Form):
    oSec01Field01 = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control shadow-sm rounded', 'style': 'color: blue;'}))
    oSec01Field02 = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control shadow-sm rounded', 'style': 'color: blue;'}))
    oSec01Field03 = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control shadow-sm rounded', 'style': 'color: blue;'}))
    oSec01Field04 = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control shadow-sm rounded', 'style': 'color: blue;'}))
    oSec01Field05 = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control shadow-sm rounded', 'style': 'color: blue;'}))
    oSec01Field06 = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control shadow-sm rounded', 'style': 'color: blue;'}))
    oSec01Field07 = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control shadow-sm rounded', 'style': 'color: blue;'}))
    oSec01Field08 = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control shadow-sm rounded', 'style': 'color: blue;'}))
    oSec01Field09 = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control shadow-sm rounded', 'style': 'color: blue;'}))
    oSec01Field10 = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control shadow-sm rounded', 'style': 'color: blue;'}))

    oSec02Field01 = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control shadow-sm rounded', 'readonly': 'readonly', 'style': 'color: blue; font-weight: bold;'}))
    oSec02Field02 = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control shadow-sm rounded', 'readonly': 'readonly', 'style': 'color: blue; font-weight: bold;'}))
    oSec02Field03 = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control shadow-sm rounded', 'readonly': 'readonly', 'style': 'color: blue; font-weight: bold;'}))
    oSec02Field04 = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control shadow-sm rounded', 'readonly': 'readonly', 'style': 'color: blue; font-weight: bold;'}))
    oSec02Field05 = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control shadow-sm rounded', 'readonly': 'readonly', 'style': 'color: blue; font-weight: bold;'}))
    oSec02Field06 = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control shadow-sm rounded', 'readonly': 'readonly', 'style': 'color: blue; font-weight: bold;'}))
    oSec02Field07 = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control shadow-sm rounded', 'readonly': 'readonly', 'style': 'color: blue; font-weight: bold;'}))

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        form_name = 'formCalcPNch'
        
        # Fetch field configurations from the database
        field_configs = FormFieldConfig.objects.filter(form_name=form_name)
        config_dict = {config.field_name: config for config in field_configs}

        for field_name, field in self.fields.items():
            if field_name in config_dict:
                field.label = config_dict[field_name].label  # Set label from DB
                if not field.initial:  # Only set if no initial value is passed
                    field.initial = config_dict[field_name].initial_value

    def save(self, commit=True):
        instance = modelcalc(
            oSec01Field01=self.cleaned_data['oSec01Field01'],
            oSec01Field02=self.cleaned_data['oSec01Field02'],
            oSec01Field03=self.cleaned_data['oSec01Field03'],
            oSec01Field04=self.cleaned_data['oSec01Field04'],
            oSec01Field05=self.cleaned_data['oSec01Field05'],
            oSec01Field06=self.cleaned_data['oSec01Field06'],
            oSec01Field07=self.cleaned_data['oSec01Field07'],
            oSec01Field08=self.cleaned_data['oSec01Field08'],
            oSec01Field09=self.cleaned_data['oSec01Field09'],
            oSec01Field10=self.cleaned_data['oSec01Field10'],
            
            oSec02Field01=self.cleaned_data['oSec02Field01'],
            oSec02Field02=self.cleaned_data['oSec02Field02'],
            oSec02Field03=self.cleaned_data['oSec02Field03'],
            oSec02Field04=self.cleaned_data['oSec02Field04'],
            oSec02Field05=self.cleaned_data['oSec02Field05'],
            oSec02Field06=self.cleaned_data['oSec02Field06'],
            oSec02Field07=self.cleaned_data['oSec02Field07'],
        )
        if commit:
            instance.save()
        return instance



