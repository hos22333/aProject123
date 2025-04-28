from django.urls import path
from . import views

urlpatterns = [
    path("PageCalculationSheet/", views.LoadPageCalculationSheet, name="PageCalculationSheet"),
    path('generate_report/', views.generate_report, name='generate_report'),
    path('PageCalculationSheet/submit/', views.HandleCalculationSheetForm, name='submitPageCalculationSheet'),

    path('DeleteCalcMachine/<int:machine_id>/', views.DeleteCalcMachine, name='DeleteCalcMachine'),
    path('CalculationSheet_get_data/<int:machine_id>/',   views.CalculationSheet_get_data, name='get_calculationsheet_data'),
    path('generate_saved_report/<int:machine_id>/', views.generate_saved_report, name='generate_saved_report'),
]