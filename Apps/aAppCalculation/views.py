

from datetime import datetime
from Apps.aAdmin.models import UserRole, RoleAutho, Autho
from Apps.aAppMechanical.models import aLogEntry
from Apps.aAppSubmittal.models import AddMachine
from Apps.aAppProject.models import APP_Project
from .models import modelcalc
from Apps.aAppMechanical.models import UserCompany
import requests

from .forms import FormCalculationSheet, FormCalculationSheet_log

from django.http import HttpResponse
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.shortcuts import render, redirect
from django.utils.timezone import now 
from django.contrib.auth.models import User

import os
import ezdxf

from docx import Document
from docx.shared import Pt, RGBColor
from docx.enum.text import WD_PARAGRAPH_ALIGNMENT
from docx.oxml import OxmlElement, ns
from docx.shared import Inches
from docx.shared import Pt
# Create your views here.


def check_user_autho(username, autho_name):
    try:
        # Fetch the user by username
        user = User.objects.get(username=username)
        
        # Fetch the Autho by name
        autho = Autho.objects.get(name=autho_name)
        
        # Check if the user has a role and if that role has the specified Autho
        user_roles = UserRole.objects.filter(user=user)
        
        for user_role in user_roles:
            # Check if the role associated with the user has the specified Autho
            if RoleAutho.objects.filter(role=user_role.role, autho=autho).exists():
                return "T"  # User has the required Autho
            
        return "N"  # User does not have the required Autho
    
    except User.DoesNotExist:
        return "User not found"
    except Autho.DoesNotExist:
        return "Autho not found"

def interact_with_api(api_url, req_type, input_data):
    """
    Interact with the specified API by sending a POST request.

    Parameters:
        api_url (str): The API endpoint URL.
        req_type (str): The request type (e.g., 'MS').
        input_data (dict): A dictionary of input parameters.

    Returns:
        dict: The API response parsed into a Python dictionary.
    """
    # Prepare the payload
    payload = {
        **req_type,
        **input_data  # Merge the input data into the payload
    }

    try:
        # Send POST request
        response = requests.post(api_url, json=payload)

        # Raise an error for bad responses
        response.raise_for_status()

        # Parse and return the JSON response
        return response.json()

    except requests.exceptions.RequestException as e:
        print(f"Error while interacting with API: {e}")
        return None


###################################
###################################


def LoadPageCalculationSheet(request):
    machineShow = "Hide"
    # Redirect unauthenticated users
    if not request.user.is_authenticated:
        return redirect("login")
    
    # Get the company of the logged-in user    
    user_company = None
    if request.user.is_authenticated:
        try:
            user_company = UserCompany.objects.get(user=request.user).company
        except UserCompany.DoesNotExist:
            user_company = None

    print(user_company)

    sheet_keys = AddMachine.objects.exclude(nameFormCalcXX__isnull=True).exclude(nameFormCalcXX__exact="None").filter(company=user_company)

    sheet_key = None

    # If POST, get the selected sheet_key
    if request.method == "POST":
        sheet_key = request.POST.get("sheet_key")
        if sheet_key :
            machineShow = "Yes"

    #pdb.set_trace()
    print(sheet_key)
    

    result = check_user_autho(request.user.username, sheet_key)
    print('#####')
    print(result)
    print('######')
    
    print(request.user)
    print(f"{request.user} accessed Load {sheet_key}")
    ###LOG
    
    aLogEntry.objects.create(
        user=request.user,
        message=f"{request.user} >>> {sheet_key}"
    )
    

    #Define Retrieve values from AddMachine model
    try:
        machine_config = AddMachine.objects.get(keyValue=sheet_key, company=user_company)
        form_type = machine_config.nameFormCalcXX
        aMachineName = machine_config.nameMachine
    except AddMachine.DoesNotExist:
        form_type = "None"
        aMachineName = "None"
        


    # Optional: Handle cases where the sheet_key is invalid
    if form_type is None:
        print(f"Warning: Unknown sheet_key '{sheet_key}'")


     # Assign company filter only if the user has a company
    if user_company:
        machines = modelcalc.objects.filter(oSec00Field03=sheet_key, company=user_company)
        projects = APP_Project.objects.filter(company=user_company)
    else:
        machines = modelcalc.objects.none()  # Return an empty queryset if no company
        projects = APP_Project.objects.none()  # Return an empty queryset if no company

    print(form_type)


    form = FormCalculationSheet(form_type=form_type)
    
    print(f"Initial value for oSec01Field02: {form.fields['oSec01Field02'].initial}")
    
    # Initialize all section variables
    aSection01Field01Show = "Yes"
    aSection01Field02Show = "Yes"
    aSection01Field03Show = "Yes"
    aSection01Field04Show = "Yes"
    aSection01Field05Show = "Yes"
    aSection01Field06Show = "Yes"
    aSection01Field07Show = "Yes"
    aSection01Field08Show = "Yes"
    aSection01Field09Show = "Yes"
    aSection01Field10Show = "Yes"
    aSection01Field11Show = "Yes"
    aSection01Field12Show = "Yes"
    aSection01Field13Show = "Yes"
    aSection01Field14Show = "Yes"
    aSection01Field15Show = "Yes"
    aSection01Field16Show = "Yes"
    aSection01Field17Show = "Yes"
    aSection01Field18Show = "Yes"
    aSection01Field19Show = "Yes"
    aSection01Field20Show = "Yes"
    aSection01Field21Show = "Yes"
    aSection01Field22Show = "Yes"
    aSection01Field23Show = "Yes"
    aSection01Field24Show = "Yes"
    aSection01Field25Show = "Yes"
    aSection01Field26Show = "Yes"
    aSection01Field27Show = "Yes"
    aSection01Field28Show = "Yes"
    aSection01Field29Show = "Yes"
    aSection01Field30Show = "Yes"
    aSection02Field01Show = "Yes"
    aSection02Field02Show = "Yes"
    aSection02Field03Show = "Yes"
    aSection02Field04Show = "Yes"
    aSection02Field05Show = "Yes"
    aSection02Field06Show = "Yes"
    aSection02Field07Show = "Yes"
    aSection02Field08Show = "Yes"
    aSection02Field09Show = "Yes"
    aSection02Field10Show = "Yes"
    aSection02Field11Show = "Yes"
    aSection02Field12Show = "Yes"
    aSection02Field13Show = "Yes"
    aSection02Field14Show = "Yes"
    aSection02Field15Show = "Yes"
    aSection02Field16Show = "Yes"
    aSection02Field17Show = "Yes"
    aSection02Field18Show = "Yes"
    aSection02Field19Show = "Yes"
    aSection02Field20Show = "Yes"
    aSection02Field21Show = "Yes"
    aSection02Field22Show = "Yes"
    aSection02Field23Show = "Yes"
    aSection02Field24Show = "Yes"
    aSection02Field25Show = "Yes"
    aSection02Field26Show = "Yes"
    aSection02Field27Show = "Yes"
    aSection02Field28Show = "Yes"
    aSection02Field29Show = "Yes"
    aSection02Field30Show = "Yes"
    
    print(form.fields['oSec01Field01'].initial)
    print(form.fields['oSec01Field02'].initial)
    print(form.fields['oSec01Field03'].initial)
    print(form.fields['oSec01Field04'].initial)
    print(form.fields['oSec01Field05'].initial)
    print(form.fields['oSec01Field06'].initial)
    print(form.fields['oSec01Field07'].initial)
    print(form.fields['oSec01Field08'].initial)
    print(form.fields['oSec01Field09'].initial)
    print(form.fields['oSec01Field10'].initial)
    print(form.fields['oSec01Field11'].initial)
    print(form.fields['oSec01Field12'].initial)
    print(form.fields['oSec01Field13'].initial)
    print(form.fields['oSec01Field14'].initial)
    print(form.fields['oSec01Field15'].initial)
    print(form.fields['oSec01Field16'].initial)
    print(form.fields['oSec01Field17'].initial)
    print(form.fields['oSec01Field18'].initial)
    print(form.fields['oSec01Field19'].initial)
    print(form.fields['oSec01Field20'].initial)
    print(form.fields['oSec01Field21'].initial)
    print(form.fields['oSec01Field22'].initial)
    print(form.fields['oSec01Field23'].initial)
    print(form.fields['oSec01Field24'].initial)
    print(form.fields['oSec01Field25'].initial)
    print(form.fields['oSec01Field26'].initial)
    print(form.fields['oSec01Field27'].initial)
    print(form.fields['oSec01Field28'].initial)
    print(form.fields['oSec01Field29'].initial)
    print(form.fields['oSec01Field30'].initial)
    print(form.fields['oSec02Field01'].initial)
    print(form.fields['oSec02Field02'].initial)
    print(form.fields['oSec02Field03'].initial)
    print(form.fields['oSec02Field04'].initial)
    print(form.fields['oSec02Field05'].initial)
    print(form.fields['oSec02Field06'].initial)
    print(form.fields['oSec02Field07'].initial)
    print(form.fields['oSec02Field08'].initial)
    print(form.fields['oSec02Field09'].initial)
    print(form.fields['oSec02Field10'].initial)
    print(form.fields['oSec02Field11'].initial)
    print(form.fields['oSec02Field12'].initial)
    print(form.fields['oSec02Field13'].initial)
    print(form.fields['oSec02Field14'].initial)
    print(form.fields['oSec02Field15'].initial)
    print(form.fields['oSec02Field16'].initial)
    print(form.fields['oSec02Field17'].initial)
    print(form.fields['oSec02Field18'].initial)
    print(form.fields['oSec02Field19'].initial)
    print(form.fields['oSec02Field20'].initial)
    print(form.fields['oSec02Field21'].initial)
    print(form.fields['oSec02Field22'].initial)
    print(form.fields['oSec02Field23'].initial)
    print(form.fields['oSec02Field24'].initial)
    print(form.fields['oSec02Field25'].initial)
    print(form.fields['oSec02Field26'].initial)
    print(form.fields['oSec02Field27'].initial)
    print(form.fields['oSec02Field28'].initial)
    print(form.fields['oSec02Field29'].initial)
    print(form.fields['oSec02Field30'].initial)

    # Apply conditions to modify the values
    if form.fields['oSec01Field01'].initial in ["oooo", None , ""]:
        aSection01Field01Show = "Hide"
    if form.fields['oSec01Field02'].initial in ["oooo", None , ""]:
        aSection01Field02Show = "Hide"
    if form.fields['oSec01Field03'].initial in ["oooo", None , ""]:
        aSection01Field03Show = "Hide"
    if form.fields['oSec01Field04'].initial in ["oooo", None , ""]:
        aSection01Field04Show = "Hide"
    if form.fields['oSec01Field05'].initial in ["oooo", None , ""]:
        aSection01Field05Show = "Hide"
    if form.fields['oSec01Field06'].initial in ["oooo", None , ""]:
        aSection01Field06Show = "Hide"
    if form.fields['oSec01Field07'].initial in ["oooo", None , ""]:
        aSection01Field07Show = "Hide"
    if form.fields['oSec01Field08'].initial in ["oooo", None , ""]:
        aSection01Field08Show = "Hide"
    if form.fields['oSec01Field09'].initial in ["oooo", None , ""]:
        aSection01Field09Show = "Hide"
    if form.fields['oSec01Field10'].initial in ["oooo", None , ""]:
        aSection01Field10Show = "Hide"
    if form.fields['oSec01Field11'].initial in ["oooo", None , ""]:
        aSection01Field11Show = "Hide"
    if form.fields['oSec01Field12'].initial in ["oooo", None , ""]:
        aSection01Field12Show = "Hide"
    if form.fields['oSec01Field13'].initial in ["oooo", None , ""]:
        aSection01Field13Show = "Hide"
    if form.fields['oSec01Field14'].initial in ["oooo", None , ""]:
        aSection01Field14Show = "Hide"
    if form.fields['oSec01Field15'].initial in ["oooo", None , ""]:
        aSection01Field15Show = "Hide"
    if form.fields['oSec01Field16'].initial in ["oooo", None , ""]:
        aSection01Field16Show = "Hide"
    if form.fields['oSec01Field17'].initial in ["oooo", None , ""]:
        aSection01Field17Show = "Hide"
    if form.fields['oSec01Field18'].initial in ["oooo", None , ""]:
        aSection01Field18Show = "Hide"
    if form.fields['oSec01Field19'].initial in ["oooo", None , ""]:
        aSection01Field19Show = "Hide"
    if form.fields['oSec01Field20'].initial in ["oooo", None , ""]:
        aSection01Field20Show = "Hide"
    if form.fields['oSec01Field21'].initial in ["oooo", None , ""]:
        aSection01Field21Show = "Hide"
    if form.fields['oSec01Field22'].initial in ["oooo", None , ""]:
        aSection01Field22Show = "Hide"
    if form.fields['oSec01Field23'].initial in ["oooo", None , ""]:
        aSection01Field23Show = "Hide"
    if form.fields['oSec01Field24'].initial in ["oooo", None , ""]:
        aSection01Field24Show = "Hide"
    if form.fields['oSec01Field25'].initial in ["oooo", None , ""]:
        aSection01Field25Show = "Hide"
    if form.fields['oSec01Field26'].initial in ["oooo", None , ""]:
        aSection01Field26Show = "Hide"
    if form.fields['oSec01Field27'].initial in ["oooo", None , ""]:
        aSection01Field27Show = "Hide"
    if form.fields['oSec01Field28'].initial in ["oooo", None , ""]:
        aSection01Field28Show = "Hide"
    if form.fields['oSec01Field29'].initial in ["oooo", None , ""]:
        aSection01Field29Show = "Hide"
    if form.fields['oSec01Field30'].initial in ["oooo", None , ""]:
        aSection01Field30Show = "Hide"

    if form.fields['oSec02Field01'].initial in ["oooo", None , ""]:
        aSection02Field01Show = "Hide"
    if form.fields['oSec02Field02'].initial in ["oooo", None , ""]:
        aSection02Field02Show = "Hide"
    if form.fields['oSec02Field03'].initial in ["oooo", None , ""]:
        aSection02Field03Show = "Hide"
    if form.fields['oSec02Field04'].initial in ["oooo", None , ""]:
        aSection02Field04Show = "Hide"
    if form.fields['oSec02Field05'].initial in ["oooo", None , ""]:
        aSection02Field05Show = "Hide"
    if form.fields['oSec02Field06'].initial in ["oooo", None , ""]:
        aSection02Field06Show = "Hide"
    if form.fields['oSec02Field07'].initial in ["oooo", None , ""]:
        aSection02Field07Show = "Hide"
    if form.fields['oSec02Field08'].initial in ["oooo", None , ""]:
        aSection02Field08Show = "Hide"
    if form.fields['oSec02Field09'].initial in ["oooo", None , ""]:
        aSection02Field09Show = "Hide"
    if form.fields['oSec02Field10'].initial in ["oooo", None , ""]:
        aSection02Field10Show = "Hide"
    if form.fields['oSec02Field11'].initial in ["oooo", None , ""]:
        aSection02Field11Show = "Hide"
    if form.fields['oSec02Field12'].initial in ["oooo", None , ""]:
        aSection02Field12Show = "Hide"
    if form.fields['oSec02Field13'].initial in ["oooo", None , ""]:
        aSection02Field13Show = "Hide"
    if form.fields['oSec01Field14'].initial in ["oooo", None , ""]:
        aSection02Field14Show = "Hide"
    if form.fields['oSec02Field15'].initial in ["oooo", None , ""]:
        aSection02Field15Show = "Hide"
    if form.fields['oSec02Field16'].initial in ["oooo", None , ""]:
        aSection02Field16Show = "Hide"
    if form.fields['oSec02Field17'].initial in ["oooo", None , ""]:
        aSection02Field17Show = "Hide"
    if form.fields['oSec02Field18'].initial in ["oooo", None , ""]:
        aSection02Field18Show = "Hide"
    if form.fields['oSec02Field19'].initial in ["oooo", None , ""]:
        aSection02Field19Show = "Hide"
    if form.fields['oSec02Field20'].initial in ["oooo", None , ""]:
        aSection02Field20Show = "Hide"
    if form.fields['oSec02Field21'].initial in ["oooo", None , ""]:
        aSection02Field21Show = "Hide"
    if form.fields['oSec02Field22'].initial in ["oooo", None , ""]:
        aSection02Field22Show = "Hide"
    if form.fields['oSec02Field23'].initial in ["oooo", None , ""]:
        aSection02Field23Show = "Hide"
    if form.fields['oSec01Field24'].initial in ["oooo", None , ""]:
        aSection02Field24Show = "Hide"
    if form.fields['oSec02Field25'].initial in ["oooo", None , ""]:
        aSection02Field25Show = "Hide"
    if form.fields['oSec02Field26'].initial in ["oooo", None , ""]:
        aSection02Field26Show = "Hide"
    if form.fields['oSec02Field27'].initial in ["oooo", None , ""]:
        aSection02Field27Show = "Hide"
    if form.fields['oSec02Field28'].initial in ["oooo", None , ""]:
        aSection02Field28Show = "Hide"
    if form.fields['oSec02Field29'].initial in ["oooo", None , ""]:
        aSection02Field29Show = "Hide"
    if form.fields['oSec02Field30'].initial in ["oooo", None , ""]:
        aSection02Field30Show = "Hide"
    
    print(aSection01Field01Show)
    print(aSection01Field02Show)
    print(aSection01Field03Show)
    print(aSection01Field04Show)
    print(aSection01Field05Show)
    print(aSection01Field06Show)
    print(aSection01Field07Show)
    print(aSection01Field08Show)
    print(aSection01Field09Show)
    print(aSection01Field10Show)
    print(aSection01Field11Show)
    print(aSection01Field12Show)
    print(aSection01Field13Show)
    print(aSection01Field14Show)
    print(aSection01Field15Show)
    print(aSection01Field16Show)
    print(aSection01Field17Show)
    print(aSection01Field18Show)
    print(aSection01Field19Show)
    print(aSection01Field20Show)
    print(aSection01Field21Show)
    print(aSection01Field22Show)
    print(aSection01Field23Show)
    print(aSection01Field24Show)
    print(aSection01Field25Show)
    print(aSection01Field26Show)
    print(aSection01Field27Show)
    print(aSection01Field28Show)
    print(aSection01Field29Show)
    print(aSection01Field30Show)
    print(aSection02Field01Show)
    print(aSection02Field02Show)
    print(aSection02Field03Show)
    print(aSection02Field04Show)
    print(aSection02Field05Show)
    print(aSection02Field06Show)
    print(aSection02Field07Show)
    print(aSection02Field08Show)
    print(aSection02Field09Show)
    print(aSection02Field10Show)
    print(aSection02Field11Show)
    print(aSection02Field12Show)
    print(aSection02Field13Show)
    print(aSection02Field14Show)
    print(aSection02Field15Show)
    print(aSection02Field16Show)
    print(aSection02Field17Show)
    print(aSection02Field18Show)
    print(aSection02Field19Show)
    print(aSection02Field20Show)
    print(aSection02Field21Show)
    print(aSection02Field22Show)
    print(aSection02Field23Show)
    print(aSection02Field24Show)
    print(aSection02Field25Show)
    print(aSection02Field26Show)
    print(aSection02Field27Show)
    print(aSection02Field28Show)
    print(aSection02Field29Show)
    print(aSection02Field30Show)
    

    return render(request, "PageCalculationSheet.html", {
    "form": form,
    "machines": machines,
    "projects": projects,  
    "aMachineName": aMachineName, 
    "user_company": user_company, 
    "sheet_key": sheet_key,
    "sheet_keys": sheet_keys,
    "machineShow": machineShow,
    "aSection01Field01Show": aSection01Field01Show,
    "aSection01Field02Show": aSection01Field02Show,
    "aSection01Field03Show": aSection01Field03Show,
    "aSection01Field04Show": aSection01Field04Show,
    "aSection01Field05Show": aSection01Field05Show,
    "aSection01Field06Show": aSection01Field06Show,
    "aSection01Field07Show": aSection01Field07Show,
    "aSection01Field08Show": aSection01Field08Show,
    "aSection01Field09Show": aSection01Field09Show,
    "aSection01Field10Show": aSection01Field10Show,
    "aSection01Field11Show": aSection01Field11Show,
    "aSection01Field12Show": aSection01Field12Show,
    "aSection01Field13Show": aSection01Field13Show,
    "aSection01Field14Show": aSection01Field14Show,
    "aSection01Field15Show": aSection01Field15Show,
    "aSection01Field16Show": aSection01Field16Show,
    "aSection01Field17Show": aSection01Field17Show,
    "aSection01Field18Show": aSection01Field18Show,
    "aSection01Field19Show": aSection01Field19Show,
    "aSection01Field20Show": aSection01Field20Show,
    "aSection01Field21Show": aSection01Field21Show,
    "aSection01Field22Show": aSection01Field22Show,
    "aSection01Field23Show": aSection01Field23Show,
    "aSection01Field24Show": aSection01Field24Show,
    "aSection01Field25Show": aSection01Field25Show,
    "aSection01Field26Show": aSection01Field26Show,
    "aSection01Field27Show": aSection01Field27Show,
    "aSection01Field28Show": aSection01Field28Show,
    "aSection01Field29Show": aSection01Field29Show,
    "aSection01Field30Show": aSection01Field30Show,
    "aSection02Field01Show": aSection02Field01Show,
    "aSection02Field02Show": aSection02Field02Show,
    "aSection02Field03Show": aSection02Field03Show,
    "aSection02Field04Show": aSection02Field04Show,
    "aSection02Field05Show": aSection02Field05Show,
    "aSection02Field06Show": aSection02Field06Show,
    "aSection02Field07Show": aSection02Field07Show,
    "aSection02Field08Show": aSection02Field08Show,
    "aSection02Field09Show": aSection02Field09Show,
    "aSection02Field10Show": aSection02Field10Show,
    "aSection02Field11Show": aSection02Field11Show,
    "aSection02Field12Show": aSection02Field12Show,
    "aSection02Field13Show": aSection02Field13Show,
    "aSection02Field14Show": aSection02Field14Show,
    "aSection02Field15Show": aSection02Field15Show,
    "aSection02Field16Show": aSection02Field16Show,
    "aSection02Field17Show": aSection02Field17Show,
    "aSection02Field18Show": aSection02Field18Show,
    "aSection02Field19Show": aSection02Field19Show,
    "aSection02Field20Show": aSection02Field20Show,
    "aSection02Field21Show": aSection02Field21Show,
    "aSection02Field22Show": aSection02Field22Show,
    "aSection02Field23Show": aSection02Field23Show,
    "aSection02Field24Show": aSection02Field24Show,
    "aSection02Field25Show": aSection02Field25Show,
    "aSection02Field26Show": aSection02Field26Show,
    "aSection02Field27Show": aSection02Field27Show,
    "aSection02Field28Show": aSection02Field28Show,
    "aSection02Field29Show": aSection02Field29Show,
    "aSection02Field30Show": aSection02Field30Show,
    
})

