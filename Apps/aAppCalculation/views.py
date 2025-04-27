

from datetime import datetime
from Apps.aAdmin.models import UserRole, RoleAutho, Autho
from Apps.aAppMechanical.models import aLogEntry
from Apps.aAppSubmittal.models import AddMachine
from Apps.aAppProject.models import APP_Project
from .models import modelcalc
from Apps.aAppMechanical.models import UserCompany
import requests

from .forms import FormCalculationSheet

from django.http import HttpResponse
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.shortcuts import render, redirect
from django.urls import reverse
from django.utils.timezone import now 
from django.contrib.auth.models import User
from django.conf import settings

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
        "reqType": req_type,
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
###################################
###################################
###################################
###################################


def LoadPageCalculationSheet(request):

    # Redirect unauthenticated users
    if not request.user.is_authenticated:
        return redirect("login")

    sheet_keys = AddMachine.objects.exclude(nameFormCalcXX__isnull=True).exclude(nameFormCalcXX__exact="None")


    sheet_key = None

    
    
    
    # If POST, get the selected sheet_key
    if request.method == "POST":
        sheet_key = request.POST.get("sheet_key")

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
        machine_config = AddMachine.objects.get(keyValue=sheet_key)
        form_type = machine_config.nameFormCalcXX
        DB_Name = machine_config.nameDB
        aMachineName = machine_config.nameMachine
    except AddMachine.DoesNotExist:
        form_type = "None"
        DB_Name = "None"
        aMachineName = "None"
        


    # Optional: Handle cases where the sheet_key is invalid
    if form_type is None:
        print(f"Warning: Unknown sheet_key '{sheet_key}'")


     # Assign company filter only if the user has a company
    if user_company:
        machinescalc = modelcalc.objects.filter(oSec00Field03=DB_Name, company=user_company)
        projects = APP_Project.objects.filter(company=user_company)
    else:
        machinescalc = modelcalc.objects.none()  # Return an empty queryset if no company
        projects = APP_Project.objects.none()  # Return an empty queryset if no company



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
    

    return render(request, "PageCalculationSheet.html", {
    "form": form,
    "machinescalc": machinescalc,
    "projects": projects,  
    "aMachineName": aMachineName, 
    "user_company": user_company, 
    "sheet_key": sheet_key,
    "sheet_keys": sheet_keys,
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
    
})

