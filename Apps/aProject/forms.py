from django import forms
from Apps.aAppMechanical.models import Project


class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ['name', 'client_name', 'capacity']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter project name'}),
            'client_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter client name'}),
            'capacity': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter capacity'}),
        }