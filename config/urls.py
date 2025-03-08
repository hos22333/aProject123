from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('Apps.aApp1.urls')),
    path('Mechanical/', include('Apps.aAppMechanical.urls')),
]
