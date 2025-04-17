from django.shortcuts import render, redirect
from .forms import RegistrationForm, RoleForm, AuthoForm, UserRoleForm, RoleAuthoForm
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import AuthenticationForm
from .models import Role
from .models import Autho
from .models import UserRole
from .models import RoleAutho

from django.contrib.auth.models import User
from Apps.aAppMechanical.models import modelcalc
from Apps.aAppMechanical.models import Machine
from django.shortcuts import get_object_or_404

from django.contrib.auth.decorators import login_required
from django.contrib import messages



def home(request):
    return render(request, 'home.html')

def index(request):
    return render(request, 'index.html')



def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('index')  # Redirect to home page after registration
    else:
        form = RegistrationForm()
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



def modelcalc_list(request):
    records = modelcalc.objects.all()
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
    records = Machine.objects.all()
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
