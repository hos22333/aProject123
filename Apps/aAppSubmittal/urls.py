from django.urls import path
from . import views


urlpatterns = [
    path('add-machine/', views.add_machine, name='add_machine'),
    path('delete-machine/<int:machine_id>/', views.delete_machine, name='delete_machine'),
    path('edit-machine/<int:machine_id>/', views.edit_amachine, name='edit_machine'),

    path('DeleteMachine/<int:machine_id>/', views.DeleteMachine, name='DeleteMachine'),

    path('Edit_DataSheetNS/<int:machine_id>/', views.edit_machine, name='Edit_DataSheetNS'),
    
    path('DataSheetNSget_data/<int:machine_id>/',   views.DataSheetNS_get_datasheet_data, name='get_datasheet_data'),

    path("PageDataSheet/", views.LoadPageDataSheet, name="PageDataSheet"),
    path("PageDataSheet/Save/", views.SavePageDataSheet, name="SavePageDataSheet"),
###############

    path("Draw/<int:aMachine_ID>/<str:aType>/", views.General_DXF_ALL, name="General_DXF_ALL"),
    path("FullDrawing/<int:aMachine_ID>/<str:aType>/", views.FullDrawing, name="FullDrawing"),
]