def HandleCalculationSheetForm(request):
    sheet_key = request.POST.get("sheet_key")
    print(sheet_key)
    if sheet_key :
            machineShow = "Yes"
    if not request.user.is_authenticated:
        return redirect('login')
    
    print(request.user)
    print(f"{request.user} accessed Load {sheet_key}")
    
    # Get the company of the logged-in user    
    user_company = None
    firstletter = None
    if request.user.is_authenticated:
        try:
            user_company = UserCompany.objects.get(user=request.user).company
            firstletter = user_company.nameCompanies[0]
        except UserCompany.DoesNotExist:
            user_company = None

    print(user_company)

    sheet_keys = AddMachine.objects.exclude(nameFormCalcXX__isnull=True).exclude(nameFormCalcXX__exact="None").filter(company=user_company)
    


    form_mapping = {
        f"NS_{firstletter}": {
            "input_fields": {
                "NS_Ch_Height":       'oSec01Field02', 
                "NS_Ch_Width":        'oSec01Field04', 
                "NS_WaterLv":         'oSec01Field06', 
                "NS_WaterLv_Margin":  'oSec01Field08',
                "NS_Bar_Spacing":     'oSec01Field10', 
                "NS_Bar_Th":          'oSec01Field12', 
                "NS_Bar_Width":       'oSec01Field14', 
                "NS_Angle":           'oSec01Field16',
            },
            "output_fields": {
                "oSec02Field02": "O_Weight",
            },
            "req_type": {
                "reqType": "NS"
            },
        },
        f"MS_{firstletter}": {
            "input_fields": {
                "MS_ChannelHeight":     'oSec01Field02',
                "MS_ScreenWidth":       'oSec01Field04',
                "MS_BeltHeight":        'oSec01Field06',
                "MS_WaterLevel":        'oSec01Field08',
                "MS_BarSpacing":        'oSec01Field10',
                "MS_BarThickness":      'oSec01Field12',
                "MS_BarWidth":          'oSec01Field14',
                "MS_InclinationDegree": 'oSec01Field16',
                "MS_SprocketDiameter":  'oSec01Field18',
                "MS_Velocity":          'oSec01Field20',
                "MS_FOS":               'oSec01Field22',
            },
            "output_fields": {
                "oSec02Field02": "MS_w",
                "oSec02Field04": "MS_p",
                "oSec02Field06": "MS_s",
            },
            "req_type": {
                "reqType": "MS"
            },
        },
        f"BC_{firstletter}": {
            "input_fields": {
                "BC_Length": 'oSec01Field02',
                "BC_Width": 'oSec01Field04',
                "BC_DrumDia": 'oSec01Field06',
                "BC_Friction": 'oSec01Field08',
                "BC_Velocity": 'oSec01Field10',
                "BC_FOS": 'oSec01Field12',
            },
            "output_fields": {
                "oSec02Field02": "BC_w",
                "oSec02Field04": "BC_p",
                "oSec02Field06": "BC_s",
            },
            "req_type": {
                "reqType": "BC"
            },
        },
        f"GR_{firstletter}": {
            "input_fields": {
                "GR_n_channel":       'oSec01Field02',
                "GR_channel_width":   'oSec01Field04',
                "GR_civil_width":     'oSec01Field06',
                "GR_bridge_length":   'oSec01Field08',
                "GR_wheel_diameter":  'oSec01Field10',
                "GR_Friction":        'oSec01Field12',
                "GR_Velocity":        'oSec01Field14',
                "GR_FOS":        'oSec01Field16',
            },
            "output_fields": {
                "oSec02Field02": "GR_out3",
                "oSec02Field04": "GR_out1",
                "oSec02Field06": "GR_out2",
                "oSec02Field08": "GR_out4",
                "oSec02Field10": "GR_out5",
                "oSec02Field12": "GR_out6",
            },
            "req_type": {
                "reqType": "GR"
            },
        },
        f"PS_{firstletter}": {
            "input_fields": {
                "PS_walkway_length": 'oSec01Field02',
                "PS_Friction":       'oSec01Field04',
                "PS_Velocity":       'oSec01Field06',
                "PS_FOS":        'oSec01Field08',
            },
            "output_fields": {
                "oSec02Field02": "PS_out2",
                "oSec02Field04": "PS_out1",
                "oSec02Field06": "000",
                "oSec02Field08": "PS_out3",
                "oSec02Field10": "PS_out4",
            },
            "req_type": {
                "reqType": "PS"
            },
        },
        f"TH_{firstletter}": {
            "input_fields": {
                "TH_diameter":  'oSec01Field02', 
                "TH_n_arm":     'oSec01Field04', 
                "TH_Velocity":  'oSec01Field06', 
                "TH_FOS":       'oSec01Field08',
            },
            "output_fields": {
                "oSec02Field02": "TH_w",
                "oSec02Field04": "TH_p",
                "oSec02Field06": "TH_s",
            },
            "req_type": {
                "reqType": "TH"
            },
        },
        f"MX_{firstletter}": {
            "input_fields": {
                "MX_length":        'oSec01Field02', 
                "MX_width":         'oSec01Field04', 
                "MX_water_depth":           'oSec01Field06', 
                "MX_tank_depth":            'oSec01Field08',
                "MX_impeller_coefficient":  'oSec01Field10', 
                "MX_velocity_gradient":     'oSec01Field12', 
                "MX_impeller_diameter_factor":  'oSec01Field14', 
                "MX_safety_factor":             'oSec01Field16',
            },
            "output_fields": {
                "oSec02Field02": "000",
                "oSec02Field04": "MX_p",
                "oSec02Field06": "MX_s",
                "oSec02Field08": "MX_d",
                "oSec02Field10": "MX_shaftL",
                "oSec02Field12": "MX_shaftD",
                "oSec02Field14": "MX_Type",
            },
            "req_type": {
                "reqType": "MX"
            },
        },
        f"RT_{firstletter}": {
            "input_fields": {
                "RT_Length":    'oSec01Field02', 
                "RT_Width":     'oSec01Field04', 
                "RT_Hight":     'oSec01Field06', 
                "RT_ShellTH":   'oSec01Field08',
                "RT_BaseTH":    'oSec01Field10', 
                "RT_N_Spliter": 'oSec01Field12',
            },
            "output_fields": {
                "oSec02Field02": "RT_w10",
            },
            "req_type": {
                "reqType": "RT"
            },
        },
        f"CT_{firstletter}": {
            "input_fields": {
                "CT_Diameter": 'oSec01Field02', 
                "CT_Height": 'oSec01Field04',
            },
            "output_fields": {
                "oSec02Field02": "O_Tank_Weight",
                "oSec02Field04": "O_Tank_Volume",
                "oSec02Field06": "O_Tank_Shell_Th",
                "oSec02Field08": "O_Tank_Base_Th",
                "oSec02Field10": "O_Tank_Shell_Weight",
                "oSec02Field12": "O_Tank_Base_Weight",
                "oSec02Field14": "O_Tank_Base_UPN_Weight",
                "oSec02Field16": "O_Tank_Cover_Weight",
            },
            "req_type": {
                "reqType": "CT"
            },
        },
        f"SC_{firstletter}": {
            "input_fields": {
                "aInput01": 'oSec01Field02', 
                "aInput02": 'oSec01Field04', 
                "aInput03": 'oSec01Field06', 
                "aInput04": 'oSec01Field08',
                "aInput05": 'oSec01Field10', 
                "aInput06": 'oSec01Field12', 
                "aInput07": 'oSec01Field14', 
                "aInput08": 'oSec01Field16',
            },
            "output_fields": {
                "oSec02Field02": "Pitch",
                "oSec02Field04": "SpeedRPM",
                "oSec02Field06": "MotorPower",
                "oSec02Field08": "ScrewWeight",
                "oSec02Field10": "FrameWeight",
                "oSec02Field12": "1111",
            },
            "req_type": {
                "reqType": "SC"
            },
        },
        f"BS_{firstletter}": {
            "input_fields": {
                "BS_Bar_Dia":     'oSec01Field02', 
                "BS_Bar_Space":     'oSec01Field04', 
                "BS_Screen_Height": 'oSec01Field06', 
                "BS_Screen_Width":  'oSec01Field08',
                "BS_Screen_Depth":  'oSec01Field10', 
                "BS_Plate_Th":      'oSec01Field12',
            },
            "output_fields": {
                "oSec02Field02": "O_Weight_allBars",
                "oSec02Field04": "O_Plate_weight",
                "oSec02Field06": "O_Total_weight",
            },
            "req_type": {
                "reqType": "BS"
            },
        },
        f"PNch_{firstletter}": {
            "input_fields": {
                "PNch_Channel_Height":             'oSec01Field02', 
                "PNch_Frame_Height_Over_Channel":  'oSec01Field04', 
                "PNch_Channel_Width":              'oSec01Field06', 
                "PNch_Gate_Margin_Width":          'oSec01Field08',
                "PNch_Water_Lv":                   'oSec01Field10', 
                "PNch_Gate_Margin_Over_Water_Lv":  'oSec01Field12', 
                "PNch_Gate_Th":                    'oSec01Field14', 
                "PNch_Gate_Other_PLs":             'oSec01Field16',
                "PNch_HeadStock":                  'oSec01Field18', 
                "PNch_Frame_Weight_Per_M":         'oSec01Field20',
            },
            "output_fields": {
                "oSec02Field02": "O_Frame_Perimeter",
                "oSec02Field04": "O_Frame_Weight",
                "oSec02Field06": "O_Gate_PL_Weight",
                "oSec02Field08": "O_Gate_Stiffener_N",
                "oSec02Field10": "O_Gate_Stiffener_Weight",
                "oSec02Field12": "O_Gate_Weight",
                "oSec02Field14": "O_Total_Weight",
            },
            "req_type": {
                "reqType": "PNch"
            },
        },
        f"PNwa_{firstletter}": {
            "input_fields": {
                "aInput01":   'oSec01Field03', 
                "aInput02":   'oSec01Field04', 
                "aInput03":   'oSec01Field06', 
                "aInput04":   'oSec01Field08',
                "aInput05":   'oSec01Field10', 
                "aInput06":   'oSec01Field12', 
                "aInput07":   'oSec01Field14', 
                "aInput08":   'oSec01Field16',
                "aInput09":   'oSec01Field18', 
                "aInput10":   'oSec01Field20',
            },
            "output_fields": {
                "oSec02Field02": "O_PNwa_Out01",
                "oSec02Field04": "O_PNwa_Out02",
                "oSec02Field06": "O_PNwa_Out03",
                "oSec02Field08": "O_PNwa_Out04",
                "oSec02Field10": "O_PNwa_Out05",
                "oSec02Field12": "O_PNwa_Out06",
                "oSec02Field14": "O_PNwa_Out07",
            },
            "req_type": {
                "reqType": "PNwa"
            },
        },
    }
    
    #Define Retrieve values from AddMachine model
    try:
        machine_config = AddMachine.objects.get(keyValue=sheet_key, company=user_company)
        form_type = machine_config.nameFormCalcXX
        aMachineName = machine_config.nameMachine
    except AddMachine.DoesNotExist:
        form_type = "None"
        aMachineName = "None"
        


    config = form_mapping.get(sheet_key)
    if not config:
        return redirect('PageCalculationSheet.html')  # Or a 404 page

    
    req_type = config['req_type']
    input_fields = config['input_fields']
    output_fields = config['output_fields']

    # Assign company filter only if the user has a company
    if user_company:
        machines = modelcalc.objects.filter(oSec00Field03=sheet_key, company=user_company)
        projects = APP_Project.objects.filter(company=user_company)
    else:
        machines = modelcalc.objects.none()  # Return an empty queryset if no company
        projects = APP_Project.objects.none()  # Return an empty queryset if no company
    
    print(user_company)

    ###LOG
    
    aLogEntry.objects.create(
        user=request.user,
        message=f"{request.user} Calculated >>> {sheet_key} "
    )

    if request.method == 'POST' and 'form1_submit' in request.POST:
        form = FormCalculationSheet(form_type=form_type, data=request.POST)
        if form.is_valid():
            

            input_data = {
                f"{api_key}": form.cleaned_data.get(field)
                for api_key, field in input_fields.items() if form.cleaned_data.get(field) is not None
            }
            print ("input_data : ", input_data)
            


            response = interact_with_api(
                "https://us-central1-h1000project1.cloudfunctions.net/f01",
                req_type,
                input_data
            )

            print("response : ", response)



            instance = form.save(commit=False)
            for form_field, api_key in output_fields.items():
                if api_key not in ["000", "1111"]:
                    setattr(instance, form_field, response[api_key])
            instance.oSec00Field01 = request.user.username
            instance.oSec00Field02 = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            instance.oSec00Field03 = sheet_key


            # Handle project assignment
            project_id = request.POST.get("project")
            if project_id:
                try:
                    instance.project = APP_Project.objects.get(id=project_id)
                except APP_Project.DoesNotExist:
                    """ return render(request, "PageCalculationSheet.html", {"form": form, "sheet_keys": sheet_keys, "projects": projects, "machines": machines, "aMachineName": aMachineName, "sheet_key": sheet_key, "machineShow": "Yes",  "error": "Invalid Project ID"})
            else:
                return render(request, "PageCalculationSheet.html", {"form": form, "sheet_keys": sheet_keys, "projects": projects, "machines": machines, "aMachineName": aMachineName, "sheet_key": sheet_key, "machineShow": "Yes",  "error": "Project is required"})
            """ 
            # Get the company associated with the user
            try:
                user_company = UserCompany.objects.get(user=request.user).company
                instance.company = user_company  # Assign company to the instance
            except UserCompany.DoesNotExist:
                return render(request, "PageCalculationSheet.html", 
                              {"form": form, 
                               "error": "User is not associated with a company",
                               "aMachineName": aMachineName,
                               "sheet_key" : sheet_key,
                               "sheet_keys": sheet_keys,
                               "machineShow":machineShow,})

            instance.save()

            # Refill form for display
            initial_data = {form_field: form.cleaned_data.get(form_field) for form_field in input_fields.values()}
            for form_field, api_key in output_fields.items():
                if api_key not in ["000", "1111"]:
                    initial_data[form_field] = response[api_key]

            form = FormCalculationSheet(form_type=form_type, initial=initial_data)

            form1 = FormCalculationSheet_log(form_type=form_type, data=request.POST)
            if form1.is_valid():


                input_data1 = {
                    f"{api_key}": form1.cleaned_data.get(field)
                    for api_key, field in input_fields.items() if form1.cleaned_data.get(field) is not None
                }
                print ("input_data1 : ", input_data1)


                response1 = interact_with_api(
                    "https://us-central1-h1000project1.cloudfunctions.net/f01",
                    req_type,
                    input_data1
                )

                print("response1 : ", response1)



                instance1 = form1.save(commit=False)
                for form_field, api_key in output_fields.items():
                    if api_key not in ["000", "1111"]:
                        setattr(instance1, form_field, response1[api_key])
                instance1.oSec00Field01 = request.user.username
                instance1.oSec00Field02 = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                instance1.oSec00Field03 = sheet_key


                if project_id:
                    try:
                        instance1.project = APP_Project.objects.get(id=project_id)
                    except APP_Project.DoesNotExist:
                        """ return render(request, "PageCalculationSheet.html", {"form": form, "sheet_keys": sheet_keys, "projects": projects, "machines": machines, "aMachineName": aMachineName, "sheet_key": sheet_key, "machineShow": "Yes", "error": "Invalid Project ID"})
                else:
                    return render(request, "PageCalculationSheet.html", {"form": form, "sheet_keys": sheet_keys, "projects": projects, "machines": machines, "aMachineName": aMachineName, "sheet_key": sheet_key, "machineShow": "Yes",  "error": "Project is required"}) """

                # Get the company associated with the user
                try:
                    user_company = UserCompany.objects.get(user=request.user).company
                    instance1.company = user_company  # Assign company to the instance
                except UserCompany.DoesNotExist:
                    return render(request, "PageCalculationSheet.html", 
                                  {"form": form, 
                                   "error": "User is not associated with a company",
                                   "aMachineName": aMachineName,
                                   "sheet_key" : sheet_key,
                                   "sheet_keys": sheet_keys,
                                   "machineShow":machineShow,})

                instance1.save()

                # Refill form for display
                initial_data1 = {form_field: form1.cleaned_data.get(form_field) for form_field in input_fields.values()}
                for form_field, api_key in output_fields.items():
                    if api_key not in ["000", "1111"]:
                        initial_data1[form_field] = response1[api_key]

                form1 = FormCalculationSheet_log(form_type=form_type, initial=initial_data1)
            

            # Initialize visibility dictionaries
            aSection01FieldShow = {f"aSection01Field{str(i).zfill(2)}Show": "Hide" for i in range(1, 21)}
            aSection02FieldShow = {f"aSection02Field{str(i).zfill(2)}Show": "Hide" for i in range(1, 21)}
            
            # Update visibility based on field counts
            for i in range(1, len(input_fields)*2 + 1):
                aSection01FieldShow[f"aSection01Field{str(i).zfill(2)}Show"] = "Yes"
            
            for i in range(1, len(output_fields)*2 + 1):
                aSection02FieldShow[f"aSection02Field{str(i).zfill(2)}Show"] = "Yes"
            
            
            

            return render(request, 'PageCalculationSheet.html', {
                'form': form,
                'sheet_keys': sheet_keys,
                'sheet_key': sheet_key,
                'machines': machines,
                'projects': projects,  
                'machineShow': machineShow,
                'aMachineName': aMachineName, 
                'user_company': user_company, 
                **aSection01FieldShow,
                **aSection02FieldShow,
            })

    return redirect("PageCalculationSheet")

