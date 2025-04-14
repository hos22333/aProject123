import pdb


from Apps.aAppMechanical.models import Project
from Apps.aAppMechanical.models import Machine
from Apps.aAppMechanical.models import UserCompany
from Apps.aAppMechanical.models import aLogEntry
from Apps.aAppMechanical.models import FormFieldConfig
from Apps.aAppMechanical.views import interact_with_api

from . import forms


from datetime import datetime
from docx import Document
from Apps.aApp1.models import UserRole, RoleAutho, Autho
import requests

from django.http import HttpResponse
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.shortcuts import render, redirect
from django.urls import reverse
from django.utils.timezone import now 
from django.contrib.auth.models import User
from django.conf import settings

""" # Create your views here.
def LoadPageCalculationsSheet(request, sheet_key):
    #pdb.set_trace()
    print(sheet_key)
    
    # Redirect unauthenticated users
    if not request.user.is_authenticated:
        return redirect("login")  
    
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




    # Define a dictionary mapping sheet keys to their corresponding values
    sheet_mapping = {
        "MS": ("FCS_MechanicalScreen",          "CalculationsSheetMS",      "Mechanical Screen"),
        "BC": ("FCS_BeltConveyor",              "CalculationsSheetBC",      "Belt Conveyor"),
        "GR": ("FCS_GritGreaseRemoval",         "CalculationsSheetGR",      "Gritremoval"),
        "PS": ("FCS_PrimarySedimentationTank",  "CalculationsSheetPS",      "Primary Sedimentation Tank"),
        "TH": ("FCS_SludgeThickener",           "CalculationsSheetTH",      "Thickener"),
        "MX": ("FCS_Rectangular Mixers",           "CalculationsSheetMX",      "Rectangular Mixers"),
        "RT": ("FCS_Rectangular Tanks",           "CalculationsSheetRT",      "Rectangular Tanks"),
        "CT": ("FCS_Circular Tanks",           "CalculationsSheetCT",      "Circular Tanks"),
        "SC": ("FCS_Screw Conveyor",           "CalculationsSheetSC",      "Screw Conveyor"),
        "BS": ("FCS_Basket Screen",           "CalculationsSheetBS",      "Basket Screen"),
        "NS": ("formCalculationsSheetNS",               "CalculationsSheetNS",      "Manual Screen"),
        "PNch": ("FCS_Channel Penstock",                 "CalculationsSheetPNch",      "Channel Penstock"),
        "PNwa": ("FCS_Wall Penstock",                  "CalculationsSheetPNwa",      "Wall Penstock"),
    }

    # Retrieve values using the dictionary
    form_type, DB_Name, aMachineName = sheet_mapping.get(sheet_key, ("None", "None", "None"))

    # Optional: Handle cases where the sheet_key is invalid
    if form_type is None:
        print(f"Warning: Unknown sheet_key '{sheet_key}'")




    # Assign company filter only if the user has a company
    if user_company:
        machines = Machine.objects.filter(oSec00Field03=DB_Name, company=user_company)
        projects = Project.objects.filter(company=user_company)
    else:
        machines = Machine.objects.none()  # Return an empty queryset if no company
        projects = Project.objects.none()  # Return an empty queryset if no company



    form = FormCalculationsSheet(user=request.user, form_type=form_type)
    
    print(f"Initial value for oSec01Field02: {form.fields['oSec01Field02'].initial}")
    
    
    # Initialize all section variables
    aSection01Show = "Yes"
    aSection02Show = "Yes"
    
    print(form.fields['oSec01Field01'].initial)
    print(form.fields['oSec02Field01'].initial)

    # Apply conditions to modify the values
    if form.fields['oSec01Field01'].initial in ["oooo", None]:
        aSection01Show = "Hide"

    if form.fields['oSec02Field01'].initial in ["oooo", None]:
        aSection02Show = "Hide"

   
    
    print(aSection01Show)
    print(aSection02Show)
    
    # print(projects)

    return render(request, "PageCalculationsSheet.html", {
    "form": form,
    "machines": machines,
    "projects": projects,  
    "aMachineName": aMachineName,  
    "user_company": user_company,
    "sheet_key": sheet_key,
    "aSection01Show": aSection01Show,
    "aSection02Show": aSection02Show,
})




def SavePageCalculationsSheet(request, sheet_key):    
    print(sheet_key)
    
    # Redirect unauthenticated users
    if not request.user.is_authenticated:
        return redirect("login")  
    
    
    ###LOG
    aLogEntry.objects.create(
            user=request.user,
            message=f"at {now()} {request.user} accessed Load {sheet_key} "
        )
    
    
    # Get the company of the logged-in user    
    user_company = None
    if request.user.is_authenticated:
        try:
            user_company = UserCompany.objects.get(user=request.user).company
        except UserCompany.DoesNotExist:
            user_company = None


    
    # Define a dictionary mapping sheet keys to their corresponding values
    sheet_mapping = {
        "NS": ("formDataSheetNS",               "DataSheetNS",      "Manual Screen"),
        "MS": ("FDS_MechanicalScreen",          "DataSheetMS",      "Mechanical Screen"),
        "BC": ("FDS_BeltConveyor",              "DataSheetBC",      "Belt Conveyor"),
        "CO": ("FDS_Container",                 "DataSheetCO",      "Container"),
        "GR": ("FDS_GritGreaseRemoval",         "DataSheetGR",      "Gritremoval"),
        "SS": ("FDS_SandSilo",                  "DataSheetSS",      "Sand Silo"),
        "PS": ("FDS_PrimarySedimentationTank",  "DataSheetPS",      "Primary Sedimentation Tank"),
        "QV": ("FDS_QuickValve",                "DataSheetQV",      "Quick Valve"),
        "TV": ("FDS_TelescopicValve",           "DataSheetTV",      "Telescopic Valve"),
        "TH": ("FDS_SludgeThickener",           "DataSheetTH",      "Thickener"),
    }

    # Retrieve values using the dictionary
    form_type, DB_Name, aMachineName = sheet_mapping.get(sheet_key, ("None", "None", "None"))
    


    # Assign company filter only if the user has a company
    if user_company:
        machines = Machine.objects.filter(oSec00Field03=DB_Name, company=user_company)
        projects = Project.objects.filter(company=user_company)
    else:
        machines = Machine.objects.none()  # Return an empty queryset if no company
        projects = Project.objects.none()  # Return an empty queryset if no company

    print(form_type)
    

    if request.method == "POST":
        form = FormCalculationsSheet(form_type=form_type, data=request.POST)

        if form.is_valid():
            instance = form.save(commit=False)  # Don't save to DB yet

            # Assign common fields
            instance.oSec00Field01 = request.user.username  # Username
            instance.oSec00Field02 = datetime.now().strftime("%Y-%m-%d %H:%M:%S")  # Timestamp
            instance.oSec00Field03 = DB_Name  # Fixed type

            # Handle project assignment
            project_id = request.POST.get("project")
            if project_id:
                try:
                    instance.project = Project.objects.get(id=project_id)
                except Project.DoesNotExist:
                    return render(request, "PageDataSheet.html", {"form": form, "error": "Invalid Project ID"})
            else:
                return render(request, "PageDataSheet.html", {"form": form, "error": "Project is required"})

            # Get the company associated with the user
            try:
                user_company = UserCompany.objects.get(user=request.user).company
                instance.company = user_company  # Assign company to the instance
            except UserCompany.DoesNotExist:
                return render(request, "PageDataSheet.html", 
                              {"form": form, 
                               "error": "User is not associated with a company",
                               "aMachineName": aMachineName,
                               "sheet_key" : sheet_key})

            # Save the instance to the database
            instance.save()

            # Refresh form with initial values
            form = FormCalculationsSheet(initial=form.cleaned_data, form_type=form_type)

            # Filter machines by the user’s company
            machines = Machine.objects.filter(oSec00Field03=DB_Name, company=user_company)

            #######################################
            #######################################
            #######################################
            print("#######################")
        
            # Initialize all section variables
            aSection01Show = "Yes"
            aSection02Show = "Yes"
            aSection03Show = "Yes"
            aSection04Show = "Yes"
            aSection05Show = "Yes"
            aSection06Show = "Yes"
            aSection07Show = "Yes"
            aSection08Show = "Yes"
            aSection09Show = "Yes"
            aSection10Show = "Yes"
            
            print(form.fields['oSec01Field01'].initial)
            print(form.fields['oSec02Field01'].initial)
            print(form.fields['oSec03Field01'].initial)
            print(form.fields['oSec04Field01'].initial)
            print(form.fields['oSec05Field01'].initial)
            print(form.fields['oSec06Field01'].initial)
            print(form.fields['oSec07Field01'].initial)
            print(form.fields['oSec08Field01'].initial)
            print(form.fields['oSec09Field01'].initial)
            print(form.fields['oSec10Field01'].initial)
        
            # Apply conditions to modify the values
            if form.fields['oSec01Field01'].initial in ["oooo", None]:
                aSection01Show = "Hide"
        
            if form.fields['oSec02Field01'].initial in ["oooo", None]:
                aSection02Show = "Hide"
        
            if form.fields['oSec03Field01'].initial in ["oooo", None]:
                aSection03Show = "Hide"
        
            if form.fields['oSec04Field01'].initial in ["oooo", None]:
                aSection04Show = "Hide"
        
            if form.fields['oSec05Field01'].initial in ["oooo", None]:
                aSection05Show = "Hide"
        
            if form.fields['oSec06Field01'].initial in ["oooo", None]:
                aSection06Show = "Hide"
        
            if form.fields['oSec07Field01'].initial in ["oooo", None]:
                aSection07Show = "Hide"
        
            if form.fields['oSec08Field01'].initial in ["oooo", None]:
                aSection08Show = "Hide"
        
            if form.fields['oSec09Field01'].initial in ["oooo", None]:
                aSection09Show = "Hide"
        
            if form.fields['oSec10Field01'].initial in ["oooo", None]:
                aSection10Show = "Hide"
            
            print(aSection01Show)
            print(aSection02Show)
            print(aSection03Show)
            print(aSection04Show)
            print(aSection05Show)
            print(aSection06Show)
            print(aSection07Show)
            print(aSection08Show)
            print(aSection09Show)
            print(aSection10Show)
            
            

            return render(request, "PageDataSheet.html", {
                "form": form,
                "machines": machines,
                "projects": projects,  
                "aMachineName": aMachineName,  
                "user_company": user_company,
                "sheet_key": sheet_key,
                "aSection01Show": aSection01Show,
                "aSection02Show": aSection02Show,
                "aSection03Show": aSection03Show,
                "aSection04Show": aSection04Show,
                "aSection05Show": aSection05Show,
                "aSection06Show": aSection06Show,
                "aSection07Show": aSection07Show,
                "aSection08Show": aSection08Show,
                "aSection09Show": aSection09Show,
                "aSection10Show": aSection10Show,
            })

        else:
            # If the form has errors, return all machines for this DB_Name (no company filtering)
            machines = Machine.objects.filter(oSec00Field03=DB_Name)
            return render(request, "PageDataSheet.html", {"form": form, "error": "Form contains errors", "machines": machines})

    return redirect("ms_load")  # Redirect for invalid requests


def DataSheetNS_get_datasheet_data(request, machine_id):
    machine = get_object_or_404(Machine, id=machine_id)
    
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
        
        "oSec03Field01": machine.oSec03Field01,
        "oSec03Field02": machine.oSec03Field02,
        "oSec03Field03": machine.oSec03Field03,
        "oSec03Field04": machine.oSec03Field04,
        "oSec03Field05": machine.oSec03Field05,
        "oSec03Field06": machine.oSec03Field06,
        "oSec03Field07": machine.oSec03Field07,
        "oSec03Field08": machine.oSec03Field08,
        "oSec03Field09": machine.oSec03Field09,
        "oSec03Field10": machine.oSec03Field10,        
        "oSec03Field11": machine.oSec03Field11,
        "oSec03Field12": machine.oSec03Field12,
        "oSec03Field13": machine.oSec03Field13,
        "oSec03Field14": machine.oSec03Field14,
        "oSec03Field15": machine.oSec03Field15,
        "oSec03Field16": machine.oSec03Field16,
        "oSec03Field17": machine.oSec03Field17,
        "oSec03Field18": machine.oSec03Field18,
        "oSec03Field19": machine.oSec03Field19,
        "oSec03Field20": machine.oSec03Field20,
        
        "oSec04Field01": machine.oSec04Field01,
        "oSec04Field02": machine.oSec04Field02,
        "oSec04Field03": machine.oSec04Field03,
        "oSec04Field04": machine.oSec04Field04,
        "oSec04Field05": machine.oSec04Field05,
        "oSec04Field06": machine.oSec04Field06,
        "oSec04Field07": machine.oSec04Field07,
        "oSec04Field08": machine.oSec04Field08,
        "oSec04Field09": machine.oSec04Field09,
        "oSec04Field10": machine.oSec04Field10,        
        "oSec04Field11": machine.oSec04Field11,
        "oSec04Field12": machine.oSec04Field12,
        "oSec04Field13": machine.oSec04Field13,
        "oSec04Field14": machine.oSec04Field14,
        "oSec04Field15": machine.oSec04Field15,
        "oSec04Field16": machine.oSec04Field16,
        "oSec04Field17": machine.oSec04Field17,
        "oSec04Field18": machine.oSec04Field18,
        "oSec04Field19": machine.oSec04Field19,
        "oSec04Field20": machine.oSec04Field20,
        
        "oSec05Field01": machine.oSec05Field01,
        "oSec05Field02": machine.oSec05Field02,
        "oSec05Field03": machine.oSec05Field03,
        "oSec05Field04": machine.oSec05Field04,
        "oSec05Field05": machine.oSec05Field05,
        "oSec05Field06": machine.oSec05Field06,
        "oSec05Field07": machine.oSec05Field07,
        "oSec05Field08": machine.oSec05Field08,
        "oSec05Field09": machine.oSec05Field09,
        "oSec05Field10": machine.oSec05Field10,        
        "oSec05Field11": machine.oSec05Field11,
        "oSec05Field12": machine.oSec05Field12,
        "oSec05Field13": machine.oSec05Field13,
        "oSec05Field14": machine.oSec05Field14,
        "oSec05Field15": machine.oSec05Field15,
        "oSec05Field16": machine.oSec05Field16,
        "oSec05Field17": machine.oSec05Field17,
        "oSec05Field18": machine.oSec05Field18,
        "oSec05Field19": machine.oSec05Field19,
        "oSec05Field20": machine.oSec05Field20,
        
        "oSec06Field01": machine.oSec06Field01,
        "oSec06Field02": machine.oSec06Field02,
        "oSec06Field03": machine.oSec06Field03,
        "oSec06Field04": machine.oSec06Field04,
        "oSec06Field05": machine.oSec06Field05,
        "oSec06Field06": machine.oSec06Field06,
        "oSec06Field07": machine.oSec06Field07,
        "oSec06Field08": machine.oSec06Field08,
        "oSec06Field09": machine.oSec06Field09,
        "oSec06Field10": machine.oSec06Field10,        
        "oSec06Field11": machine.oSec06Field11,
        "oSec06Field12": machine.oSec06Field12,
        "oSec06Field13": machine.oSec06Field13,
        "oSec06Field14": machine.oSec06Field14,
        "oSec06Field15": machine.oSec06Field15,
        "oSec06Field16": machine.oSec06Field16,
        "oSec06Field17": machine.oSec06Field17,
        "oSec06Field18": machine.oSec06Field18,
        "oSec06Field19": machine.oSec06Field19,
        "oSec06Field20": machine.oSec06Field20,
        
        "oSec07Field01": machine.oSec07Field01,
        "oSec07Field02": machine.oSec07Field02,
        "oSec07Field03": machine.oSec07Field03,
        "oSec07Field04": machine.oSec07Field04,
        "oSec07Field05": machine.oSec07Field05,
        "oSec07Field06": machine.oSec07Field06,
        "oSec07Field07": machine.oSec07Field07,
        "oSec07Field08": machine.oSec07Field08,
        "oSec07Field09": machine.oSec07Field09,
        "oSec07Field10": machine.oSec07Field10,        
        "oSec07Field11": machine.oSec07Field11,
        "oSec07Field12": machine.oSec07Field12,
        "oSec07Field13": machine.oSec07Field13,
        "oSec07Field14": machine.oSec07Field14,
        "oSec07Field15": machine.oSec07Field15,
        "oSec07Field16": machine.oSec07Field16,
        "oSec07Field17": machine.oSec07Field17,
        "oSec07Field18": machine.oSec07Field18,
        "oSec07Field19": machine.oSec07Field19,
        "oSec07Field20": machine.oSec07Field20,
        
        "oSec08Field01": machine.oSec08Field01,
        "oSec08Field02": machine.oSec08Field02,
        "oSec08Field03": machine.oSec08Field03,
        "oSec08Field04": machine.oSec08Field04,
        "oSec08Field05": machine.oSec08Field05,
        "oSec08Field06": machine.oSec08Field06,
        "oSec08Field07": machine.oSec08Field07,
        "oSec08Field08": machine.oSec08Field08,
        "oSec08Field09": machine.oSec08Field09,
        "oSec08Field10": machine.oSec08Field10,        
        "oSec08Field11": machine.oSec08Field11,
        "oSec08Field12": machine.oSec08Field12,
        "oSec08Field13": machine.oSec08Field13,
        "oSec08Field14": machine.oSec08Field14,
        "oSec08Field15": machine.oSec08Field15,
        "oSec08Field16": machine.oSec08Field16,
        "oSec08Field17": machine.oSec08Field17,
        "oSec08Field18": machine.oSec08Field18,
        "oSec08Field19": machine.oSec08Field19,
        "oSec08Field20": machine.oSec08Field20,
        
        "oSec09Field01": machine.oSec09Field01,
        "oSec09Field02": machine.oSec09Field02,
        "oSec09Field03": machine.oSec09Field03,
        "oSec09Field04": machine.oSec09Field04,
        "oSec09Field05": machine.oSec09Field05,
        "oSec09Field06": machine.oSec09Field06,
        "oSec09Field07": machine.oSec09Field07,
        "oSec09Field08": machine.oSec09Field08,
        "oSec09Field09": machine.oSec09Field09,
        "oSec09Field10": machine.oSec09Field10,        
        "oSec09Field11": machine.oSec09Field11,
        "oSec09Field12": machine.oSec09Field12,
        "oSec09Field13": machine.oSec09Field13,
        "oSec09Field14": machine.oSec09Field14,
        "oSec09Field15": machine.oSec09Field15,
        "oSec09Field16": machine.oSec09Field16,
        "oSec09Field17": machine.oSec09Field17,
        "oSec09Field18": machine.oSec09Field18,
        "oSec09Field19": machine.oSec09Field19,
        "oSec09Field20": machine.oSec09Field20,
        
        "oSec10Field01": machine.oSec10Field01,
        "oSec10Field02": machine.oSec10Field02,
        "oSec10Field03": machine.oSec10Field03,
        "oSec10Field04": machine.oSec10Field04,
        "oSec10Field05": machine.oSec10Field05,
        "oSec10Field06": machine.oSec10Field06,
        "oSec10Field07": machine.oSec10Field07,
        "oSec10Field08": machine.oSec10Field08,
        "oSec10Field09": machine.oSec10Field09,
        "oSec10Field10": machine.oSec10Field10,        
        "oSec10Field11": machine.oSec10Field11,
        "oSec10Field12": machine.oSec10Field12,
        "oSec10Field13": machine.oSec10Field13,
        "oSec10Field14": machine.oSec10Field14,
        "oSec10Field15": machine.oSec10Field15,
        "oSec10Field16": machine.oSec10Field16,
        "oSec10Field17": machine.oSec10Field17,
        "oSec10Field18": machine.oSec10Field18,
        "oSec10Field19": machine.oSec10Field19,
        "oSec10Field20": machine.oSec10Field20,
        
        
        
        # Add other fields if necessary
    }

    return JsonResponse(data) """


