from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

from .models import Role, Autho, UserRole, RoleAutho, DataTransfer


from django.core.exceptions import ValidationError

class UserCreationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Enter your password'}))
    confirm_password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Confirm your password'}))

    class Meta:
        model = User
        fields = ['username', 'email', 'password']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter your user name'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Enter your email'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')

        if password != confirm_password:
            raise ValidationError("Passwords do not match")
        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password'])
        if commit:
            user.save()
        return user




# Role Form
class RoleForm(forms.ModelForm):
    class Meta:
        model = Role
        fields = ['name']

# Autho Form
class AuthoForm(forms.ModelForm):
    class Meta:
        model = Autho
        fields = ['name']



# RoleAutho Form
class RoleAuthoForm(forms.ModelForm):
    class Meta:
        model = RoleAutho
        fields = ['role', 'autho']



# UserRole Form
class UserRoleForm(forms.ModelForm):
    class Meta:
        model = UserRole
        fields = ['user', 'role']



# Upload DXF File Form
class DXFUploadForm(forms.Form):
    file = forms.FileField(label="Upload DXF File")


class DataTransferForm(forms.ModelForm):
    class Meta:
        model = DataTransfer
        fields = ['keyValue', 'CalculationField', 'SubmittalField', 'company']
        widgets = {
            'keyValue': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter the machine sheetkey'}),
            'CalculationField': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter the Calculation Field name'}),
            'SubmittalField': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter the Submittal field name'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Add Bootstrap class to make it large
        self.fields['company'].widget.attrs.update({'class': 'form-control form-control-lg'})
        
        # Add empty label as placeholder
        self.fields['company'].empty_label = "Select a company..."