def generate_report(request):
    sheet_key = request.POST.get("sheet_key")
    print(sheet_key)
    try:
        #pdb.set_trace()
        # Log the action
        aLogEntry.objects.create(user=request.user, message=f"at {now()} {request.user} accessed Word Report")
        
        #pdb.set_trace()
        # Get the user’s company and project
        aCompany = UserCompany.objects.get(user=request.user)

        project_id = request.POST.get("project")

        #pdb.set_trace()
        # Determine the company and generate the corresponding report
        if aCompany.company.nameCompanies == "AAAA":
            print("Company 1")
            return generate_report_AAA(request, project_id, sheet_key)

        elif aCompany.company.nameCompanies == "BBBB":
            print("Company 2")
            return generate_report_BBB(request, project_id, sheet_key)

        else:
            return HttpResponse("Invalid company ID", status=400)

    except UserCompany.DoesNotExist:
        return HttpResponse("User does not belong to a company", status=403)

    except APP_Project.DoesNotExist:
        return HttpResponse("Project not found", status=404)




def generate_report_AAA(request, project_id, sheet_key):
    
    def add_table(doc, data, title=None):
        """Creates a table and applies a background color to the header."""
        if title:
            doc.add_heading(title, level=3)

        table = doc.add_table(rows=len(data), cols=2)
        table.style = "Table Grid"

        for i, row in enumerate(data):
            for j, text in enumerate(row):
                cell = table.cell(i, j)
                cell.text = text

                # Apply background color only to the header row (first row)
                if i == 0:
                    shading_elm = OxmlElement("w:shd")
                    shading_elm.set(ns.qn("w:fill"), "FFA500")  # Orange color                    
                    #shading_elm.set(ns.qn("w:fill"), "ADD8E6")  # Blue color
                        
                    cell._tc.get_or_add_tcPr().append(shading_elm)
                    
            """Generates a Word report for a given project."""
    
    
    
    def add_header_footer(doc):
        """Adds header and footer with page numbers in the format 'Page X of Y'."""
        section = doc.sections[0]
    
        # Header
        header = section.header
        header_para = header.paragraphs[0] if header.paragraphs else header.add_paragraph()
        # header_para.add_run("Company Name\n")
        # header_para.add_run("Project Name\n")
        # header_para.add_run("Date: " + datetime.now().strftime('%Y-%m-%d %H:%M:%S') + "\n")
        header_para.alignment = WD_PARAGRAPH_ALIGNMENT.CENTER
    
        # Adding logo
        run_logo = header_para.add_run()  # Corrected reference to header paragraph
        
        try:
            run_logo.add_picture("static/aLogo/LogoAAA.PNG", width=Inches(7.0))  # Adjust width as needed
        except Exception as e:
            print(f"Error adding logo: {e}")

        # Footer
        footer = section.footer
        footer_para = footer.paragraphs[0] if footer.paragraphs else footer.add_paragraph()
        footer_para.alignment = WD_PARAGRAPH_ALIGNMENT.CENTER
    
        # Add "Page X of Y" format
        run = footer_para.add_run("Page ")
    
        # PAGE field (Current Page Number)
        fldChar1 = OxmlElement("w:fldChar")
        fldChar1.set(ns.qn("w:fldCharType"), "begin")
    
        instrText1 = OxmlElement("w:instrText")
        instrText1.set(ns.qn("xml:space"), "preserve")
        instrText1.text = "PAGE"
    
        fldChar2 = OxmlElement("w:fldChar")
        fldChar2.set(ns.qn("w:fldCharType"), "end")
    
        run._r.append(fldChar1)
        run._r.append(instrText1)
        run._r.append(fldChar2)
    
        run.add_text(" of ")
    
        # NUMPAGES field (Total Number of Pages)
        fldChar3 = OxmlElement("w:fldChar")
        fldChar3.set(ns.qn("w:fldCharType"), "begin")
    
        instrText2 = OxmlElement("w:instrText")
        instrText2.set(ns.qn("xml:space"), "preserve")
        instrText2.text = "NUMPAGES"
    
        fldChar4 = OxmlElement("w:fldChar")
        fldChar4.set(ns.qn("w:fldCharType"), "end")
    
        run._r.append(fldChar3)
        run._r.append(instrText2)
        run._r.append(fldChar4)
    
    
    def add_colored_heading(doc, text, level, color):
        """Adds a heading with color."""
        heading = doc.add_paragraph()
        run = heading.add_run(text)
        run.bold = True
        run.font.size = Pt(14) if level == 1 else Pt(12)
        run.font.color.rgb = color
        heading.style = f"Heading {level}"
    
    
    
    try:
        
        ###LOG
        aLogEntry.objects.create(
                user=request.user,
                message=f"at {now()} {request.user} accessed Load  "
            )
        print(f"at {now()} {User} accessed Download Report")
        ###LOG

        # Get the company of the logged-in user    
        user_company = None
        if request.user.is_authenticated:
            try:
                user_company = UserCompany.objects.get(user=request.user).company
            except UserCompany.DoesNotExist:
                user_company = None

        print(user_company)

        #Define Retrieve values from AddMachine model
        try:
            machine_config = AddMachine.objects.get(keyValue=sheet_key, company=user_company)
            form_type = machine_config.nameFormCalcXX
            aMachineName = machine_config.nameMachine
        except AddMachine.DoesNotExist:
            form_type = "None"
            aMachineName = "None"

        # Optional: Handle cases where the sheet_key is invalid
        if form_type is None:
            print(f"Warning: Unknown sheet_key '{sheet_key}'")

        aCompany = UserCompany.objects.get(user=request.user)
        project = APP_Project.objects.get(id=project_id)
        form1 = FormCalculationSheet(form_type=form_type)
        
        
        print(aCompany.id)
        print(project.id)
    
        print("Company 1")
    
    
        # Create a Word document
        doc = Document()

        # Add header and footer with page numbers
        add_header_footer(doc)

        # Add project title
        doc.add_heading(f'Project Report: {project.name}', level=1)

        # Add project details
        doc.add_heading("Project Details", level=2)     

        doc.add_paragraph("\n")
        doc.add_paragraph("Name: " + project.name)
        doc.add_paragraph("Client Name: " + project.client_name)
        doc.add_paragraph("Capacity: " + project.capacity)
        doc.add_paragraph("\n")
        
        doc.add_page_break()     
        doc.add_paragraph("\n")


        # Extract form data
        Input_data = [
            (request.POST.get("oSec01Field01", "N/A"), request.POST.get("oSec01Field02", "N/A")),
            (request.POST.get("oSec01Field03", "N/A"), request.POST.get("oSec01Field04", "N/A")),
            (request.POST.get("oSec01Field05", "N/A"), request.POST.get("oSec01Field06", "N/A")),
            (request.POST.get("oSec01Field07", "N/A"), request.POST.get("oSec01Field08", "N/A")),
            (request.POST.get("oSec01Field09", "N/A"), request.POST.get("oSec01Field10", "N/A")),
            (request.POST.get("oSec01Field11", "N/A"), request.POST.get("oSec01Field12", "N/A")),
            (request.POST.get("oSec01Field13", "N/A"), request.POST.get("oSec01Field14", "N/A")),
            (request.POST.get("oSec01Field15", "N/A"), request.POST.get("oSec01Field16", "N/A")),
            (request.POST.get("oSec01Field17", "N/A"), request.POST.get("oSec01Field18", "N/A")),
            (request.POST.get("oSec01Field19", "N/A"), request.POST.get("oSec01Field20", "N/A")),
            (request.POST.get("oSec01Field21", "N/A"), request.POST.get("oSec01Field22", "N/A")),
            (request.POST.get("oSec01Field23", "N/A"), request.POST.get("oSec01Field24", "N/A")),
            (request.POST.get("oSec01Field25", "N/A"), request.POST.get("oSec01Field26", "N/A")),
            (request.POST.get("oSec01Field27", "N/A"), request.POST.get("oSec01Field28", "N/A")),
            (request.POST.get("oSec01Field29", "N/A"), request.POST.get("oSec01Field30", "N/A")),
        ]
        Output_data = [
            (request.POST.get("oSec02Field01", "N/A"), request.POST.get("oSec02Field02", "N/A")),
            (request.POST.get("oSec02Field03", "N/A"), request.POST.get("oSec02Field04", "N/A")),
            (request.POST.get("oSec02Field05", "N/A"), request.POST.get("oSec02Field06", "N/A")),
            (request.POST.get("oSec02Field07", "N/A"), request.POST.get("oSec02Field08", "N/A")),
            (request.POST.get("oSec02Field09", "N/A"), request.POST.get("oSec02Field10", "N/A")),
            (request.POST.get("oSec02Field11", "N/A"), request.POST.get("oSec02Field12", "N/A")),
            (request.POST.get("oSec02Field13", "N/A"), request.POST.get("oSec02Field14", "N/A")),
            (request.POST.get("oSec02Field15", "N/A"), request.POST.get("oSec02Field16", "N/A")),
            (request.POST.get("oSec02Field17", "N/A"), request.POST.get("oSec02Field18", "N/A")),
            (request.POST.get("oSec02Field19", "N/A"), request.POST.get("oSec02Field20", "N/A")),
            (request.POST.get("oSec02Field21", "N/A"), request.POST.get("oSec02Field22", "N/A")),
            (request.POST.get("oSec02Field23", "N/A"), request.POST.get("oSec02Field24", "N/A")),
            (request.POST.get("oSec02Field25", "N/A"), request.POST.get("oSec02Field26", "N/A")),
            (request.POST.get("oSec02Field27", "N/A"), request.POST.get("oSec02Field28", "N/A")),
            (request.POST.get("oSec02Field29", "N/A"), request.POST.get("oSec02Field30", "N/A")),
        ]
        

        # Add machine title with font size 14 and numbering
        machine_title = doc.add_paragraph(f" {aMachineName}", style="Heading3")
        machine_title.runs[0].font.size = Pt(14)

        input_section_data = [("Field", "Value")]
        for input_key, input_value in Input_data:
            input_key = input_key.strip() if input_key else ""
            input_value = input_value.strip() if input_value else ""
            if input_key and input_value and input_key.lower() != "oooo" and input_key.lower() != "" and input_key.lower() != "n/a" and input_value.lower() != "oooo" and input_value.lower() != "" and input_value.lower() != "n/a":
                input_section_data.append((input_key, input_value))
        if len(input_section_data) > 1:  # If the section has valid data, create a table
            doc.add_paragraph(f"Input", style="Heading3")  # Only one title now
            add_table(doc, input_section_data)  # Removed redundant title

        output_section_data = [("Field", "Value")]
        for output_key, output_value in Output_data:
            output_key = output_key.strip() if output_key else ""
            output_value = output_value.strip() if output_value else ""
            if output_key and output_value and output_key.lower() != "oooo" and output_key.lower() != "" and output_key.lower() != "n/a" and output_value.lower() != "oooo" and output_value.lower() != "" and output_value.lower() != "n/a":
                output_section_data.append((output_key, output_value))
        if len(output_section_data) > 1:  # If the section has valid data, create a table
            doc.add_paragraph(f"Output", style="Heading3")  # Only one title now
            add_table(doc, output_section_data)  # Removed redundant title

        doc.add_page_break() 
        
        # Save the document to a response
        response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.wordprocessingml.document')
        response['Content-Disposition'] = f'attachment; filename={project.name}_report.docx'
        doc.save(response)
        return response

    except APP_Project.DoesNotExist:
        return HttpResponse("Project not found", status=404)





