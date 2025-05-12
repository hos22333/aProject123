from django import forms
from .models import APP_Project

class ProjectForm(forms.ModelForm):
    class Meta:
        model = APP_Project
        fields = ['name', 'client_name', 'capacity', 'cover_page_text']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter project name'}),
            'client_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter client name'}),
            'capacity': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter capacity'}),
            'cover_page_text': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Enter cover page text'}),
        }