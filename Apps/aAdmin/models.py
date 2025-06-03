from django.db import models
from django.contrib.auth.models import User
from Apps.aAppMechanical.models import Companies


class Autho(models.Model):
    name = models.CharField(max_length=100, unique=True)
    
    def __str__(self):
        return self.name


class Role(models.Model):
    name = models.CharField(max_length=100, unique=True)
    
    def __str__(self):
        return self.name



class RoleAutho(models.Model):
    role = models.ForeignKey(Role, on_delete=models.CASCADE)
    autho = models.ForeignKey(Autho, on_delete=models.CASCADE)
    
    def __str__(self):
        return f"{self.role.name} - {self.autho.name}"



class UserRole(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    role = models.ForeignKey(Role, on_delete=models.CASCADE)
    
    def __str__(self):
        return f"{self.user.username} - {self.role.name}"


class DataTransfer(models.Model):
    keyValue            = models.CharField(max_length=255)
    CalculationField = models.CharField(max_length=255)
    SubmittalField = models.CharField(max_length=255)
    company = models.ForeignKey(Companies, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return f"{self.keyValue}_{self.company}"