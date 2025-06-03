from django.shortcuts import render, redirect
from .forms import UserCreationForm, RoleForm, AuthoForm, UserRoleForm, RoleAuthoForm, DXFUploadForm
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import AuthenticationForm
from .models import Role
from .models import Autho
from .models import UserRole
from .models import RoleAutho
from .models import DataTransfer

from django.contrib.auth.models import User
from Apps.aAppCalculation.models import modelcalc_log
from Apps.aAppCalculation.models import API_Keys
from Apps.aAppSubmittal.models import Machine_log
from Apps.aAppSubmittal.models import DXF_data
from Apps.aAppMechanical.models import UserCompany
from Apps.aAppMechanical.models import aLogEntry
from Apps.aAppMechanical.models import Companies
from Apps.aAppMechanical.models import FormFieldConfig
from Apps.aAppSubmittal.models import AddMachine
from django.shortcuts import get_object_or_404



from .forms import DataTransferForm


from Apps.aAppMechanical.forms import UserCompanyForm
from Apps.aAppMechanical.forms import CompanyForm
from Apps.aAppMechanical.forms import FormFieldConfigForm
from Apps.aAppSubmittal.forms import MachineForm  
from Apps.aAppSubmittal.forms import DXFdataForm  
from Apps.aAppCalculation.forms import APIkeyForm  

from django.contrib.auth.decorators import login_required
from django.contrib import messages

from django.utils.text import slugify

from config import settings
import os

    
def home(request):
    return render(request, 'home.html')

def index(request):
    return render(request, 'index.html')

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('index')  # Redirect to home page after registration
    else:
        form = UserCreationForm()
    return render(request, 'register.html', {'form': form})

def user_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('index')  # Redirect to home page after login
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})

#############################################
# Create Role
def create_role(request):
    if request.method == 'POST':
        form = RoleForm(request.POST)
        
        if form.is_valid():
            form.save()
    else:
        form = RoleForm()

    # Fetch all current roles
    roles = Role.objects.all()

    return render(request, 'create_role.html', {'form': form, 'roles': roles})


# Delete Role
def delete_role(request, role_id):
    role = get_object_or_404(Role, id=role_id)
    
    role.delete()
    return redirect('create_role')  # Redirect back to the list



# Edit Role
def edit_role(request, role_id):
    role = get_object_or_404(Role, id=role_id)
    old_name = role.name
    if request.method == 'POST':
        form = RoleForm(request.POST, instance=role)
        if form.is_valid():
            form.save()
            
            return redirect('create_role')  # Redirect back to the main page
    else:
        form = RoleForm(instance=role)

    return render(request, 'edit_role.html', {'form': form, 'role': role})

###############################

# Create Autho
def create_autho(request):
    if request.method == 'POST':
        form = AuthoForm(request.POST)
       
        if form.is_valid():
            form.save()
    else:
        form = AuthoForm()

    # Fetch all current authos
    authos = Autho.objects.all()

    return render(request, 'create_autho.html', {'form': form, 'authos': authos})


# Delete Autho
def delete_autho(request, autho_id):
    autho = get_object_or_404(Autho, id=autho_id)
    
    autho.delete()
    return redirect('create_autho')  # Redirect back to the list

#######################################




# Assign RoleAutho
def assign_role_autho(request):
    if request.method == 'POST':
        form = RoleAuthoForm(request.POST)
        
        if form.is_valid():
            form.save()
            #return redirect('role_autho_list')
    else:
        form = RoleAuthoForm()
        
    role_authos = RoleAutho.objects.all()
    
    return render(request, 'assign_role_autho.html', {'form': form, 'role_authos': role_authos})

def delete_role_autho(request, role_autho_id):
    role_autho = get_object_or_404(RoleAutho, id=role_autho_id)
    if request.method == 'POST':
        
        role_autho.delete()
    return redirect('assign_role_autho')  # Redirect back to the assign page




