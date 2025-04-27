from django.urls import path
from . import views

urlpatterns = [
    path("PageCalculationSheet/", views.LoadPageCalculationSheet, name="PageCalculationSheet"),
    path('generate_report/', views.generate_report, name='generate_report'),
    path('PageCalculationSheet/submit/', views.HandleCalculationSheetForm, name='submitPageCalculationSheet'),

]