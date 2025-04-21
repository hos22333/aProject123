from django.db import models
from django.contrib.auth.models import User
from django.utils.timezone import now

class aLogEntry(models.Model):
    timestamp = models.DateTimeField(default=now)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    message = models.TextField()

    def __str__(self):
        return f"{self.timestamp} - {self.user} - {self.message}"


class Companies(models.Model):
    nameCompanies  = models.CharField(max_length=255)

    def __str__(self):
        return self.nameCompanies  # Use the correct field name
    
    

   
    
class UserCompany(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)  # Ensures one user belongs to one company
    company = models.ForeignKey(Companies, on_delete=models.CASCADE)  # Allows multiple users to be assigned to the same company

    def __str__(self):
        return f"{self.user.username} - {self.company.nameCompanies}"
    


     
class FormFieldConfig(models.Model):
    form_name = models.CharField(max_length=100)
    field_name = models.CharField(max_length=100)
    label = models.CharField(max_length=100, blank=True, null=True)
    initial_value = models.CharField(max_length=255, blank=True, null=True)
    VISIBILITY_CHOICES = [
        ('Show', 'Show'),
        ('Hide', 'Hide'),
    ]
    visibility = models.CharField(max_length=10, choices=VISIBILITY_CHOICES, default='Show')
    company = models.ForeignKey(Companies, on_delete=models.CASCADE, null=True, blank=True)  # Add company selection


    def __str__(self):
        return f"{self.form_name} - {self.field_name}"