SHEET_CONFIG = {
    'MS': {
        'form_class': forms.formCalcMS,
        'aMachineName': 'Mechanical Screen',
        'template': 'PageCalculationsSheet.html',
        'api_type': 'MS',
        'input_fields': [
            'oSec01Field01', 'oSec01Field02', 'oSec01Field03',
            'oSec01Field04', 'oSec01Field05', 'oSec01Field06', 'oSec01Field07',
            'oSec01Field08', 'oSec01Field09', 'oSec01Field10', 'oSec01Field11',
        ],
        'output_fields': ['oSec02Field01', 'oSec02Field02', 'oSec02Field03'],
        'api_fields': {
            "MS_ChannelHeight":     'oSec01Field01',
                "MS_ScreenWidth":       'oSec01Field02',
                "MS_BeltHeight":        'oSec01Field03',
                "MS_WaterLevel":        'oSec01Field04',
                "MS_BarSpacing":        'oSec01Field05',
                "MS_BarThickness":      'oSec01Field06',
                "MS_BarWidth":          'oSec01Field07',
                "MS_InclinationDegree": 'oSec01Field08',
                "MS_SprocketDiameter":  'oSec01Field09',
                "MS_Velocity":          'oSec01Field10',
                "MS_FOS":               'oSec01Field11',
        },
    },
    'BC': {
        'form_class': forms.formCalcBC,
        'aMachineName': 'Belt Conveyor',
        'template': 'PageCalculationsSheet.html',
        'api_type': 'BC',
        'input_fields': [
            'oSec01Field01', 'oSec01Field02', 'oSec01Field03',
            'oSec01Field04', 'oSec01Field05', 'oSec01Field06', 'oSec01Field07',
        ],
        'output_fields': ['oSec02Field01', 'oSec02Field02', 'oSec02Field03'],
        'api_fields': {
            'BC_Length': 'oSec01Field01',
            'BC_Width': 'oSec01Field02',
            'BC_DrumDia': 'oSec01Field03',
            'BC_Friction': 'oSec01Field04',
            'BC_Velocity': 'oSec01Field05',
            'BC_FOS': 'oSec01Field06',
            'BC_Belt_weight_per_meter': 'oSec01Field07',
        },
    },
    'GR': {
        'form_class': forms.formCalcGR,
        'aMachineName': 'Grit Removal',
        'template': 'PageCalculationsSheet.html',
        'api_type': 'GR',
        'input_fields': [
            'oSec01Field01', 'oSec01Field02', 'oSec01Field03', 'oSec01Field04',
            'oSec01Field05', 'oSec01Field06', 'oSec01Field07', 'oSec01Field08',
        ],
        'output_fields': [
            'oSec02Field01', 'oSec02Field02', 'oSec02Field03',
            'oSec02Field04', 'oSec02Field05', 'oSec02Field06',
        ],
        'api_fields': {
            'GR_n_channel': 'oSec01Field01',
            'GR_channel_width': 'oSec01Field02',
            'GR_civil_width': 'oSec01Field03',
            'GR_bridge_length': 'oSec01Field04',
            'GR_wheel_diameter': 'oSec01Field05',
            'GR_Friction': 'oSec01Field06',
            'GR_Velocity': 'oSec01Field07',
            'GR_FOS': 'oSec01Field08',
        },
    },
    'PS': {
        'form_class': forms.formCalcPS,
        'aMachineName': 'PST',
        'template': 'PageCalculationsSheet.html',
        'api_type': 'PS',
        'input_fields': [
            'oSec01Field01', 'oSec01Field02', 'oSec01Field03', 'oSec01Field04',
        ],
        'output_fields': [
            'oSec02Field01', 'oSec02Field02', 'oSec02Field03',
            'oSec02Field04', 'oSec02Field05'
        ],
        'api_fields': {
                "PS_walkway_length":     'oSec01Field01',
                "PS_Friction":       'oSec01Field02',
                "PS_Velocity":        'oSec01Field03',
                "PS_FOS":        'oSec01Field04',
        },
    },
    'TH': {
        'form_class': forms.formCalcTH,
        'aMachineName': 'Thickener',
        'template': 'PageCalculationsSheet.html',
        'api_type': 'TH',
        'input_fields': [
            'oSec01Field01', 'oSec01Field02', 'oSec01Field03', 'oSec01Field04',
        ],
        'output_fields': [
            'oSec02Field01', 'oSec02Field02', 'oSec02Field03',
            'oSec02Field04', 'oSec02Field05',
        ],
        'api_fields': {
            "TH_diameter":     'oSec01Field01',
                "TH_n_arm":       'oSec01Field02',
                "TH_Velocity":        'oSec01Field03',
                "TH_FOS":        'oSec01Field04',
        },
    },
    'MX': {
        'form_class': forms.formCalcMX,
        'aMachineName': 'Rectangular Mixers',
        'template': 'PageCalculationsSheet.html',
        'api_type': 'MX',
        'input_fields': [
            'oSec01Field01', 'oSec01Field02', 'oSec01Field03', 'oSec01Field04',
            'oSec01Field05', 'oSec01Field06', 'oSec01Field07', 'oSec01Field08',
        ],
        'output_fields': [
            'oSec02Field01', 'oSec02Field02', 'oSec02Field03', 'oSec02Field04', 
            'oSec02Field05', 'oSec02Field06', 'oSec02Field07',
        ],
        'api_fields': {
            "MX_length":        'oSec01Field01',
             "MX_width":         'oSec01Field02',
             "MX_water_depth":           'oSec01Field03',
             "MX_tank_depth":            'oSec01Field04',
             "MX_impeller_coefficient":  'oSec01Field05',
             "MX_velocity_gradient":     'oSec01Field06',
             "MX_impeller_diameter_factor":  'oSec01Field07',
             "MX_safety_factor":             'oSec01Field08',
        },
    },
    'RT': {
        'form_class': forms.formCalcRT,
        'aMachineName': 'Rectangular Tanks',
        'template': 'PageCalculationsSheet.html',
        'api_type': 'RT',
        'input_fields': [
            'oSec01Field01', 'oSec01Field02', 'oSec01Field03', 'oSec01Field04',
            'oSec01Field05', 'oSec01Field06',
        ],
        'output_fields': [
            'oSec02Field01', 
        ],
        'api_fields': {
            "RT_Length":        'oSec01Field01',
            "RT_Width":         'oSec01Field02',
            "RT_Hight":           'oSec01Field03',
            "RT_ShellTH":            'oSec01Field04',
            "RT_BaseTH":    'oSec01Field05',
            "RT_N_Spliter":     'oSec01Field06',
        },
    },
    'CT': {
        'form_class': forms.formCalcCT,
        'aMachineName': 'Circular Tanks',
        'template': 'PageCalculationsSheet.html',
        'api_type': 'GR',
        'input_fields': [
            'oSec01Field01', 'oSec01Field02',
        ],
        'output_fields': [
            'oSec02Field01', 'oSec02Field02', 'oSec02Field03', 'oSec02Field04', 
            'oSec02Field05', 'oSec02Field06', 'oSec02Field07', 'oSec02Field08',
        ],
        'api_fields': {
            "CT_Diameter":        'oSec01Field01',
            "CT_Height":         'oSec01Field02',
        },
    },
    'SC': {
        'form_class': forms.formCalcSC,
        'aMachineName': 'Screw Conveyor',
        'template': 'PageCalculationsSheet.html',
        'api_type': 'SC',
        'input_fields': [
            'oSec01Field01', 'oSec01Field02', 'oSec01Field03', 'oSec01Field04',
            'oSec01Field05', 'oSec01Field06', 'oSec01Field07', 'oSec01Field08',
        ],
        'output_fields': [
            'oSec02Field01', 'oSec02Field02', 'oSec02Field03',
            'oSec02Field04', 'oSec02Field05', 'oSec02Field06',
        ],
        'api_fields': {
            'aInput01': 'oSec01Field01',
            'aInput02': 'oSec01Field02',
            'aInput03': 'oSec01Field03',
            'aInput04': 'oSec01Field04',
            'aInput05': 'oSec01Field05',
            'aInput06': 'oSec01Field06',
            'aInput07': 'oSec01Field07',
            'aInput08': 'oSec01Field08',
        },
    },
    'BS': {
        'form_class': forms.formCalcBS,
        'aMachineName': 'Basket Screen',
        'template': 'PageCalculationsSheet.html',
        'api_type': 'BS',
        'input_fields': [
            'oSec01Field01', 'oSec01Field02', 'oSec01Field03', 'oSec01Field04',
            'oSec01Field05', 'oSec01Field06',
        ],
        'output_fields': [
            'oSec02Field01', 'oSec02Field02', 'oSec02Field03',
        ],
        'api_fields': {
            'BS_Bar_Dia': 'oSec01Field01',
            'BS_Bar_Space': 'oSec01Field02',
            'BS_Screen_Height': 'oSec01Field03',
            'BS_Screen_Width': 'oSec01Field04',
            'BS_Screen_Depth': 'oSec01Field05',
            'BS_Plate_Th': 'oSec01Field06',
        },
    },
    'NS': {
        'form_class': forms.formCalcNS,
        'aMachineName': 'Manual Screen',
        'template': 'PageCalculationsSheet.html',
        'api_type': 'NS',
        'input_fields': [
            'oSec01Field01', 'oSec01Field02', 'oSec01Field03', 'oSec01Field04',
            'oSec01Field05', 'oSec01Field06', 'oSec01Field07', 'oSec01Field08',
        ],
        'output_fields': [
            'oSec02Field01',
        ],
        'api_fields': {
            'NS_Ch_Height': 'oSec01Field01',
            'NS_Ch_Width': 'oSec01Field02',
            'NS_WaterLv': 'oSec01Field03',
            'NS_WaterLv_Margin': 'oSec01Field04',
            'NS_Bar_Spacing': 'oSec01Field05',
            'NS_Bar_Th': 'oSec01Field06',
            'NS_Bar_Width': 'oSec01Field07',
            'NS_Angle': 'oSec01Field08',
        },
    },
    'PNch': {
        'form_class': forms.formCalcPNch,
        'aMachineName': 'Channel Penstock',
        'template': 'PageCalculationsSheet.html',
        'api_type': 'PNch',
        'input_fields': [
            'oSec01Field01', 'oSec01Field02', 'oSec01Field03', 'oSec01Field04',
            'oSec01Field05', 'oSec01Field06', 'oSec01Field07', 'oSec01Field08',
            'oSec01Field09', 'oSec01Field10',
        ],
        'output_fields': [
            'oSec02Field01', 'oSec02Field02', 'oSec02Field03', 'oSec02Field04', 
            'oSec02Field05', 'oSec02Field06', 'oSec02Field07', 
        ],
        'api_fields': {
            'PNch_Channel_Height': 'oSec01Field01',
            'PNch_Frame_Height_Over_Channel': 'oSec01Field02',
            'PNch_Channel_Width': 'oSec01Field03',
            'PNch_Gate_Margin_Width': 'oSec01Field04',
            'PNch_Water_Lv': 'oSec01Field05',
            'PNch_Gate_Margin_Over_Water_Lv': 'oSec01Field06',
            'PNch_Gate_Th': 'oSec01Field07',
            'PNch_Gate_Other_PLs': 'oSec01Field08',
            'PNch_HeadStock': 'oSec01Field09',
            'PNch_Frame_Weight_Per_M': 'oSec01Field10',
        },
    },
    'PNwa': {
        'form_class': forms.formCalcPNwa,
        'aMachineName': 'Wall Penstock',
        'template': 'PageCalculationsSheet.html',
        'api_type': 'PNwa',
        'input_fields': [
            'oSec01Field01', 'oSec01Field02', 'oSec01Field03', 'oSec01Field04',
            'oSec01Field05', 'oSec01Field06', 'oSec01Field07', 'oSec01Field08',
            'oSec01Field09', 'oSec01Field10',
        ],
        'output_fields': [
            'oSec02Field01', 'oSec02Field02', 'oSec02Field03', 'oSec02Field04', 
            'oSec02Field05', 'oSec02Field06', 'oSec02Field07', 
        ],
        'api_fields': {
            'aInput01': 'oSec01Field01',
            'aInput02': 'oSec01Field02',
            'aInput03': 'oSec01Field03',
            'aInput04': 'oSec01Field04',
            'aInput05': 'oSec01Field05',
            'aInput06': 'oSec01Field06',
            'aInput07': 'oSec01Field07',
            'aInput08': 'oSec01Field08',
            'aInput09': 'oSec01Field09',
            'aInput010': 'oSec01Field10',
        },
    },
    
}

