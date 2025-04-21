import pdb

from Apps.aAppProject.models import APP_Project
from Apps.aAppSubmittal.models import Machine
from .models import UserCompany
from .models import aLogEntry
from .models import FormFieldConfig


from .forms import FormFieldConfigForm
from .forms import UserCompanyForm

from datetime import datetime
from Apps.aAdmin.models import UserRole, RoleAutho, Autho
import requests

from django.http import HttpResponse
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.shortcuts import render, redirect
from django.urls import reverse
from django.utils.timezone import now 
from django.contrib.auth.models import User
from django.conf import settings




###################################
###################################
###################################
###################################
###################################
###################################

def list_configs(request):
    print("LINE52")
    sort_by = request.GET.get('sort', 'id')  # Default sorting by ID
    order = request.GET.get('order', 'asc')  # Default order is ascending

    valid_fields = ['id', 'form_name', 'field_name', 'label', 'initial_value', 'visibility', 'company']
    if sort_by not in valid_fields:
        sort_by = 'id'

    
    print("LINE61")
    
    # Apply sorting order
    if order == 'desc':
        sort_by = f'-{sort_by}'

    configs = FormFieldConfig.objects.all().order_by(sort_by)
    
    
    print("LINE70")
    
    return render(request, 'form_config.html', {
        'configs': configs,
        'sort_by': sort_by.strip(''),  # Remove '-' to keep track of column sorting
        'order': order
    })

def add_config(request):
    if request.method == "POST":
        form = FormFieldConfigForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('list_configs')
    else:
        form = FormFieldConfigForm()
    return render(request, 'form_config_form.html', {'form': form})

def edit_config(request, config_id):
    config = get_object_or_404(FormFieldConfig, id=config_id)
    if request.method == "POST":
        form = FormFieldConfigForm(request.POST, instance=config)
        if form.is_valid():
            form.save()
            return redirect('list_configs')
    else:
        form = FormFieldConfigForm(instance=config)
    return render(request, 'form_config_form.html', {'form': form})

def delete_config(request, config_id):
    config = get_object_or_404(FormFieldConfig, id=config_id)
    config.delete()
    return redirect('list_configs')

###################################
###################################

def assign_user_to_company(request):
    if request.method == "POST":
        form = UserCompanyForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("assign_user")  # Redirect to a success page
    else:
        form = UserCompanyForm()
    
    return render(request, "assign_user_to_company.html", {"form": form})


############################
############################
############################
############################
############################
############################
############################
############################
############################
############################
############################
############################
############################
############################
############################
############################
############################
############################
############################
############################







###
###




###
###






#######
#######
#######
#######
#######
#######
#######
#######


# Helper function to get the user's company


    
    


###
###
###
###
###
###
###
###
###
###
###
###
###
###
###
###
###
###
###
###
###
###
###
###
###
###
###
###
###
###
###
###
###
###
###
###
###
###
###
###
###
###
###
###
###
###
###
###
###
###
###
###
###
###
###
###
###
###
###
###
###
###
###
###
###
###
###
###
###
###






####



