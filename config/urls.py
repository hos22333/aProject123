from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('Apps.aAdmin.urls')),
    path("Cost/", include("Apps.aCost.urls")),      
    path('Mechanical/', include('Apps.aAppMechanical.urls')),
    path('Project/', include('Apps.aAppProject.urls')),
    path('submittal/', include('Apps.aAppSubmittal.urls')),
    path('Calculation/', include('Apps.aAppCalculation.urls')),
    path('Calculations/', include('Apps.aCalculations.urls')),
]