def LoadPageCalculationsSheet(request, sheet_key):
    if not request.user.is_authenticated:
        return redirect('login')

    config = SHEET_CONFIG.get(sheet_key)
    if not config:
        return HttpResponse("Invalid sheet key", status=404)

    aMachineName = config['aMachineName']
    form_class = config['form_class']
    template = config['template']
    api_type = config['api_type']
    api_url = "https://us-central1-h1000project1.cloudfunctions.net/f01"

    if request.method == "GET":
        form = form_class()
        # Initialize all section variables
        aSection01Show = "Yes"
        aSection02Show = "Yes"

        print(form.fields['oSec01Field01'].initial)
        print(form.fields['oSec02Field01'].initial)

        # Apply conditions to modify the values
        if form.fields['oSec01Field01'].initial in ["oooo", None]:
            aSection01Show = "Hide"

        if form.fields['oSec02Field01'].initial in ["oooo", None]:
            aSection02Show = "Hide"

    

        print(aSection01Show)
        print(aSection02Show)
        return render(request, template, {
            'form1': form,
            'aMachineName':aMachineName,
            "aSection01Show": aSection01Show,
            "aSection02Show": aSection02Show,
            })

    if request.method == "POST":
        form = form_class(request.POST)
        if 'generate_report' in request.POST:
            doc = Document()
            doc.add_heading(f'{sheet_key} Report', level=1)

            sections = {
                "Input": config['input_fields'],
                "Output": config['output_fields'],
            }

            for section, fields in sections.items():
                doc.add_heading(section, level=2)
                for field in fields:
                    label = form.fields[field].label
                    value = request.POST.get(field, "N/A")
                    doc.add_paragraph(f"{label}: {value}")

            response = HttpResponse(
                content_type='application/vnd.openxmlformats-officedocument.wordprocessingml.document'
            )
            response['Content-Disposition'] = f'attachment; filename="{sheet_key}_Report.docx"'
            doc.save(response)
            return response
        
        if 'form1_submit' in request.POST:
            if form.is_valid():
                cleaned = form.cleaned_data
                input_data = {
                    api_key: cleaned.get(form_field)
                    for api_key, form_field in config['api_fields'].items()
                }
    
                # Call external API
                response = interact_with_api(api_url, api_type, input_data)
    
                # Update output fields
                instance = form.save(commit=False)
                for field in config['output_fields']:
                    if field in response:
                        setattr(instance, field, response[field])
    
                instance.oSec00Field01 = request.user.username
                instance.oSec00Field02 = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                instance.oSec00Field03 = sheet_key
                instance.save()
    
                # Re-initialize with new values for display
                initial_data = {field: cleaned.get(field) for field in config['input_fields']}
                initial_data.update({field: response.get(field) for field in config['output_fields']})
                form = form_class(initial=initial_data)
                # Initialize all section variables
                aSection01Show = "Yes"
                aSection02Show = "Yes"
    
                print(form.fields['oSec01Field01'].initial)
                print(form.fields['oSec02Field01'].initial)
    
                # Apply conditions to modify the values
                if form.fields['oSec01Field01'].initial in ["oooo", None]:
                    aSection01Show = "Hide"
    
                if form.fields['oSec02Field01'].initial in ["oooo", None]:
                    aSection02Show = "Hide"
    
    
    
                print(aSection01Show)
                print(aSection02Show)
    
            return render(request, template, {
                'form1': form,
                'aMachineName':aMachineName,
                "aSection01Show": aSection01Show,
                "aSection02Show": aSection02Show,
                })

    return HttpResponse("Invalid request method", status=405)