def generate_report_BBB(request, project_id, sheet_key):
    
    def add_table(doc, data, title=None):
        """Creates a borderless table and applies a background color to the header."""
        if title:
            doc.add_heading(title, level=3)

        table = doc.add_table(rows=len(data), cols=2)

        # Remove all table borders manually
        tbl = table._tbl  # Get the table's XML element
        tblPr = tbl.find(ns.qn("w:tblPr"))  # Find existing table properties

        if tblPr is None:
            tblPr = OxmlElement("w:tblPr")  # Create table properties if missing
            tbl.insert(0, tblPr)  # Insert as the first child of <w:tbl>

        tblBorders = OxmlElement("w:tblBorders")  # Create <w:tblBorders>
        for border_name in ["top", "left", "bottom", "right", "insideH", "insideV"]:
            border = OxmlElement(f"w:{border_name}")
            border.set(ns.qn("w:val"), "nil")  # Remove the border
            tblBorders.append(border)

        tblPr.append(tblBorders)  # Append border settings to the table properties

        for i, row in enumerate(data):
            for j, text in enumerate(row):
                cell = table.cell(i, j)
                cell.text = text

                # Apply background color only to the header row (first row)
                if i == 0:
                    shading_elm = OxmlElement("w:shd")
                    shading_elm.set(ns.qn("w:val"), "clear")  # Set shading value
                    shading_elm.set(ns.qn("w:fill"), "ADD8E6")  # Light blue color
                    cell._tc.get_or_add_tcPr().append(shading_elm)
   
    
    
    def add_header_footer(doc):
        """Adds header and footer with page numbers in the format 'Page X of Y'."""
        section = doc.sections[0]
    
        # Header
        header = section.header
        header_para = header.paragraphs[0] if header.paragraphs else header.add_paragraph()
        # header_para.add_run("Company Name\n")
        # header_para.add_run("Project Name\n")
        # header_para.add_run("Date: " + datetime.now().strftime('%Y-%m-%d %H:%M:%S') + "\n")
        header_para.alignment = WD_PARAGRAPH_ALIGNMENT.CENTER
    
        # Adding logo
        run_logo = header_para.add_run()  # Corrected reference to header paragraph
        try:
            run_logo.add_picture("static/aLogo/LogoBBB.PNG", width=Inches(7.0))  # Adjust width as needed
        except Exception as e:
            print(f"Error adding logo: {e}")

        
    
        # Footer
        footer = section.footer
        footer_para = footer.paragraphs[0] if footer.paragraphs else footer.add_paragraph()
        footer_para.alignment = WD_PARAGRAPH_ALIGNMENT.CENTER
    
        # Add "Page X of Y" format
        run = footer_para.add_run("Page ")
    
        # PAGE field (Current Page Number)
        fldChar1 = OxmlElement("w:fldChar")
        fldChar1.set(ns.qn("w:fldCharType"), "begin")
    
        instrText1 = OxmlElement("w:instrText")
        instrText1.set(ns.qn("xml:space"), "preserve")
        instrText1.text = "PAGE"
    
        fldChar2 = OxmlElement("w:fldChar")
        fldChar2.set(ns.qn("w:fldCharType"), "end")
    
        run._r.append(fldChar1)
        run._r.append(instrText1)
        run._r.append(fldChar2)
    
        run.add_text(" of ")
    
        # NUMPAGES field (Total Number of Pages)
        fldChar3 = OxmlElement("w:fldChar")
        fldChar3.set(ns.qn("w:fldCharType"), "begin")
    
        instrText2 = OxmlElement("w:instrText")
        instrText2.set(ns.qn("xml:space"), "preserve")
        instrText2.text = "NUMPAGES"
    
        fldChar4 = OxmlElement("w:fldChar")
        fldChar4.set(ns.qn("w:fldCharType"), "end")
    
        run._r.append(fldChar3)
        run._r.append(instrText2)
        run._r.append(fldChar4)
    
    
    def add_colored_heading(doc, text, level, color):
        """Adds a heading with color."""
        heading = doc.add_paragraph()
        run = heading.add_run(text)
        run.bold = True
        run.font.size = Pt(14) if level == 1 else Pt(12)
        run.font.color.rgb = color
        heading.style = f"Heading {level}"
    
    
    
    try:
        
        ###LOG
        aLogEntry.objects.create(
                user=request.user,
                message=f"at {now()} {request.user} accessed Load  "
            )
        print(f"at {now()} {User} accessed Download Report")
        ###LOG

        # Get the company of the logged-in user    
        user_company = None
        if request.user.is_authenticated:
            try:
                user_company = UserCompany.objects.get(user=request.user).company
            except UserCompany.DoesNotExist:
                user_company = None

        print(user_company)

        #Define Retrieve values from AddMachine model
        try:
            machine_config = AddMachine.objects.get(keyValue=sheet_key, company=user_company)
            form_type = machine_config.nameFormCalcXX
            aMachineName = machine_config.nameMachine
        except AddMachine.DoesNotExist:
            form_type = "None"
            aMachineName = "None"

        # Optional: Handle cases where the sheet_key is invalid
        if form_type is None:
            print(f"Warning: Unknown sheet_key '{sheet_key}'")

        aCompany = UserCompany.objects.get(user=request.user)
        project = APP_Project.objects.get(id=project_id)
        form1 = FormCalculationSheet(form_type=form_type)
        
        
        print(aCompany.id)
        print(project.id)
    
        print("Company 2")
    
    
        # Create a Word document
        doc = Document()

        # Add header and footer with page numbers
        add_header_footer(doc)

        # Add project title
        doc.add_heading(f'Project Report: {project.name}', level=1)

        # Add project details
        doc.add_heading("Project Details", level=2)     

        doc.add_paragraph("\n")
        doc.add_paragraph("Name: " + project.name)
        doc.add_paragraph("Client Name: " + project.client_name)
        doc.add_paragraph("Capacity: " + project.capacity)
        doc.add_paragraph("\n")
        
        doc.add_page_break()     
        doc.add_paragraph("\n")

        # Extract form data
        Input_data = [
            (request.POST.get("oSec01Field01", "N/A"), request.POST.get("oSec01Field02", "N/A")),
            (request.POST.get("oSec01Field03", "N/A"), request.POST.get("oSec01Field04", "N/A")),
            (request.POST.get("oSec01Field05", "N/A"), request.POST.get("oSec01Field06", "N/A")),
            (request.POST.get("oSec01Field07", "N/A"), request.POST.get("oSec01Field08", "N/A")),
            (request.POST.get("oSec01Field09", "N/A"), request.POST.get("oSec01Field10", "N/A")),
            (request.POST.get("oSec01Field11", "N/A"), request.POST.get("oSec01Field12", "N/A")),
            (request.POST.get("oSec01Field13", "N/A"), request.POST.get("oSec01Field14", "N/A")),
            (request.POST.get("oSec01Field15", "N/A"), request.POST.get("oSec01Field16", "N/A")),
            (request.POST.get("oSec01Field17", "N/A"), request.POST.get("oSec01Field18", "N/A")),
            (request.POST.get("oSec01Field19", "N/A"), request.POST.get("oSec01Field20", "N/A")),
            (request.POST.get("oSec01Field21", "N/A"), request.POST.get("oSec01Field22", "N/A")),
            (request.POST.get("oSec01Field23", "N/A"), request.POST.get("oSec01Field24", "N/A")),
            (request.POST.get("oSec01Field25", "N/A"), request.POST.get("oSec01Field26", "N/A")),
            (request.POST.get("oSec01Field27", "N/A"), request.POST.get("oSec01Field28", "N/A")),
            (request.POST.get("oSec01Field29", "N/A"), request.POST.get("oSec01Field30", "N/A")),
        ]
        Output_data = [
            (request.POST.get("oSec02Field01", "N/A"), request.POST.get("oSec02Field02", "N/A")),
            (request.POST.get("oSec02Field03", "N/A"), request.POST.get("oSec02Field04", "N/A")),
            (request.POST.get("oSec02Field05", "N/A"), request.POST.get("oSec02Field06", "N/A")),
            (request.POST.get("oSec02Field07", "N/A"), request.POST.get("oSec02Field08", "N/A")),
            (request.POST.get("oSec02Field09", "N/A"), request.POST.get("oSec02Field10", "N/A")),
            (request.POST.get("oSec02Field11", "N/A"), request.POST.get("oSec02Field12", "N/A")),
            (request.POST.get("oSec02Field13", "N/A"), request.POST.get("oSec02Field14", "N/A")),
            (request.POST.get("oSec02Field15", "N/A"), request.POST.get("oSec02Field16", "N/A")),
            (request.POST.get("oSec02Field17", "N/A"), request.POST.get("oSec02Field18", "N/A")),
            (request.POST.get("oSec02Field19", "N/A"), request.POST.get("oSec02Field20", "N/A")),
            (request.POST.get("oSec02Field21", "N/A"), request.POST.get("oSec02Field22", "N/A")),
            (request.POST.get("oSec02Field23", "N/A"), request.POST.get("oSec02Field24", "N/A")),
            (request.POST.get("oSec02Field25", "N/A"), request.POST.get("oSec02Field26", "N/A")),
            (request.POST.get("oSec02Field27", "N/A"), request.POST.get("oSec02Field28", "N/A")),
            (request.POST.get("oSec02Field29", "N/A"), request.POST.get("oSec02Field30", "N/A")),
        ]


        # Add machine title with font size 14 and numbering
        machine_title = doc.add_paragraph(f" {aMachineName}", style="Heading3")
        machine_title.runs[0].font.size = Pt(14)

        input_section_data = [("Field", "Value")]
        for input_key, input_value in Input_data:
            input_key = input_key.strip() if input_key else ""
            input_value = input_value.strip() if input_value else ""
            if input_key and input_value and input_key.lower() != "oooo" and input_key.lower() != "" and input_key.lower() != "n/a" and input_value.lower() != "oooo" and input_value.lower() != "" and input_value.lower() != "n/a":
                input_section_data.append((input_key, input_value))
        if len(input_section_data) > 1:  # If the section has valid data, create a table
            doc.add_paragraph(f"Input", style="Heading3")  # Only one title now
            add_table(doc, input_section_data)  # Removed redundant title

        output_section_data = [("Field", "Value")]
        for output_key, output_value in Output_data:
            output_key = output_key.strip() if output_key else ""
            output_value = output_value.strip() if output_value else ""
            if output_key and output_value and output_key.lower() != "oooo" and output_key.lower() != "" and output_key.lower() != "n/a" and output_value.lower() != "oooo" and output_value.lower() != "" and output_value.lower() != "n/a":
                output_section_data.append((output_key, output_value))
        if len(output_section_data) > 1:  # If the section has valid data, create a table
            doc.add_paragraph(f"Output", style="Heading3")  # Only one title now
            add_table(doc, output_section_data)  # Removed redundant title


        doc.add_page_break()     

        # Save the document to a response
        response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.wordprocessingml.document')
        response['Content-Disposition'] = f'attachment; filename={project.name}_report.docx'
        doc.save(response)
        return response

    except APP_Project.DoesNotExist:
        return HttpResponse("Project not found", status=404)


