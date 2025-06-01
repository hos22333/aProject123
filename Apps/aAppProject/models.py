from django.db import models
from Apps.aAppMechanical.models import Companies
from django.contrib.auth.models import User

# Create your models here.


class APP_Project(models.Model):
    name            = models.CharField(max_length=255)
    client_name     = models.CharField(max_length=255)
    capacity        = models.CharField(max_length=100)
    company         = models.ForeignKey(Companies, on_delete=models.CASCADE, null=True, blank=True)
    last_saved_time = models.DateTimeField(null=True, blank=True)
    cover_page_text = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.name



class ReportProgress(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    project_id = models.IntegerField()
    status = models.CharField(max_length=500, default='starting')  
    percent = models.IntegerField(default=0)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user}_{self.project_id}_{self.status}"


