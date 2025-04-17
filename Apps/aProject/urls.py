from django.urls import path
from . import views


urlpatterns = [
    path('projects/', views.project_list, name='project_lists'),
    path('editprojects/<int:project_id>/', views.edit_project, name='edit_projects'),
    path('deleteprojects/<int:project_id>/', views.delete_project, name='delete_projects'),    
    path('get_machines/<int:project_id>/', views.get_machines, name='get_machiness'),    
    path('generate_report/<int:project_id>/', views.generate_report, name='generate_reports'),
]