def DeleteCalcMachine(request, machine_id):  
    sheet_key = request.POST.get("sheet_key")
    print(sheet_key)
    if sheet_key :
            machineShow = "Yes"

    

    machine = get_object_or_404(modelcalc, id=machine_id)
    aLogEntry.objects.create(
        user=request.user,
        message=f"{request.user} deleted >>> {sheet_key} >>> {machine.project.name}"
    )
    machine.delete()

    

     # Get the company of the logged-in user    
    user_company = None
    if request.user.is_authenticated:
        try:
            user_company = UserCompany.objects.get(user=request.user).company
        except UserCompany.DoesNotExist:
            user_company = None

    print(user_company)

    sheet_keys = AddMachine.objects.exclude(nameFormCalcXX__isnull=True).exclude(nameFormCalcXX__exact="None").filter(company=user_company)

    #Define Retrieve values from AddMachine model
    try:
        machine_config = AddMachine.objects.get(keyValue=sheet_key, company=user_company)
        form_type = machine_config.nameFormCalcXX
        aMachineName = machine_config.nameMachine
    except AddMachine.DoesNotExist:
        form_type = "None"
        aMachineName = "None"
        


    # Optional: Handle cases where the sheet_key is invalid
    if form_type is None:
        print(f"Warning: Unknown sheet_key '{sheet_key}'")


     # Assign company filter only if the user has a company
    if user_company:
        machines = modelcalc.objects.filter(oSec00Field03=sheet_key, company=user_company)
        projects = APP_Project.objects.filter(company=user_company)
    else:
        machines = modelcalc.objects.none()  # Return an empty queryset if no company
        projects = APP_Project.objects.none()  # Return an empty queryset if no company

    print(form_type)


    form = FormCalculationSheet(form_type=form_type)
    
    print(f"Initial value for oSec01Field02: {form.fields['oSec01Field02'].initial}")
    
    # Initialize all section variables
    aSection01Field01Show = "Yes"
    aSection01Field02Show = "Yes"
    aSection01Field03Show = "Yes"
    aSection01Field04Show = "Yes"
    aSection01Field05Show = "Yes"
    aSection01Field06Show = "Yes"
    aSection01Field07Show = "Yes"
    aSection01Field08Show = "Yes"
    aSection01Field09Show = "Yes"
    aSection01Field10Show = "Yes"
    aSection01Field11Show = "Yes"
    aSection01Field12Show = "Yes"
    aSection01Field13Show = "Yes"
    aSection01Field14Show = "Yes"
    aSection01Field15Show = "Yes"
    aSection01Field16Show = "Yes"
    aSection01Field17Show = "Yes"
    aSection01Field18Show = "Yes"
    aSection01Field19Show = "Yes"
    aSection01Field20Show = "Yes"
    aSection01Field21Show = "Yes"
    aSection01Field22Show = "Yes"
    aSection01Field23Show = "Yes"
    aSection01Field24Show = "Yes"
    aSection01Field25Show = "Yes"
    aSection01Field26Show = "Yes"
    aSection01Field27Show = "Yes"
    aSection01Field28Show = "Yes"
    aSection01Field29Show = "Yes"
    aSection01Field30Show = "Yes"
    aSection02Field01Show = "Yes"
    aSection02Field02Show = "Yes"
    aSection02Field03Show = "Yes"
    aSection02Field04Show = "Yes"
    aSection02Field05Show = "Yes"
    aSection02Field06Show = "Yes"
    aSection02Field07Show = "Yes"
    aSection02Field08Show = "Yes"
    aSection02Field09Show = "Yes"
    aSection02Field10Show = "Yes"
    aSection02Field11Show = "Yes"
    aSection02Field12Show = "Yes"
    aSection02Field13Show = "Yes"
    aSection02Field14Show = "Yes"
    aSection02Field15Show = "Yes"
    aSection02Field16Show = "Yes"
    aSection02Field17Show = "Yes"
    aSection02Field18Show = "Yes"
    aSection02Field19Show = "Yes"
    aSection02Field20Show = "Yes"
    aSection02Field21Show = "Yes"
    aSection02Field22Show = "Yes"
    aSection02Field23Show = "Yes"
    aSection02Field24Show = "Yes"
    aSection02Field25Show = "Yes"
    aSection02Field26Show = "Yes"
    aSection02Field27Show = "Yes"
    aSection02Field28Show = "Yes"
    aSection02Field29Show = "Yes"
    aSection02Field30Show = "Yes"
    
    print(form.fields['oSec01Field01'].initial)
    print(form.fields['oSec01Field02'].initial)
    print(form.fields['oSec01Field03'].initial)
    print(form.fields['oSec01Field04'].initial)
    print(form.fields['oSec01Field05'].initial)
    print(form.fields['oSec01Field06'].initial)
    print(form.fields['oSec01Field07'].initial)
    print(form.fields['oSec01Field08'].initial)
    print(form.fields['oSec01Field09'].initial)
    print(form.fields['oSec01Field10'].initial)
    print(form.fields['oSec01Field11'].initial)
    print(form.fields['oSec01Field12'].initial)
    print(form.fields['oSec01Field13'].initial)
    print(form.fields['oSec01Field14'].initial)
    print(form.fields['oSec01Field15'].initial)
    print(form.fields['oSec01Field16'].initial)
    print(form.fields['oSec01Field17'].initial)
    print(form.fields['oSec01Field18'].initial)
    print(form.fields['oSec01Field19'].initial)
    print(form.fields['oSec01Field20'].initial)
    print(form.fields['oSec01Field21'].initial)
    print(form.fields['oSec01Field22'].initial)
    print(form.fields['oSec01Field23'].initial)
    print(form.fields['oSec01Field24'].initial)
    print(form.fields['oSec01Field25'].initial)
    print(form.fields['oSec01Field26'].initial)
    print(form.fields['oSec01Field27'].initial)
    print(form.fields['oSec01Field28'].initial)
    print(form.fields['oSec01Field29'].initial)
    print(form.fields['oSec01Field30'].initial)
    print(form.fields['oSec02Field01'].initial)
    print(form.fields['oSec02Field02'].initial)
    print(form.fields['oSec02Field03'].initial)
    print(form.fields['oSec02Field04'].initial)
    print(form.fields['oSec02Field05'].initial)
    print(form.fields['oSec02Field06'].initial)
    print(form.fields['oSec02Field07'].initial)
    print(form.fields['oSec02Field08'].initial)
    print(form.fields['oSec02Field09'].initial)
    print(form.fields['oSec02Field10'].initial)
    print(form.fields['oSec02Field11'].initial)
    print(form.fields['oSec02Field12'].initial)
    print(form.fields['oSec02Field13'].initial)
    print(form.fields['oSec02Field14'].initial)
    print(form.fields['oSec02Field15'].initial)
    print(form.fields['oSec02Field16'].initial)
    print(form.fields['oSec02Field17'].initial)
    print(form.fields['oSec02Field18'].initial)
    print(form.fields['oSec02Field19'].initial)
    print(form.fields['oSec02Field20'].initial)
    print(form.fields['oSec02Field21'].initial)
    print(form.fields['oSec02Field22'].initial)
    print(form.fields['oSec02Field23'].initial)
    print(form.fields['oSec02Field24'].initial)
    print(form.fields['oSec02Field25'].initial)
    print(form.fields['oSec02Field26'].initial)
    print(form.fields['oSec02Field27'].initial)
    print(form.fields['oSec02Field28'].initial)
    print(form.fields['oSec02Field29'].initial)
    print(form.fields['oSec02Field30'].initial)

    # Apply conditions to modify the values
    if form.fields['oSec01Field01'].initial in ["oooo", None , ""]:
        aSection01Field01Show = "Hide"
    if form.fields['oSec01Field02'].initial in ["oooo", None , ""]:
        aSection01Field02Show = "Hide"
    if form.fields['oSec01Field03'].initial in ["oooo", None , ""]:
        aSection01Field03Show = "Hide"
    if form.fields['oSec01Field04'].initial in ["oooo", None , ""]:
        aSection01Field04Show = "Hide"
    if form.fields['oSec01Field05'].initial in ["oooo", None , ""]:
        aSection01Field05Show = "Hide"
    if form.fields['oSec01Field06'].initial in ["oooo", None , ""]:
        aSection01Field06Show = "Hide"
    if form.fields['oSec01Field07'].initial in ["oooo", None , ""]:
        aSection01Field07Show = "Hide"
    if form.fields['oSec01Field08'].initial in ["oooo", None , ""]:
        aSection01Field08Show = "Hide"
    if form.fields['oSec01Field09'].initial in ["oooo", None , ""]:
        aSection01Field09Show = "Hide"
    if form.fields['oSec01Field10'].initial in ["oooo", None , ""]:
        aSection01Field10Show = "Hide"
    if form.fields['oSec01Field11'].initial in ["oooo", None , ""]:
        aSection01Field11Show = "Hide"
    if form.fields['oSec01Field12'].initial in ["oooo", None , ""]:
        aSection01Field12Show = "Hide"
    if form.fields['oSec01Field13'].initial in ["oooo", None , ""]:
        aSection01Field13Show = "Hide"
    if form.fields['oSec01Field14'].initial in ["oooo", None , ""]:
        aSection01Field14Show = "Hide"
    if form.fields['oSec01Field15'].initial in ["oooo", None , ""]:
        aSection01Field15Show = "Hide"
    if form.fields['oSec01Field16'].initial in ["oooo", None , ""]:
        aSection01Field16Show = "Hide"
    if form.fields['oSec01Field17'].initial in ["oooo", None , ""]:
        aSection01Field17Show = "Hide"
    if form.fields['oSec01Field18'].initial in ["oooo", None , ""]:
        aSection01Field18Show = "Hide"
    if form.fields['oSec01Field19'].initial in ["oooo", None , ""]:
        aSection01Field19Show = "Hide"
    if form.fields['oSec01Field20'].initial in ["oooo", None , ""]:
        aSection01Field20Show = "Hide"
    if form.fields['oSec01Field21'].initial in ["oooo", None , ""]:
        aSection01Field21Show = "Hide"
    if form.fields['oSec01Field22'].initial in ["oooo", None , ""]:
        aSection01Field22Show = "Hide"
    if form.fields['oSec01Field23'].initial in ["oooo", None , ""]:
        aSection01Field23Show = "Hide"
    if form.fields['oSec01Field24'].initial in ["oooo", None , ""]:
        aSection01Field24Show = "Hide"
    if form.fields['oSec01Field25'].initial in ["oooo", None , ""]:
        aSection01Field25Show = "Hide"
    if form.fields['oSec01Field26'].initial in ["oooo", None , ""]:
        aSection01Field26Show = "Hide"
    if form.fields['oSec01Field27'].initial in ["oooo", None , ""]:
        aSection01Field27Show = "Hide"
    if form.fields['oSec01Field28'].initial in ["oooo", None , ""]:
        aSection01Field28Show = "Hide"
    if form.fields['oSec01Field29'].initial in ["oooo", None , ""]:
        aSection01Field29Show = "Hide"
    if form.fields['oSec01Field30'].initial in ["oooo", None , ""]:
        aSection01Field30Show = "Hide"

    if form.fields['oSec02Field01'].initial in ["oooo", None , ""]:
        aSection02Field01Show = "Hide"
    if form.fields['oSec02Field02'].initial in ["oooo", None , ""]:
        aSection02Field02Show = "Hide"
    if form.fields['oSec02Field03'].initial in ["oooo", None , ""]:
        aSection02Field03Show = "Hide"
    if form.fields['oSec02Field04'].initial in ["oooo", None , ""]:
        aSection02Field04Show = "Hide"
    if form.fields['oSec02Field05'].initial in ["oooo", None , ""]:
        aSection02Field05Show = "Hide"
    if form.fields['oSec02Field06'].initial in ["oooo", None , ""]:
        aSection02Field06Show = "Hide"
    if form.fields['oSec02Field07'].initial in ["oooo", None , ""]:
        aSection02Field07Show = "Hide"
    if form.fields['oSec02Field08'].initial in ["oooo", None , ""]:
        aSection02Field08Show = "Hide"
    if form.fields['oSec02Field09'].initial in ["oooo", None , ""]:
        aSection02Field09Show = "Hide"
    if form.fields['oSec02Field10'].initial in ["oooo", None , ""]:
        aSection02Field10Show = "Hide"
    if form.fields['oSec02Field11'].initial in ["oooo", None , ""]:
        aSection02Field11Show = "Hide"
    if form.fields['oSec02Field12'].initial in ["oooo", None , ""]:
        aSection02Field12Show = "Hide"
    if form.fields['oSec02Field13'].initial in ["oooo", None , ""]:
        aSection02Field13Show = "Hide"
    if form.fields['oSec01Field14'].initial in ["oooo", None , ""]:
        aSection02Field14Show = "Hide"
    if form.fields['oSec02Field15'].initial in ["oooo", None , ""]:
        aSection02Field15Show = "Hide"
    if form.fields['oSec02Field16'].initial in ["oooo", None , ""]:
        aSection02Field16Show = "Hide"
    if form.fields['oSec02Field17'].initial in ["oooo", None , ""]:
        aSection02Field17Show = "Hide"
    if form.fields['oSec02Field18'].initial in ["oooo", None , ""]:
        aSection02Field18Show = "Hide"
    if form.fields['oSec02Field19'].initial in ["oooo", None , ""]:
        aSection02Field19Show = "Hide"
    if form.fields['oSec02Field20'].initial in ["oooo", None , ""]:
        aSection02Field20Show = "Hide"
    if form.fields['oSec02Field21'].initial in ["oooo", None , ""]:
        aSection02Field21Show = "Hide"
    if form.fields['oSec02Field22'].initial in ["oooo", None , ""]:
        aSection02Field22Show = "Hide"
    if form.fields['oSec02Field23'].initial in ["oooo", None , ""]:
        aSection02Field23Show = "Hide"
    if form.fields['oSec01Field24'].initial in ["oooo", None , ""]:
        aSection02Field24Show = "Hide"
    if form.fields['oSec02Field25'].initial in ["oooo", None , ""]:
        aSection02Field25Show = "Hide"
    if form.fields['oSec02Field26'].initial in ["oooo", None , ""]:
        aSection02Field26Show = "Hide"
    if form.fields['oSec02Field27'].initial in ["oooo", None , ""]:
        aSection02Field27Show = "Hide"
    if form.fields['oSec02Field28'].initial in ["oooo", None , ""]:
        aSection02Field28Show = "Hide"
    if form.fields['oSec02Field29'].initial in ["oooo", None , ""]:
        aSection02Field29Show = "Hide"
    if form.fields['oSec02Field30'].initial in ["oooo", None , ""]:
        aSection02Field30Show = "Hide"
    
    print(aSection01Field01Show)
    print(aSection01Field02Show)
    print(aSection01Field03Show)
    print(aSection01Field04Show)
    print(aSection01Field05Show)
    print(aSection01Field06Show)
    print(aSection01Field07Show)
    print(aSection01Field08Show)
    print(aSection01Field09Show)
    print(aSection01Field10Show)
    print(aSection01Field11Show)
    print(aSection01Field12Show)
    print(aSection01Field13Show)
    print(aSection01Field14Show)
    print(aSection01Field15Show)
    print(aSection01Field16Show)
    print(aSection01Field17Show)
    print(aSection01Field18Show)
    print(aSection01Field19Show)
    print(aSection01Field20Show)
    print(aSection01Field21Show)
    print(aSection01Field22Show)
    print(aSection01Field23Show)
    print(aSection01Field24Show)
    print(aSection01Field25Show)
    print(aSection01Field26Show)
    print(aSection01Field27Show)
    print(aSection01Field28Show)
    print(aSection01Field29Show)
    print(aSection01Field30Show)
    print(aSection02Field01Show)
    print(aSection02Field02Show)
    print(aSection02Field03Show)
    print(aSection02Field04Show)
    print(aSection02Field05Show)
    print(aSection02Field06Show)
    print(aSection02Field07Show)
    print(aSection02Field08Show)
    print(aSection02Field09Show)
    print(aSection02Field10Show)
    print(aSection02Field11Show)
    print(aSection02Field12Show)
    print(aSection02Field13Show)
    print(aSection02Field14Show)
    print(aSection02Field15Show)
    print(aSection02Field16Show)
    print(aSection02Field17Show)
    print(aSection02Field18Show)
    print(aSection02Field19Show)
    print(aSection02Field20Show)
    print(aSection02Field21Show)
    print(aSection02Field22Show)
    print(aSection02Field23Show)
    print(aSection02Field24Show)
    print(aSection02Field25Show)
    print(aSection02Field26Show)
    print(aSection02Field27Show)
    print(aSection02Field28Show)
    print(aSection02Field29Show)
    print(aSection02Field30Show)
    

    return render(request, "PageCalculationSheet.html", {
    "form": form,
    "machines": machines,
    "projects": projects,  
    "aMachineName": aMachineName, 
    "user_company": user_company, 
    "sheet_key": sheet_key,
    "sheet_keys": sheet_keys,
    "machineShow": machineShow,
    "aSection01Field01Show": aSection01Field01Show,
    "aSection01Field02Show": aSection01Field02Show,
    "aSection01Field03Show": aSection01Field03Show,
    "aSection01Field04Show": aSection01Field04Show,
    "aSection01Field05Show": aSection01Field05Show,
    "aSection01Field06Show": aSection01Field06Show,
    "aSection01Field07Show": aSection01Field07Show,
    "aSection01Field08Show": aSection01Field08Show,
    "aSection01Field09Show": aSection01Field09Show,
    "aSection01Field10Show": aSection01Field10Show,
    "aSection01Field11Show": aSection01Field11Show,
    "aSection01Field12Show": aSection01Field12Show,
    "aSection01Field13Show": aSection01Field13Show,
    "aSection01Field14Show": aSection01Field14Show,
    "aSection01Field15Show": aSection01Field15Show,
    "aSection01Field16Show": aSection01Field16Show,
    "aSection01Field17Show": aSection01Field17Show,
    "aSection01Field18Show": aSection01Field18Show,
    "aSection01Field19Show": aSection01Field19Show,
    "aSection01Field20Show": aSection01Field20Show,
    "aSection01Field21Show": aSection01Field21Show,
    "aSection01Field22Show": aSection01Field22Show,
    "aSection01Field23Show": aSection01Field23Show,
    "aSection01Field24Show": aSection01Field24Show,
    "aSection01Field25Show": aSection01Field25Show,
    "aSection01Field26Show": aSection01Field26Show,
    "aSection01Field27Show": aSection01Field27Show,
    "aSection01Field28Show": aSection01Field28Show,
    "aSection01Field29Show": aSection01Field29Show,
    "aSection01Field30Show": aSection01Field30Show,
    "aSection02Field01Show": aSection02Field01Show,
    "aSection02Field02Show": aSection02Field02Show,
    "aSection02Field03Show": aSection02Field03Show,
    "aSection02Field04Show": aSection02Field04Show,
    "aSection02Field05Show": aSection02Field05Show,
    "aSection02Field06Show": aSection02Field06Show,
    "aSection02Field07Show": aSection02Field07Show,
    "aSection02Field08Show": aSection02Field08Show,
    "aSection02Field09Show": aSection02Field09Show,
    "aSection02Field10Show": aSection02Field10Show,
    "aSection02Field11Show": aSection02Field11Show,
    "aSection02Field12Show": aSection02Field12Show,
    "aSection02Field13Show": aSection02Field13Show,
    "aSection02Field14Show": aSection02Field14Show,
    "aSection02Field15Show": aSection02Field15Show,
    "aSection02Field16Show": aSection02Field16Show,
    "aSection02Field17Show": aSection02Field17Show,
    "aSection02Field18Show": aSection02Field18Show,
    "aSection02Field19Show": aSection02Field19Show,
    "aSection02Field20Show": aSection02Field20Show,
    "aSection02Field21Show": aSection02Field21Show,
    "aSection02Field22Show": aSection02Field22Show,
    "aSection02Field23Show": aSection02Field23Show,
    "aSection02Field24Show": aSection02Field24Show,
    "aSection02Field25Show": aSection02Field25Show,
    "aSection02Field26Show": aSection02Field26Show,
    "aSection02Field27Show": aSection02Field27Show,
    "aSection02Field28Show": aSection02Field28Show,
    "aSection02Field29Show": aSection02Field29Show,
    "aSection02Field30Show": aSection02Field30Show,
    
})


