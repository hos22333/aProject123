from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('aApp1.urls')),
    path('Mechanical/', include('aAppMechanical.urls')),
]
