from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from django.contrib.auth.views import LogoutView
from django.contrib.auth.views import PasswordChangeView, PasswordChangeDoneView


urlpatterns = [
    path('', views.index, name='index'),
    path('home/', views.home, name='home'),
    
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('logout/', LogoutView.as_view(next_page='/'), name='logout'),
    path('password_change/', PasswordChangeView.as_view(template_name='password_change.html'), name='password_change'),
    path('password_change/done/', PasswordChangeDoneView.as_view(template_name='password_change_done.html'), name='password_change_done'),
    
    
    path('password_reset/', auth_views.PasswordResetView.as_view(template_name='password_reset.html'), name='password_reset'),
    path('password_reset_done/', auth_views.PasswordResetDoneView.as_view(template_name='password_reset_done.html'), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='password_reset_confirm.html'), name='password_reset_confirm'),
    path('reset_done/', auth_views.PasswordResetCompleteView.as_view(template_name='password_reset_complete.html'), name='password_reset_complete'),


    #############################

    path('create-autho/', views.create_autho, name='create_autho'),
    path('delete-autho/<int:autho_id>/', views.delete_autho, name='delete_autho'),
    
    path('create-role/', views.create_role, name='create_role'),
    path('delete-role/<int:role_id>/', views.delete_role, name='delete_role'),
    path('edit-role/<int:role_id>/', views.edit_role, name='edit_role'),
    
    path('assign-role-autho/', views.assign_role_autho, name='assign_role_autho'),
    path('delete-role-autho/<int:role_autho_id>/', views.delete_role_autho, name='delete_role_autho'),
    
    path('assign-user-role/', views.assign_user_role, name='assign_user_role'),
    path('delete-user-role/<int:user_role_id>/', views.delete_user_role, name='delete_user_role'),
    
    path('change-username/', views.change_username, name='change_username'),
    path('change-email/', views.change_email, name='change_email'),
    
    path('profile/', views.profile, name='profile'),
    
    #############################
    
    path('user_roles_autho/', views.user_roles_with_authos, name='user_roles_autho'),

    path('Log_history/', views.Log_history, name='Log_history'),
    path('modelcalc/', views.modelcalc_list, name='modelcalc_list'),
    path('modelmachine/', views.modelmachine_list, name='modelmachine_list'),
    
    path('users/', views.users_list, name='users_list'),



]