def CalculationSheet_get_data(request, machine_id):
    machine = get_object_or_404(modelcalc, id=machine_id)
    sheet_key = machine.oSec00Field03
    print(sheet_key)

    aLogEntry.objects.create(
        user=request.user,
        message=f"{request.user} Get data of >>> {sheet_key} >>> {machine.project.name}"
    )
    
    
    data = {
        "project": machine.project.name if machine.project else "No Project",
        "oSec01Field01": machine.oSec01Field01,
        "oSec01Field02": machine.oSec01Field02,
        "oSec01Field03": machine.oSec01Field03,
        "oSec01Field04": machine.oSec01Field04,
        "oSec01Field05": machine.oSec01Field05,
        "oSec01Field06": machine.oSec01Field06,
        "oSec01Field07": machine.oSec01Field07,
        "oSec01Field08": machine.oSec01Field08,
        "oSec01Field09": machine.oSec01Field09,
        "oSec01Field10": machine.oSec01Field10,        
        "oSec01Field11": machine.oSec01Field11,
        "oSec01Field12": machine.oSec01Field12,
        "oSec01Field13": machine.oSec01Field13,
        "oSec01Field14": machine.oSec01Field14,
        "oSec01Field15": machine.oSec01Field15,
        "oSec01Field16": machine.oSec01Field16,
        "oSec01Field17": machine.oSec01Field17,
        "oSec01Field18": machine.oSec01Field18,
        "oSec01Field19": machine.oSec01Field19,
        "oSec01Field20": machine.oSec01Field20,
        "oSec01Field21": machine.oSec01Field21,
        "oSec01Field22": machine.oSec01Field22,
        "oSec01Field23": machine.oSec01Field23,
        "oSec01Field24": machine.oSec01Field24,
        "oSec01Field25": machine.oSec01Field25,
        "oSec01Field26": machine.oSec01Field26,
        "oSec01Field27": machine.oSec01Field27,
        "oSec01Field28": machine.oSec01Field28,
        "oSec01Field29": machine.oSec01Field29,
        "oSec01Field30": machine.oSec01Field30,
        
        "oSec02Field01": machine.oSec02Field01,
        "oSec02Field02": machine.oSec02Field02,
        "oSec02Field03": machine.oSec02Field03,
        "oSec02Field04": machine.oSec02Field04,
        "oSec02Field05": machine.oSec02Field05,
        "oSec02Field06": machine.oSec02Field06,
        "oSec02Field07": machine.oSec02Field07,
        "oSec02Field08": machine.oSec02Field08,
        "oSec02Field09": machine.oSec02Field09,
        "oSec02Field10": machine.oSec02Field10,        
        "oSec02Field11": machine.oSec02Field11,
        "oSec02Field12": machine.oSec02Field12,
        "oSec02Field13": machine.oSec02Field13,
        "oSec02Field14": machine.oSec02Field14,
        "oSec02Field15": machine.oSec02Field15,
        "oSec02Field16": machine.oSec02Field16,
        "oSec02Field17": machine.oSec02Field17,
        "oSec02Field18": machine.oSec02Field18,
        "oSec02Field19": machine.oSec02Field19,
        "oSec02Field20": machine.oSec02Field20,
        "oSec02Field21": machine.oSec02Field21,
        "oSec02Field22": machine.oSec02Field22,
        "oSec02Field23": machine.oSec02Field23,
        "oSec02Field24": machine.oSec02Field24,
        "oSec02Field25": machine.oSec02Field25,
        "oSec02Field26": machine.oSec02Field26,
        "oSec02Field27": machine.oSec02Field27,
        "oSec02Field28": machine.oSec02Field28,
        "oSec02Field29": machine.oSec02Field29,
        "oSec02Field30": machine.oSec02Field30,
        
    }

    return JsonResponse(data)




