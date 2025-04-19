from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('Apps.aApp1.urls')),
    path("Cost/", include("Apps.aCost.urls")),      
    path('Mechanical/', include('Apps.aAppMechanical.urls')),
    path('Calculations/', include('Apps.aCalculations.urls')),
    path('Project/', include('Apps.aAppProject.urls')),
]