# Assign UserRole
def assign_user_role(request):
    if request.method == 'POST':
        form = UserRoleForm(request.POST)
        
        if form.is_valid():
            form.save()
            #return redirect('assign_user_role')  # Redirect to the same page after saving
    else:
        form = UserRoleForm()
    
    # Fetch all user-role assignments
    user_roles = UserRole.objects.all()
    
    return render(request, 'assign_user_role.html', {'form': form, 'user_roles': user_roles})

def delete_user_role(request, user_role_id):
    user_role = get_object_or_404(UserRole, id=user_role_id)
    if request.method == 'POST':
        
        user_role.delete()
    return redirect('assign_user_role')  # Redirect back to the assign page


def user_roles_with_authos(request):
    # Get filters from GET request
    selected_user = request.GET.get('user')
    selected_role = request.GET.get('role')

    # Retrieve filtered user-role data
    user_roles = UserRole.objects.select_related('user', 'role')

    if selected_user:
        user_roles = user_roles.filter(user__id=selected_user)
    if selected_role:
        user_roles = user_roles.filter(role__id=selected_role)

    user_data = []
    for user_role in user_roles:
        authos = RoleAutho.objects.filter(role=user_role.role).select_related('autho')
        user_data.append({
            'user': user_role.user,
            'role': user_role.role,
            'authos': [autho.autho for autho in authos]
        })

    # Retrieve all users and roles for dropdown options
    users = User.objects.all()
    roles = Role.objects.all()

    context = {
        'user_data': user_data,
        'users': users,
        'roles': roles,
        'selected_user': int(selected_user) if selected_user else None,
        'selected_role': int(selected_role) if selected_role else None
    }
    return render(request, 'user_roles.html', context)


#######################################

def Log_history(request):
    
    records = aLogEntry.objects.filter(user=request.user)
   

    return render(request, 'log_history_list.html', {'records': records})


def modelcalc_list(request):
    # Get the company of the logged-in user    
    user_company = None
    if request.user.is_authenticated:
        try:
            user_company = UserCompany.objects.get(user=request.user).company
        except UserCompany.DoesNotExist:
            user_company = None
    records = modelcalc_log.objects.filter(company=user_company)
    data = []

    for record in records:
        fields = []
        for field in record._meta.fields:
            if field.name not in ['id', 'oSec00Field01', 'oSec00Field02', 'oSec00Field03']:
                fields.append({'name': field.verbose_name, 'value': getattr(record, field.name)})
        data.append({
            'record': record,
            'fields': fields
        })

    return render(request, 'modelcalc_list.html', {'data': data})


def modelmachine_list(request):
    # Get the company of the logged-in user    
    user_company = None
    if request.user.is_authenticated:
        try:
            user_company = UserCompany.objects.get(user=request.user).company
        except UserCompany.DoesNotExist:
            user_company = None
    records = Machine_log.objects.filter(company=user_company)
    """ records = Machine.objects.select_related('project', 'company').all() """
    data = []

    for record in records:
        fields = []
        for field in record._meta.fields:
            if field.name not in ['id', 'oSec00Field01', 'oSec00Field02', 'oSec00Field03']:
                fields.append({'name': field.verbose_name, 'value': getattr(record, field.name)})
        data.append({
            'record': record,
            'fields': fields
        })

    return render(request, 'modelmachine_list.html', {'data': data})



#######################################


@login_required
def change_username(request):
    if request.method == 'POST':
        new_username = request.POST.get('username')
        if User.objects.filter(username=new_username).exists():
            messages.error(request, 'Username already taken.')
        else:
            
            request.user.username = new_username
            request.user.save()
            messages.success(request, 'Your username has been updated successfully.')
            return redirect('change_username')  # Or any other page

    return render(request, 'change_username.html', {'current_username': request.user.username})


