import pdb

from Apps.aAppProject.models import APP_Project
from Apps.aAppSubmittal.models import Machine
from .models import Companies
from .models import UserCompany
from .models import aLogEntry
from .models import FormFieldConfig


from .forms import FormFieldConfigForm
from .forms import UserCompanyForm
from .forms import CompanyForm

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

def configurations(request):
    return render(request, 'form_config_list.html')

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
    
     # Get the company of the logged-in user    
    user_company = None
    if request.user.is_authenticated:
        try:
            user_company = UserCompany.objects.get(user=request.user).company
        except UserCompany.DoesNotExist:
            user_company = None

    print(user_company)

    configs = FormFieldConfig.objects.filter(company=user_company).order_by(sort_by)
    
    
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
            aLogEntry.objects.create(
                user=request.user,
                message=f"{request.user} Add Configrations >>> {form.form_name}_{form.field_name}"
            )
            return redirect('list_configs')
    else:
        form = FormFieldConfigForm()
    return render(request, 'form_config_form.html', {'form': form})

def edit_config(request, config_id):
    config = get_object_or_404(FormFieldConfig, id=config_id)
    aLogEntry.objects.create(
        user=request.user,
        message=f"{request.user} editing >>> {config.form_name}_{config.field_name}"
    )
    if request.method == "POST":
        form = FormFieldConfigForm(request.POST, instance=config)
        if form.is_valid():
            form.save()
            aLogEntry.objects.create(
                user=request.user,
                message=f"{request.user} edited >>> {form.form_name}_{form.field_name}"
            )
            return redirect('list_configs')
    else:
        form = FormFieldConfigForm(instance=config)
    return render(request, 'form_config_form.html', {'form': form})

def delete_config(request, config_id):
    config = get_object_or_404(FormFieldConfig, id=config_id)
    aLogEntry.objects.create(
        user=request.user,
        message=f"{request.user} Deleted >>> {config.form_name}_{config.field_name}"
    )
    config.delete()
    return redirect('list_configs')

###################################
###################################
# Create Company
def add_company(request):
    if request.method == 'POST':
        form = CompanyForm(request.POST)
        if form.is_valid():
            form.save()
            aLogEntry.objects.create(
                user=request.user,
                message=f"{request.user} Added >>> {form.nameCompanies} Company"
            )
    else:
        form = CompanyForm()

    # Fetch all current roles
    companies = Companies.objects.all()

    return render(request, 'add_company.html', {'form': form, 'companies': companies})

# Delete Company
def delete_company(request, company_id):
    company = get_object_or_404(Companies, id=company_id)
    aLogEntry.objects.create(
        user=request.user,
        message=f"{request.user} Deleted >>> {company.nameCompanies} Company"
    )
    company.delete()
    return redirect('add_company')  # Redirect back to the list



# Edit Company
def edit_company(request, company_id):
    company = get_object_or_404(Companies, id=company_id)
    aLogEntry.objects.create(
        user=request.user,
        message=f"{request.user} Editing >>> {company.nameCompanies} Company"
    )

    if request.method == 'POST':
        form = CompanyForm(request.POST, instance=company)
        if form.is_valid():
            form.save()
            aLogEntry.objects.create(
                user=request.user,
                message=f"{request.user} Edited >>> {form.nameCompanies} Company"
            )
            return redirect('add_company')  # Redirect back to the main page
    else:
        form = CompanyForm(instance=company)

    return render(request, 'edit_company.html', {'form': form, 'company': company})

def companies_list(request):
    companies = Companies.objects.all()  # Fetch all users
    return render(request, 'companies_list.html', {'companies': companies})

def assign_user_to_company(request):
    if request.method == "POST":
        form = UserCompanyForm(request.POST)
        if form.is_valid():
            form.save()
            aLogEntry.objects.create(
                user=request.user,
                message=f"{request.user} Assigned >>> {form.user.username} to {form.company.nameCompanies} Company"
            )
            return redirect("assign_user")  # Redirect to a success page
    else:
        form = UserCompanyForm()

    user_companies = UserCompany.objects.all()
    
    return render(request, "assign_user_to_company.html", {"form": form, 'user_companies': user_companies})

def delete_user_company(request, user_company_id):
    user_company = get_object_or_404(UserCompany, id=user_company_id)
    if request.method == 'POST':
        aLogEntry.objects.create(
            user=request.user,
            message=f"{request.user} Deleted >>> {user_company.user.username} from {user_company.company.nameCompanies} Company"
        )
        user_company.delete()
    return redirect('assign_user')  # Redirect back to the assign page




############################
############################
