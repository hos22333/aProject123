from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

from .models import Role, Autho, UserRole, RoleAutho


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