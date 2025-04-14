from django.urls import path
from . import views

urlpatterns = [
    path("PageCalculationsSheet/<str:sheet_key>/", views.LoadPageCalculationsSheet, name="PageCalculationsSheet"),
    
]

""" path("PageCalculationsSheet/<str:sheet_key>/submit/", views.handle_calc_form, name='submit'), """