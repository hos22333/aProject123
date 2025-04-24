from django.urls import path
from . import views

urlpatterns = [
    path("PageCalculationSheet/<str:sheet_key>/", views.LoadPageCalculationSheet, name="PageCalculationSheet"),
    path('generate_report/<str:sheet_key>/', views.generate_report, name='generate_report'),
    path('PageCalculationSheet/<str:sheet_key>/submit/', views.HandleCalculationSheetForm, name='submitPageCalculationSheet'),
]