""" def generate_report(request, form, config, sheet_key):
    doc = Document()
    doc.add_heading(f'{sheet_key} Report', level=1)

    sections = {
        "Input": config['input_fields'],
        "Output": config['output_fields'],
    }

    for section, fields in sections.items():
        doc.add_heading(section, level=2)
        for field in fields:
            label = form.fields[field].label
            value = request.POST.get(field, "N/A")
            doc.add_paragraph(f"{label}: {value}")

    response = HttpResponse(
        content_type='application/vnd.openxmlformats-officedocument.wordprocessingml.document'
    )
    response['Content-Disposition'] = f'attachment; filename="{sheet_key}_Report.docx"'
    doc.save(response)
    return response """



""" def handle_calc_form(request, sheet_key):
    if not request.user.is_authenticated:
        return redirect('login')

    form_classes = {
        "MS": form.formCalcMS,
        "BC": form.formCalcBC,
        # Add other forms if needed
    }

    req_types = {
        "MS": "MS",
        "BC": "BC",
    }

    api_field_map = {
        "MS": {
            "input_fields": [
                "MS_ChannelHeight", "MS_ScreenWidth", "MS_BeltHeight",
                "MS_WaterLevel", "MS_BarSpacing", "MS_BarThickness",
                "MS_BarWidth", "MS_InclinationDegree", "MS_SprocketDiameter",
                "MS_Velocity", "MS_FOS",
            ],
            "field_keys": [
                'oSec01Field01', 'oSec01Field02', 'oSec01Field03',
                'oSec01Field04', 'oSec01Field05', 'oSec01Field06',
                'oSec01Field07', 'oSec01Field08', 'oSec01Field09',
                'oSec01Field10', 'oSec01Field11',
            ],
            "response_keys": ["MS_w", "MS_p", "MS_s"],
        },
        "BC": {
            "input_fields": [
                "BC_Length", "BC_Width", "BC_DrumDia",
                "BC_Friction", "BC_Velocity", "BC_FOS",
                "BC_Belt_weight_per_meter",
            ],
            "field_keys": [
                'oSec01Field01', 'oSec01Field02', 'oSec01Field03',
                'oSec01Field04', 'oSec01Field05', 'oSec01Field06',
                'oSec01Field07',
            ],
            "response_keys": ["BC_w", "BC_p", "BC_s"],
        },
    }

    if request.method == 'POST' and 'form1_submit' in request.POST:
        form_class = form_classes.get(sheet_key)
        config = api_field_map.get(sheet_key)
        if not form_class or not config:
            return redirect('PageCalculationsSheet.html')  # fallback if sheet_key is not supported

        form = form_class(request.POST)
        if form.is_valid():
            input_data = {
                api_name: form.cleaned_data.get(field_name)
                for api_name, field_name in zip(config["input_fields"], config["field_keys"])
            }

            # Call the API
            api_url = "https://us-central1-h1000project1.cloudfunctions.net/f01"
            req_type = req_types[sheet_key]
            response = interact_with_api(api_url, req_type, input_data)

            instance = form.save(commit=False)
            instance.oSec00Field01 = request.user.username
            instance.oSec00Field02 = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            instance.oSec00Field03 = sheet_key

            # Fill response data
            for i, key in enumerate(config["response_keys"], start=1):
                setattr(instance, f'oSec02Field0{i}', response.get(key))

            instance.save()

            # Refill the form with both input and response
            initial_data = {field: form.cleaned_data.get(field) for field in config["field_keys"]}
            for i, key in enumerate(config["response_keys"], start=1):
                initial_data[f'oSec02Field0{i}'] = response.get(key)

            form = form_class(initial=initial_data)

            return render(request, "PageCalculationsSheet.html", {"form1": form, "sheet_key": sheet_key})

    return redirect(f"{sheet_key.lower()}_load")  # Redirect to fallback """