def generate_saved_report(request, machine_id):
    try:
        #pdb.set_trace()
        # Log the action
        aLogEntry.objects.create(user=request.user, message=f"at {now()} {request.user} accessed Word Report")
        
        #pdb.set_trace()
        # Get the user’s company and project
        aCompany = UserCompany.objects.get(user=request.user)



        #pdb.set_trace()
        # Determine the company and generate the corresponding report
        if aCompany.company.nameCompanies == "AAAA":
            print("Company 1")
            return generate_saved_report_AAA(request, machine_id)

        elif aCompany.company.nameCompanies == "BBBB":
            print("Company 2")
            return generate_saved_report_BBB(request, machine_id)

        else:
            return HttpResponse("Invalid company ID", status=400)

    except UserCompany.DoesNotExist:
        return HttpResponse("User does not belong to a company", status=403)

    except APP_Project.DoesNotExist:
        return HttpResponse("Project not found", status=404)




def generate_saved_report_AAA(request, machine_id):
    
    def add_table(doc, data, title=None):
        """Creates a table and applies a background color to the header."""
        if title:
            doc.add_heading(title, level=3)

        table = doc.add_table(rows=len(data), cols=2)
        table.style = "Table Grid"

        for i, row in enumerate(data):
            for j, text in enumerate(row):
                cell = table.cell(i, j)
                cell.text = text

                # Apply background color only to the header row (first row)
                if i == 0:
                    shading_elm = OxmlElement("w:shd")
                    shading_elm.set(ns.qn("w:fill"), "FFA500")  # Orange color                    
                    #shading_elm.set(ns.qn("w:fill"), "ADD8E6")  # Blue color
                        
                    cell._tc.get_or_add_tcPr().append(shading_elm)
                    
            """Generates a Word report for a given project."""
    
    
    
    def add_header_footer(doc):
        """Adds header and footer with page numbers in the format 'Page X of Y'."""
        section = doc.sections[0]
    
        # Header
        header = section.header
        header_para = header.paragraphs[0] if header.paragraphs else header.add_paragraph()
        # header_para.add_run("Company Name\n")
        # header_para.add_run("Project Name\n")
        # header_para.add_run("Date: " + datetime.now().strftime('%Y-%m-%d %H:%M:%S') + "\n")
        header_para.alignment = WD_PARAGRAPH_ALIGNMENT.CENTER
    
        # Adding logo
        run_logo = header_para.add_run()  # Corrected reference to header paragraph
        
        try:
            run_logo.add_picture("static/aLogo/LogoAAA.PNG", width=Inches(7.0))  # Adjust width as needed
        except Exception as e:
            print(f"Error adding logo: {e}")

        # Footer
        footer = section.footer
        footer_para = footer.paragraphs[0] if footer.paragraphs else footer.add_paragraph()
        footer_para.alignment = WD_PARAGRAPH_ALIGNMENT.CENTER
    
        # Add "Page X of Y" format
        run = footer_para.add_run("Page ")
    
        # PAGE field (Current Page Number)
        fldChar1 = OxmlElement("w:fldChar")
        fldChar1.set(ns.qn("w:fldCharType"), "begin")
    
        instrText1 = OxmlElement("w:instrText")
        instrText1.set(ns.qn("xml:space"), "preserve")
        instrText1.text = "PAGE"
    
        fldChar2 = OxmlElement("w:fldChar")
        fldChar2.set(ns.qn("w:fldCharType"), "end")
    
        run._r.append(fldChar1)
        run._r.append(instrText1)
        run._r.append(fldChar2)
    
        run.add_text(" of ")
    
        # NUMPAGES field (Total Number of Pages)
        fldChar3 = OxmlElement("w:fldChar")
        fldChar3.set(ns.qn("w:fldCharType"), "begin")
    
        instrText2 = OxmlElement("w:instrText")
        instrText2.set(ns.qn("xml:space"), "preserve")
        instrText2.text = "NUMPAGES"
    
        fldChar4 = OxmlElement("w:fldChar")
        fldChar4.set(ns.qn("w:fldCharType"), "end")
    
        run._r.append(fldChar3)
        run._r.append(instrText2)
        run._r.append(fldChar4)
    
    
    def add_colored_heading(doc, text, level, color):
        """Adds a heading with color."""
        heading = doc.add_paragraph()
        run = heading.add_run(text)
        run.bold = True
        run.font.size = Pt(14) if level == 1 else Pt(12)
        run.font.color.rgb = color
        heading.style = f"Heading {level}"
    
    
    
    try:
        
        ###LOG
        aLogEntry.objects.create(
                user=request.user,
                message=f"at {now()} {request.user} accessed Load  "
            )
        print(f"at {now()} {User} accessed Download Report")
        ###LOG

        # Get the company of the logged-in user    
        user_company = None
        if request.user.is_authenticated:
            try:
                user_company = UserCompany.objects.get(user=request.user).company
            except UserCompany.DoesNotExist:
                user_company = None

        print(user_company)

        aCompany = UserCompany.objects.get(user=request.user)
        machine = get_object_or_404(modelcalc, id=machine_id)
        project = APP_Project.objects.get(name=machine.project.name)
        
        print(aCompany.id)
        print(project.id)
    
        print("Company 1")

        sheet_key = machine.oSec00Field03

        #Define Retrieve values from AddMachine model
        try:
            machine_config = AddMachine.objects.get(keyValue=sheet_key, company=user_company)
            form_type = machine_config.nameFormCalcXX
            aMachineName = machine_config.nameMachine
        except AddMachine.DoesNotExist:
            form_type = "None"
            aMachineName = "None"

        # Optional: Handle cases where the sheet_key is invalid
        if form_type is None:
            print(f"Warning: Unknown sheet_key '{sheet_key}'")
    
    
        # Create a Word document
        doc = Document()

        # Add header and footer with page numbers
        add_header_footer(doc)

        # Add project title
        doc.add_heading(f'Project Report: {project.name}', level=1)

        # Add project details
        doc.add_heading("Project Details", level=2)     

        doc.add_paragraph("\n")
        doc.add_paragraph("Name: " + project.name)
        doc.add_paragraph("Client Name: " + project.client_name)
        doc.add_paragraph("Capacity: " + project.capacity)
        doc.add_paragraph("\n")
        
        doc.add_page_break()     
        doc.add_paragraph("\n")


        # Extract form data
        Input_data = [
            (machine.oSec01Field01, machine.oSec01Field02),
            (machine.oSec01Field03, machine.oSec01Field04),
            (machine.oSec01Field05, machine.oSec01Field06),
            (machine.oSec01Field07, machine.oSec01Field08),
            (machine.oSec01Field09, machine.oSec01Field10),
            (machine.oSec01Field11, machine.oSec01Field12),
            (machine.oSec01Field13, machine.oSec01Field14),
            (machine.oSec01Field15, machine.oSec01Field16),
            (machine.oSec01Field17, machine.oSec01Field18),
            (machine.oSec01Field19, machine.oSec01Field20),
            (machine.oSec01Field21, machine.oSec01Field22),
            (machine.oSec01Field23, machine.oSec01Field24),
            (machine.oSec01Field25, machine.oSec01Field26),
            (machine.oSec01Field27, machine.oSec01Field28),
            (machine.oSec01Field29, machine.oSec01Field30),
        ]
        Output_data = [
            (machine.oSec02Field01, machine.oSec02Field02),
            (machine.oSec02Field03, machine.oSec02Field04),
            (machine.oSec02Field05, machine.oSec02Field06),
            (machine.oSec02Field07, machine.oSec02Field08),
            (machine.oSec02Field09, machine.oSec02Field10),
            (machine.oSec02Field11, machine.oSec02Field12),
            (machine.oSec02Field13, machine.oSec02Field14),
            (machine.oSec02Field15, machine.oSec02Field16),
            (machine.oSec02Field17, machine.oSec02Field18),
            (machine.oSec02Field19, machine.oSec02Field20),
            (machine.oSec02Field21, machine.oSec02Field22),
            (machine.oSec02Field23, machine.oSec02Field24),
            (machine.oSec02Field25, machine.oSec02Field26),
            (machine.oSec02Field27, machine.oSec02Field28),
            (machine.oSec02Field29, machine.oSec02Field30),
        ]
        

        # Add machine title with font size 14 and numbering
        machine_title = doc.add_paragraph(f" {aMachineName}", style="Heading3")
        machine_title.runs[0].font.size = Pt(14)

        input_section_data = [("Field", "Value")]
        for input_key, input_value in Input_data:
            input_key = input_key.strip() if input_key else ""
            input_value = input_value.strip() if input_value else ""
            if input_key and input_value and input_key.lower() != "oooo" and input_key.lower() != "" and input_key.lower() != "n/a" and input_value.lower() != "oooo" and input_value.lower() != "" and input_value.lower() != "n/a":
                input_section_data.append((input_key, input_value))
        if len(input_section_data) > 1:  # If the section has valid data, create a table
            doc.add_paragraph(f"Input", style="Heading3")  # Only one title now
            add_table(doc, input_section_data)  # Removed redundant title

        output_section_data = [("Field", "Value")]
        for output_key, output_value in Output_data:
            output_key = output_key.strip() if output_key else ""
            output_value = output_value.strip() if output_value else ""
            if output_key and output_value and output_key.lower() != "oooo" and output_key.lower() != "" and output_key.lower() != "n/a" and output_value.lower() != "oooo" and output_value.lower() != "" and output_value.lower() != "n/a":
                output_section_data.append((output_key, output_value))
        if len(output_section_data) > 1:  # If the section has valid data, create a table
            doc.add_paragraph(f"Output", style="Heading3")  # Only one title now
            add_table(doc, output_section_data)  # Removed redundant title

        doc.add_page_break() 
        
        # Save the document to a response
        response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.wordprocessingml.document')
        response['Content-Disposition'] = f'attachment; filename={project.name}_report.docx'
        doc.save(response)
        return response

    except APP_Project.DoesNotExist:
        return HttpResponse("Project not found", status=404)





