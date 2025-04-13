import pdb


from Apps.aAppMechanical.models import Project
from Apps.aAppMechanical.models import Machine
from Apps.aAppMechanical.models import UserCompany
from Apps.aAppMechanical.models import aLogEntry
from Apps.aAppMechanical.models import FormFieldConfig

from .forms import FormCalculationsSheet


from datetime import datetime
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

# Create your views here.
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
    "aSection03Show": aSection03Show,
    "aSection04Show": aSection04Show,
    "aSection05Show": aSection05Show,
    "aSection06Show": aSection06Show,
    "aSection07Show": aSection07Show,
    "aSection08Show": aSection08Show,
    "aSection09Show": aSection09Show,
    "aSection10Show": aSection10Show,
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

    return JsonResponse(data)