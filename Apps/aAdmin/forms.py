from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

from .models import Role, Autho, UserRole, RoleAutho


class RegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']




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