from django.urls import path
from . import views


urlpatterns = [
    
    
    
    path('formdata/', views.list_configs, name='list_configs'),
    path('add/', views.add_config, name='add_config'),
    path('edit/<int:config_id>/', views.edit_config, name='edit_config'),
    path('delete/<int:config_id>/', views.delete_config, name='delete_config'),
    
    
    
    
        
    path("assign-user/", views.assign_user_to_company, name="assign_user"),
   

###############
   
    


]