def HandleCalculationSheetForm(request):
    sheet_key = request.POST.get("sheet_key")
    print(sheet_key)


    if not request.user.is_authenticated:
        return redirect('login')
    
    

    form_mapping = {
        "NS": {
            "input_fields": [
                'oSec01Field01', 'oSec01Field02', 'oSec01Field03', 'oSec01Field04',
                'oSec01Field05', 'oSec01Field06', 'oSec01Field07', 'oSec01Field08',
            ],
            "output_fields": {
                "oSec02Field01": "O_Weight",
            },
        },
        "MS": {
            "input_fields": [
                'oSec01Field01', 'oSec01Field02', 'oSec01Field03', 'oSec01Field04',
                'oSec01Field05', 'oSec01Field06', 'oSec01Field07', 'oSec01Field08',
                'oSec01Field09', 'oSec01Field10', 'oSec01Field11',
            ],
            "output_fields": {
                "oSec02Field01": "MS_w",
                "oSec02Field02": "MS_p",
                "oSec02Field03": "MS_s",
            },
        },
        "BC": {
            "input_fields": [
                'oSec01Field01', 'oSec01Field02', 'oSec01Field03', 'oSec01Field04',
                'oSec01Field05', 'oSec01Field06', 'oSec01Field07',
            ],
            "output_fields": {
                "oSec02Field01": "BC_w",
                "oSec02Field02": "BC_p",
                "oSec02Field03": "BC_s",
            },
        },
        "GR": {
            "input_fields": [
                'oSec01Field01', 'oSec01Field02', 'oSec01Field03', 'oSec01Field04',
                'oSec01Field05', 'oSec01Field06', 'oSec01Field07', 'oSec01Field08',
            ],
            "output_fields": {
                "oSec02Field01": "GR_out3",
                "oSec02Field02": "GR_out1",
                "oSec02Field03": "GR_out2",
                "oSec02Field04": "GR_out4",
                "oSec02Field05": "GR_out5",
                "oSec02Field06": "GR_out6",
            },
        },
        "PS": {
            "input_fields": [
                'oSec01Field01', 'oSec01Field02', 'oSec01Field03', 'oSec01Field04',
            ],
            "output_fields": {
                "oSec02Field01": "PS_out2",
                "oSec02Field02": "PS_out1",
                "oSec02Field03": "000",
                "oSec02Field04": "PS_out3",
                "oSec02Field05": "PS_out4",
            },
        },
        "TH": {
            "input_fields": [
                'oSec01Field01', 'oSec01Field02', 'oSec01Field03', 'oSec01Field04',
            ],
            "output_fields": {
                "oSec02Field01": "TH_w",
                "oSec02Field02": "TH_p",
                "oSec02Field03": "TH_s",
            },
        },
        "MX": {
            "input_fields": [
                'oSec01Field01', 'oSec01Field02', 'oSec01Field03', 'oSec01Field04',
                'oSec01Field05', 'oSec01Field06', 'oSec01Field07', 'oSec01Field08',
            ],
            "output_fields": {
                "oSec02Field01": "000",
                "oSec02Field02": "MX_p",
                "oSec02Field03": "MX_s",
                "oSec02Field04": "MX_d",
                "oSec02Field05": "MX_shaftL",
                "oSec02Field06": "MX_shaftD",
                "oSec02Field07": "MX_Type",
            },
        },
        "RT": {
            "input_fields": [
                'oSec01Field01', 'oSec01Field02', 'oSec01Field03', 'oSec01Field04',
                'oSec01Field05', 'oSec01Field06',
            ],
            "output_fields": {
                "oSec02Field01": "RT_w10",
            },
        },
        "CT": {
            "input_fields": [
                'oSec01Field01', 'oSec01Field02',
            ],
            "output_fields": {
                "oSec02Field01": "O_Tank_Weight",
                "oSec02Field02": "O_Tank_Volume",
                "oSec02Field03": "O_Tank_Shell_Th",
                "oSec02Field04": "O_Tank_Base_Th",
                "oSec02Field05": "O_Tank_Shell_Weight",
                "oSec02Field06": "O_Tank_Base_Weight",
                "oSec02Field07": "O_Tank_Base_UPN_Weight",
                "oSec02Field08": "O_Tank_Cover_Weight",
            },
        },
        "SC": {
            "input_fields": [
                'oSec01Field01', 'oSec01Field02', 'oSec01Field03', 'oSec01Field04',
                'oSec01Field05', 'oSec01Field06', 'oSec01Field07', 'oSec01Field08',
            ],
            "output_fields": {
                "oSec02Field01": "Pitch",
                "oSec02Field02": "SpeedRPM",
                "oSec02Field03": "MotorPower",
                "oSec02Field04": "ScrewWeight",
                "oSec02Field05": "FrameWeight",
                "oSec02Field06": "1111",
            },
        },
        "BS": {
            "input_fields": [
                'oSec01Field01', 'oSec01Field02', 'oSec01Field03', 'oSec01Field04',
                'oSec01Field05', 'oSec01Field06',
            ],
            "output_fields": {
                "oSec02Field01": "O_Weight_allBars",
                "oSec02Field02": "O_Plate_weight",
                "oSec02Field03": "O_Total_weight",
            },
        },
        "PNch": {
            "input_fields": [
                'oSec01Field01', 'oSec01Field02', 'oSec01Field03', 'oSec01Field04',
                'oSec01Field05', 'oSec01Field06', 'oSec01Field07', 'oSec01Field08',
                'oSec01Field09', 'oSec01Field10',
            ],
            "output_fields": {
                "oSec02Field01": "O_Frame_Perimeter",
                "oSec02Field02": "O_Frame_Weight",
                "oSec02Field03": "O_Gate_PL_Weight",
                "oSec02Field04": "O_Gate_Stiffener_N",
                "oSec02Field05": "O_Gate_Stiffener_Weight",
                "oSec02Field06": "O_Gate_Weight",
                "oSec02Field07": "O_Total_Weight",
            },
        },
        "PNwa": {
            "input_fields": [
                'oSec01Field01', 'oSec01Field02', 'oSec01Field03', 'oSec01Field04',
                'oSec01Field05', 'oSec01Field06', 'oSec01Field07', 'oSec01Field08',
                'oSec01Field09', 'oSec01Field10',
            ],
            "output_fields": {
                "oSec02Field01": "O_PNwa_Out01",
                "oSec02Field02": "O_PNwa_Out02",
                "oSec02Field03": "O_PNwa_Out03",
                "oSec02Field04": "O_PNwa_Out04",
                "oSec02Field05": "O_PNwa_Out05",
                "oSec02Field06": "O_PNwa_Out06",
                "oSec02Field07": "O_PNwa_Out07",
            },
        },
    }

    #Define Retrieve values from AddMachine model
    try:
        machine_config = AddMachine.objects.get(keyValue=sheet_key)
        form_type = machine_config.nameFormCalcXX
        aMachineName = machine_config.nameMachine
    except AddMachine.DoesNotExist:
        form_type = "None"
        aMachineName = "None"
        


    config = form_mapping.get(sheet_key)
    if not config:
        return redirect('PageCalculationSheet.html')  # Or a 404 page

    
    req_type = sheet_key
    input_fields = config['input_fields']
    output_fields = config['output_fields']

    if request.method == 'POST' and 'form1_submit' in request.POST:
        form = FormCalculationSheet(form_type=form_type, data=request.POST)
        if form.is_valid():
            input_data = {
                f"{req_type}_{field.split('oSec01Field')[1]}": form.cleaned_data.get(field)
                for field in input_fields if form.cleaned_data.get(field) is not None
            }

            response = interact_with_api(
                "https://us-central1-h1000project1.cloudfunctions.net/f01",
                req_type,
                input_data
            )


            instance = form.save(commit=False)
            for form_field, api_key in output_fields.items():
                if api_key not in ["000", "1111"]:
                    setattr(instance, form_field, response[api_key])
            instance.oSec00Field01 = request.user.username
            instance.oSec00Field02 = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            instance.oSec00Field03 = sheet_key
            instance.save()

            # Refill form for display
            initial_data = {field: form.cleaned_data.get(field) for field in input_fields}
            for form_field, api_key in output_fields.items():
                if api_key not in ["000", "1111"]:
                    initial_data[form_field] = response[api_key]

            form = FormCalculationSheet(form_type=form_type, initial=initial_data)
            

            # Initialize visibility dictionaries
            aSection01FieldShow = {f"aSection01Field{str(i).zfill(2)}Show": "Hide" for i in range(1, 21)}
            aSection02FieldShow = {f"aSection02Field{str(i).zfill(2)}Show": "Hide" for i in range(1, 21)}
            
            # Update visibility based on field counts
            for i in range(1, len(input_fields) + 1):
                aSection01FieldShow[f"aSection01Field{str(i).zfill(2)}Show"] = "Yes"
            
            for i in range(1, len(output_fields) + 1):
                aSection02FieldShow[f"aSection02Field{str(i).zfill(2)}Show"] = "Yes"
            
            
            

            return render(request, 'PageCalculationSheet.html', {
                'form': form,
                'sheet_key': sheet_key,
                'aMachineName': aMachineName,
                **aSection01FieldShow,
                **aSection02FieldShow,
            })

    return redirect(f"{sheet_key.lower()}_load")