@login_required
def change_email(request):
    if request.method == 'POST':
        new_email = request.POST.get('email')
        if User.objects.filter(email=new_email).exists():
            messages.error(request, 'Email already taken.')
        else:
            
            request.user.email = new_email
            request.user.save()
            messages.success(request, 'Your email has been updated successfully.')
            return redirect('change_email')  # Or any other page

    return render(request, 'change_email.html', {'current_email': request.user.email})


@login_required
def profile(request):
    return render(request, 'profile.html')




def users_list(request):
    users = User.objects.all()  # Fetch all users
    return render(request, 'users_list.html', {'users': users})


#######################################

# Create Company
def add_company(request):
    if request.method == 'POST':
        form = CompanyForm(request.POST)
        if form.is_valid():
            form.save()
            company_name = request.POST.get("nameCompanies")
            base_static_path = os.path.join(settings.BASE_DIR, 'static', 'aReports')
            company_folder = os.path.join(base_static_path, company_name)
            # Create the folders if they don't exist
            os.makedirs(company_folder, exist_ok=True)
            
    else:
        form = CompanyForm()

    # Fetch all current roles
    companies = Companies.objects.all()

    return render(request, 'add_company.html', {'form': form, 'companies': companies})

# Delete Company
def delete_company(request, company_id):
    company = get_object_or_404(Companies, id=company_id)
    
    company.delete()
    return redirect('add_company')  # Redirect back to the list



# Edit Company
def edit_company(request, company_id):
    company = get_object_or_404(Companies, id=company_id)
    old_company = company.nameCompanies

    if request.method == 'POST':
        form = CompanyForm(request.POST, instance=company)
        if form.is_valid():
            form.save()
            
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
            return redirect("assign_user")  # Redirect to a success page
    else:
        form = UserCompanyForm()

    user_companies = UserCompany.objects.all()
    
    return render(request, "assign_user_to_company.html", {"form": form, 'user_companies': user_companies})

def delete_user_company(request, user_company_id):
    user_company = get_object_or_404(UserCompany, id=user_company_id)
    if request.method == 'POST':
        
        user_company.delete()
    return redirect('assign_user')  # Redirect back to the assign page


#######################################

# Create Machine
def add_machine(request):
     # Get the company of the logged-in user    
    user_company = None
    if request.user.is_authenticated:
        try:
            user_company = UserCompany.objects.get(user=request.user).company
        except UserCompany.DoesNotExist:
            user_company = None

    print(user_company)

    if request.method == 'POST':
        form = MachineForm(request.POST)
        
        if form.is_valid():
            form.save()
    else:
        form = MachineForm()

    # Fetch all current roles
    machines = AddMachine.objects.filter(company=user_company).order_by('order')

    return render(request, 'machine_list.html', {'form': form, 'machines': machines})

# Delete Machine
def delete_machine(request, machine_id):
    machine = get_object_or_404(AddMachine, id=machine_id)
    
    machine.delete()
    return redirect('add_machine')  # Redirect back to the list



# Edit Machine
def edit_amachine(request, machine_id):
    machine = get_object_or_404(AddMachine, id=machine_id)

    

    if request.method == 'POST':
        form = MachineForm(request.POST, instance=machine)
        if form.is_valid():
            form.save()
            return redirect('add_machine')  # Redirect back to the main page
    else:
        form = MachineForm(instance=machine)

    return render(request, 'edit_machine.html', {'form': form, 'machine': machine})



#######################################


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

#######################################


def DXFdata_list(request):
    if request.method == "POST":
        
        form = DXFdataForm(request.POST)
        if form.is_valid():
            
            form.save() 

            
            return redirect('DXFdata_list')
    else:
        form = DXFdataForm()
        
    
    datas = DXF_data.objects.all()
    
    return render(request, 'DXFdata_list.html', {'form': form, 'datas': datas})


# Edit Machine
def edit_DXFdata(request, data_id):
    data = get_object_or_404(DXF_data, id=data_id)

    if request.method == 'POST':
        form = DXFdataForm(request.POST, instance=data)
        if form.is_valid():
            form.save()
            return redirect('DXFdata_list')  # Redirect back to the main page
    else:
        form = DXFdataForm(instance=data)

    return render(request, 'edit_DXFdata.html', {'form': form, 'data': data})


