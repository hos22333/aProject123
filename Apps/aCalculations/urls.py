from django.urls import path
from . import views

urlpatterns = [
    path("PageCalculationsSheet/<str:sheet_key>/", views.LoadPageCalculationsSheet, name="PageCalculationsSheet"),
    path("PageCalculationsSheet/<str:sheet_key>/Save/", views.SavePageCalculationsSheet, name="SavePageCalculationsSheet"),
]