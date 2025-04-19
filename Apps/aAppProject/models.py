from django.db import models
from Apps.aAppMechanical.models import Companies

# Create your models here.


class APP_Project(models.Model):
    name            = models.CharField(max_length=255)
    client_name     = models.CharField(max_length=255)
    capacity        = models.CharField(max_length=100)
    company         = models.ForeignKey(Companies, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.name