def generate_saved_report_BBB(request, machine_id):
    
    def add_table(doc, data, title=None):
        """Creates a borderless table and applies a background color to the header."""
        if title:
            doc.add_heading(title, level=3)

        table = doc.add_table(rows=len(data), cols=2)

        # Remove all table borders manually
        tbl = table._tbl  # Get the table's XML element
        tblPr = tbl.find(ns.qn("w:tblPr"))  # Find existing table properties

        if tblPr is None:
            tblPr = OxmlElement("w:tblPr")  # Create table properties if missing
            tbl.insert(0, tblPr)  # Insert as the first child of <w:tbl>

        tblBorders = OxmlElement("w:tblBorders")  # Create <w:tblBorders>
        for border_name in ["top", "left", "bottom", "right", "insideH", "insideV"]:
            border = OxmlElement(f"w:{border_name}")
            border.set(ns.qn("w:val"), "nil")  # Remove the border
            tblBorders.append(border)

        tblPr.append(tblBorders)  # Append border settings to the table properties

        for i, row in enumerate(data):
            for j, text in enumerate(row):
                cell = table.cell(i, j)
                cell.text = text

                # Apply background color only to the header row (first row)
                if i == 0:
                    shading_elm = OxmlElement("w:shd")
                    shading_elm.set(ns.qn("w:val"), "clear")  # Set shading value
                    shading_elm.set(ns.qn("w:fill"), "ADD8E6")  # Light blue color
                    cell._tc.get_or_add_tcPr().append(shading_elm)
   
    
    
    def add_header_footer(doc):
        """Adds header and footer with page numbers in the format 'Page X of Y'."""
        section = doc.sections[0]
    
        # Header
        header = section.header
        header_para = header.paragraphs[0] if header.paragraphs else header.add_paragraph()
        # header_para.add_run("Company Name\n")
        # header_para.add_run("Project Name\n")
        # header_para.add_run("Date: " + datetime.now().strftime('%Y-%m-%d %H:%M:%S') + "\n")
        header_para.alignment = WD_PARAGRAPH_ALIGNMENT.CENTER
    
        # Adding logo
        run_logo = header_para.add_run()  # Corrected reference to header paragraph
        try:
            run_logo.add_picture("static/aLogo/LogoBBB.PNG", width=Inches(7.0))  # Adjust width as needed
        except Exception as e:
            print(f"Error adding logo: {e}")

        
    
        # Footer
        footer = section.footer
        footer_para = footer.paragraphs[0] if footer.paragraphs else footer.add_paragraph()
        footer_para.alignment = WD_PARAGRAPH_ALIGNMENT.CENTER
    
        # Add "Page X of Y" format
        run = footer_para.add_run("Page ")
    
        # PAGE field (Current Page Number)
        fldChar1 = OxmlElement("w:fldChar")
        fldChar1.set(ns.qn("w:fldCharType"), "begin")
    
        instrText1 = OxmlElement("w:instrText")
        instrText1.set(ns.qn("xml:space"), "preserve")
        instrText1.text = "PAGE"
    
        fldChar2 = OxmlElement("w:fldChar")
        fldChar2.set(ns.qn("w:fldCharType"), "end")
    
        run._r.append(fldChar1)
        run._r.append(instrText1)
        run._r.append(fldChar2)
    
        run.add_text(" of ")
    
        # NUMPAGES field (Total Number of Pages)
        fldChar3 = OxmlElement("w:fldChar")
        fldChar3.set(ns.qn("w:fldCharType"), "begin")
    
        instrText2 = OxmlElement("w:instrText")
        instrText2.set(ns.qn("xml:space"), "preserve")
        instrText2.text = "NUMPAGES"
    
        fldChar4 = OxmlElement("w:fldChar")
        fldChar4.set(ns.qn("w:fldCharType"), "end")
    
        run._r.append(fldChar3)
        run._r.append(instrText2)
        run._r.append(fldChar4)
    
    
    def add_colored_heading(doc, text, level, color):
        """Adds a heading with color."""
        heading = doc.add_paragraph()
        run = heading.add_run(text)
        run.bold = True
        run.font.size = Pt(14) if level == 1 else Pt(12)
        run.font.color.rgb = color
        heading.style = f"Heading {level}"
    
    
    
    try:
        
        ###LOG
        aLogEntry.objects.create(
                user=request.user,
                message=f"at {now()} {request.user} accessed Load  "
            )
        print(f"at {now()} {User} accessed Download Report")
        ###LOG

        # Get the company of the logged-in user    
        user_company = None
        if request.user.is_authenticated:
            try:
                user_company = UserCompany.objects.get(user=request.user).company
            except UserCompany.DoesNotExist:
                user_company = None

        print(user_company)

        aCompany = UserCompany.objects.get(user=request.user)
        machine = get_object_or_404(modelcalc, id=machine_id)
        project = APP_Project.objects.get(name=machine.project.name)
        
        
        print(aCompany.id)
        print(project.id)
    
        print("Company 2")

        
        sheet_key = machine.oSec00Field03
    
        #Define Retrieve values from AddMachine model
        try:
            machine_config = AddMachine.objects.get(keyValue=sheet_key, company=user_company)
            form_type = machine_config.nameFormCalcXX
            aMachineName = machine_config.nameMachine
        except AddMachine.DoesNotExist:
            form_type = "None"
            aMachineName = "None"

        # Optional: Handle cases where the sheet_key is invalid
        if form_type is None:
            print(f"Warning: Unknown sheet_key '{sheet_key}'")

        # Create a Word document
        doc = Document()

        # Add header and footer with page numbers
        add_header_footer(doc)

        # Add project title
        doc.add_heading(f'Project Report: {project.name}', level=1)

        # Add project details
        doc.add_heading("Project Details", level=2)     

        doc.add_paragraph("\n")
        doc.add_paragraph("Name: " + project.name)
        doc.add_paragraph("Client Name: " + project.client_name)
        doc.add_paragraph("Capacity: " + project.capacity)
        doc.add_paragraph("\n")
        
        doc.add_page_break()     
        doc.add_paragraph("\n")

        # Extract form data
        Input_data = [
            (machine.oSec01Field01, machine.oSec01Field02),
            (machine.oSec01Field03, machine.oSec01Field04),
            (machine.oSec01Field05, machine.oSec01Field06),
            (machine.oSec01Field07, machine.oSec01Field08),
            (machine.oSec01Field09, machine.oSec01Field10),
            (machine.oSec01Field11, machine.oSec01Field12),
            (machine.oSec01Field13, machine.oSec01Field14),
            (machine.oSec01Field15, machine.oSec01Field16),
            (machine.oSec01Field17, machine.oSec01Field18),
            (machine.oSec01Field19, machine.oSec01Field20),
            (machine.oSec01Field21, machine.oSec01Field22),
            (machine.oSec01Field23, machine.oSec01Field24),
            (machine.oSec01Field25, machine.oSec01Field26),
            (machine.oSec01Field27, machine.oSec01Field28),
            (machine.oSec01Field29, machine.oSec01Field30),
        ]
        Output_data = [
            (machine.oSec02Field01, machine.oSec02Field02),
            (machine.oSec02Field03, machine.oSec02Field04),
            (machine.oSec02Field05, machine.oSec02Field06),
            (machine.oSec02Field07, machine.oSec02Field08),
            (machine.oSec02Field09, machine.oSec02Field10),
            (machine.oSec02Field11, machine.oSec02Field12),
            (machine.oSec02Field13, machine.oSec02Field14),
            (machine.oSec02Field15, machine.oSec02Field16),
            (machine.oSec02Field17, machine.oSec02Field18),
            (machine.oSec02Field19, machine.oSec02Field20),
            (machine.oSec02Field21, machine.oSec02Field22),
            (machine.oSec02Field23, machine.oSec02Field24),
            (machine.oSec02Field25, machine.oSec02Field26),
            (machine.oSec02Field27, machine.oSec02Field28),
            (machine.oSec02Field29, machine.oSec02Field30),
        ]


        # Add machine title with font size 14 and numbering
        machine_title = doc.add_paragraph(f" {aMachineName}", style="Heading3")
        machine_title.runs[0].font.size = Pt(14)

        input_section_data = [("Field", "Value")]
        for input_key, input_value in Input_data:
            input_key = input_key.strip() if input_key else ""
            input_value = input_value.strip() if input_value else ""
            if input_key and input_value and input_key.lower() != "oooo" and input_key.lower() != "" and input_key.lower() != "n/a" and input_value.lower() != "oooo" and input_value.lower() != "" and input_value.lower() != "n/a":
                input_section_data.append((input_key, input_value))
        if len(input_section_data) > 1:  # If the section has valid data, create a table
            doc.add_paragraph(f"Input", style="Heading3")  # Only one title now
            add_table(doc, input_section_data)  # Removed redundant title

        output_section_data = [("Field", "Value")]
        for output_key, output_value in Output_data:
            output_key = output_key.strip() if output_key else ""
            output_value = output_value.strip() if output_value else ""
            if output_key and output_value and output_key.lower() != "oooo" and output_key.lower() != "" and output_key.lower() != "n/a" and output_value.lower() != "oooo" and output_value.lower() != "" and output_value.lower() != "n/a":
                output_section_data.append((output_key, output_value))
        if len(output_section_data) > 1:  # If the section has valid data, create a table
            doc.add_paragraph(f"Output", style="Heading3")  # Only one title now
            add_table(doc, output_section_data)  # Removed redundant title


        doc.add_page_break()     

        # Save the document to a response
        response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.wordprocessingml.document')
        response['Content-Disposition'] = f'attachment; filename={project.name}_report.docx'
        doc.save(response)
        return response

    except APP_Project.DoesNotExist:
        return HttpResponse("Project not found", status=404)