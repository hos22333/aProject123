from django.urls import path
from . import views


urlpatterns = [
    path('projects/', views.project_list, name='project_list'),
    path('editprojects/<int:project_id>/', views.edit_project, name='edit_project'),
    path('deleteprojects/<int:project_id>/', views.delete_project, name='delete_project'),    
    path('get_machines/<int:project_id>/', views.get_machines, name='get_machines'),    
    path('get_calc_machines/<int:project_id>/', views.get_calc_machines, name='get_calc_machines'),    
    path('generate_report/<int:project_id>/', views.generate_report, name='generate_report'),
]