# Delete DXF data
def delete_DXFdata(request, data_id):
    data = get_object_or_404(DXF_data, id=data_id)
    
    data.delete()
    return redirect('DXFdata_list')  # Redirect back to the list


#######################################


def APIkey_list(request):
    if request.method == "POST":
        
        form = APIkeyForm(request.POST)
        if form.is_valid():
            
            form.save() 

            
            return redirect('APIkey_list')
    else:
        form = APIkeyForm()
        
    
    datas = API_Keys.objects.all()
    
    return render(request, 'APIkey_list.html', {'form': form, 'datas': datas})


# Edit Machine
def edit_APIkey(request, data_id):
    data = get_object_or_404(API_Keys, id=data_id)

    if request.method == 'POST':
        form = APIkeyForm(request.POST, instance=data)
        if form.is_valid():
            form.save()
            return redirect('APIkey_list')  # Redirect back to the main page
    else:
        form = APIkeyForm(instance=data)

    return render(request, 'edit_APIkey.html', {'form': form, 'data': data})


# Delete DXF data
def delete_APIkey(request, data_id):
    data = get_object_or_404(API_Keys, id=data_id)
    
    data.delete()
    return redirect('APIkey_list')  # Redirect back to the list


#######################################

def manage_dxf_files(request):
    dxf_dir = os.path.join(settings.BASE_DIR, "static", "aDxfs")
    files = [f for f in os.listdir(dxf_dir) ]

    if request.method == 'POST':
        if 'upload' in request.POST:
            form = DXFUploadForm(request.POST, request.FILES)
            if form.is_valid():
                uploaded_file = form.cleaned_data['file']
                save_path = os.path.join(dxf_dir, uploaded_file.name)
                with open(save_path, 'wb+') as destination:
                    for chunk in uploaded_file.chunks():
                        destination.write(chunk)
                messages.success(request, "File uploaded successfully.")
                return redirect('manage_dxf_files')
        elif 'delete' in request.POST:
            file_to_delete = request.POST.get('file_name')
            delete_path = os.path.join(dxf_dir, file_to_delete)
            if os.path.exists(delete_path):
                os.remove(delete_path)
                messages.success(request, f"{file_to_delete} deleted.")
            else:
                messages.error(request, "File does not exist.")
            return redirect('manage_dxf_files')
    else:
        form = DXFUploadForm()

    return render(request, 'manage_dxf_files.html', {
        'files': files,
        'form': form
    })


#######################################

# Create Machine
def data_transfer_list(request):
     # Get the company of the logged-in user    
    user_company = None
    if request.user.is_authenticated:
        try:
            user_company = UserCompany.objects.get(user=request.user).company
        except UserCompany.DoesNotExist:
            user_company = None

    print(user_company)

    if request.method == 'POST':
        form = DataTransferForm(request.POST)
        
        if form.is_valid():
            form.save()
    else:
        form = DataTransferForm()

    # Fetch all current roles
    datas = DataTransfer.objects.filter(company=user_company)

    return render(request, 'data_transfer_list.html', {'form': form, 'datas': datas})

# Delete Machine
def delete_data_transfer_data(request, data_id):
    data = get_object_or_404(DataTransfer, id=data_id)
    
    data.delete()
    return redirect('data_transfer_list')  # Redirect back to the list



# Edit Machine
def edit_data_transfer_data(request, data_id):
    data = get_object_or_404(DataTransfer, id=data_id)

    

    if request.method == 'POST':
        form = DataTransferForm(request.POST, instance=data)
        if form.is_valid():
            form.save()
            return redirect('data_transfer_list')  # Redirect back to the main page
    else:
        form = DataTransferForm(instance=data)

    return render(request, 'edit_data_transfer_data.html', {'form': form, 'data': data})



#######################################