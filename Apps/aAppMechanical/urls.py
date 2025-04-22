from django.urls import path
from . import views


urlpatterns = [
    path('formdata/', views.list_configs, name='list_configs'),
    path('add/', views.add_config, name='add_config'),
    path('edit/<int:config_id>/', views.edit_config, name='edit_config'),
    path('delete/<int:config_id>/', views.delete_config, name='delete_config'),
    
    
    
    path('add-company/', views.add_company, name='add_company'),
    path('delete-company/<int:company_id>/', views.delete_company, name='delete_company'),
    path('edit-company/<int:company_id>/', views.edit_company, name='edit_company'),
    path('companies/', views.companies_list, name='companies_list'),
    path("assign-user/", views.assign_user_to_company, name="assign_user"),
    path('delete-user-company/<int:user_company_id>/', views.delete_user_company, name='delete_user_company'),
   
]