def generate_report(request):
    sheet_key = request.POST.get("sheet_key")
    print(sheet_key)

    #Define Retrieve values from AddMachine model
    try:
        machine_config = AddMachine.objects.get(keyValue=sheet_key)
        form_type = machine_config.nameFormCalcXX
        DB_Name = machine_config.nameDB
        aMachineName = machine_config.nameMachine
    except AddMachine.DoesNotExist:
        form_type = "None"
        DB_Name = "None"
        aMachineName = "None"

    # Optional: Handle cases where the sheet_key is invalid
    if form_type is None:
        print(f"Warning: Unknown sheet_key '{sheet_key}'")

    if request.method == "POST":
        form1 = FormCalculationSheet(form_type=form_type)
        # Create a new Word document
        doc = Document()
        doc.add_heading(aMachineName, level=1)

        # Extract form data
        form_data = {
            "Input": [
                (form1.fields["oSec01Field01"].label, request.POST.get("oSec01Field01", "N/A")),
                (form1.fields["oSec01Field02"].label, request.POST.get("oSec01Field02", "N/A")),
                (form1.fields["oSec01Field03"].label, request.POST.get("oSec01Field03", "N/A")),
                (form1.fields["oSec01Field04"].label, request.POST.get("oSec01Field04", "N/A")),
                (form1.fields["oSec01Field05"].label, request.POST.get("oSec01Field05", "N/A")),
                (form1.fields["oSec01Field06"].label, request.POST.get("oSec01Field06", "N/A")),
                (form1.fields["oSec01Field07"].label, request.POST.get("oSec01Field07", "N/A")),
                (form1.fields["oSec01Field08"].label, request.POST.get("oSec01Field08", "N/A")),
                (form1.fields["oSec01Field09"].label, request.POST.get("oSec01Field09", "N/A")),
                (form1.fields["oSec01Field10"].label, request.POST.get("oSec01Field10", "N/A")),
                (form1.fields["oSec01Field11"].label, request.POST.get("oSec01Field11", "N/A")),
                (form1.fields["oSec01Field12"].label, request.POST.get("oSec01Field12", "N/A")),
                (form1.fields["oSec01Field13"].label, request.POST.get("oSec01Field13", "N/A")),
                (form1.fields["oSec01Field14"].label, request.POST.get("oSec01Field14", "N/A")),
                (form1.fields["oSec01Field15"].label, request.POST.get("oSec01Field15", "N/A")),
                (form1.fields["oSec01Field16"].label, request.POST.get("oSec01Field16", "N/A")),
                (form1.fields["oSec01Field17"].label, request.POST.get("oSec01Field17", "N/A")),
                (form1.fields["oSec01Field18"].label, request.POST.get("oSec01Field18", "N/A")),
                (form1.fields["oSec01Field19"].label, request.POST.get("oSec01Field19", "N/A")),
                (form1.fields["oSec01Field20"].label, request.POST.get("oSec01Field20", "N/A")),
            ],
            "Output": [
                (form1.fields["oSec02Field01"].label, request.POST.get("oSec02Field01", "N/A")),
                (form1.fields["oSec02Field02"].label, request.POST.get("oSec02Field02", "N/A")),
                (form1.fields["oSec02Field03"].label, request.POST.get("oSec02Field03", "N/A")),
                (form1.fields["oSec02Field04"].label, request.POST.get("oSec02Field04", "N/A")),
                (form1.fields["oSec02Field05"].label, request.POST.get("oSec02Field05", "N/A")),
                (form1.fields["oSec02Field06"].label, request.POST.get("oSec02Field06", "N/A")),
                (form1.fields["oSec02Field07"].label, request.POST.get("oSec02Field07", "N/A")),
                (form1.fields["oSec02Field08"].label, request.POST.get("oSec02Field08", "N/A")),
                (form1.fields["oSec02Field09"].label, request.POST.get("oSec02Field09", "N/A")),
                (form1.fields["oSec02Field10"].label, request.POST.get("oSec02Field10", "N/A")),
                (form1.fields["oSec02Field11"].label, request.POST.get("oSec02Field11", "N/A")),
                (form1.fields["oSec02Field12"].label, request.POST.get("oSec02Field12", "N/A")),
                (form1.fields["oSec02Field13"].label, request.POST.get("oSec02Field13", "N/A")),
                (form1.fields["oSec02Field14"].label, request.POST.get("oSec02Field14", "N/A")),
                (form1.fields["oSec02Field15"].label, request.POST.get("oSec02Field15", "N/A")),
                (form1.fields["oSec02Field16"].label, request.POST.get("oSec02Field16", "N/A")),
                (form1.fields["oSec02Field17"].label, request.POST.get("oSec02Field17", "N/A")),
                (form1.fields["oSec02Field18"].label, request.POST.get("oSec02Field18", "N/A")),
                (form1.fields["oSec02Field19"].label, request.POST.get("oSec02Field19", "N/A")),
                (form1.fields["oSec02Field20"].label, request.POST.get("oSec02Field20", "N/A")),
            ]
        }

        # Add form data to the Word document
        for section, fields in form_data.items():
            doc.add_heading(section, level=2)
            for field, value in fields:
                if value != "N/A":
                    doc.add_paragraph(f"{field}: {value}")

        # Prepare the response to download the document
        response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.wordprocessingml.document')
        response['Content-Disposition'] = f'attachment; filename="{sheet_key}_report.docx"'
        doc.save(response)
        return response

    return HttpResponse("Invalid request", status=400)