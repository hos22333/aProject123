from django import forms
from Apps.aAppCalculation.models import modelcalc
from .models import FormFieldConfig
from .models import UserCompany
#######################################

class FormFieldConfigForm(forms.ModelForm):
    class Meta:
        model = FormFieldConfig
        fields = ['form_name', 'field_name', 'label', 'initial_value', 'visibility', 'company']  # Include company field
        widgets = {
            'company': forms.Select(attrs={'class': 'form-control'}),  # Dropdown for selecting a company
            'form_name': forms.TextInput(attrs={'class': 'form-control'}),
            'field_name': forms.TextInput(attrs={'class': 'form-control'}),
            'label': forms.TextInput(attrs={'class': 'form-control'}),
            'initial_value': forms.TextInput(attrs={'class': 'form-control'}),
            'visibility': forms.Select(attrs={'class': 'form-control'}),
        }








class UserCompanyForm(forms.ModelForm):
    class Meta:
        model = UserCompany
        fields = ['user', 'company']  # Include only the fields you want in the form

#######################################
#######################################
#######################################




#######################################
#######################################
#######################################











