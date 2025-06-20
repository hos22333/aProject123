import pdb
import json

from Apps.aAppProject.models import APP_Project
from .models import AddMachine
from .models import Machine
from .models import Machine_log
from .models import DXF_data
from Apps.aAppMechanical.models import UserCompany
from Apps.aAppMechanical.models import aLogEntry
from Apps.aAdmin.models import DataTransfer
from Apps.aAppCalculation.models import modelcalc
from Apps.aAppMechanical.models import Companies
from Apps.aAppMechanical.models import FormFieldConfig


from .forms import FormDataSheet, FormDataSheet_log


from django.utils.text import slugify

from datetime import datetime
import requests


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


def LoadPageDataSheet(request):
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

    sheet_keys = AddMachine.objects.exclude(nameForm__isnull=True).exclude(nameForm__exact="None").exclude(nameForm__exact="No").filter(company=user_company).order_by('order')

    sheet_key = None
    
    # If POST, get the selected sheet_key
    if request.method == "POST" and 'loadpage' in request.POST:
        sheet_key = request.POST.get("sheet_key")
        if sheet_key :
            machineShow = "Yes"

    #pdb.set_trace()
    print(sheet_key)
    
    
    
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
        form_type = machine_config.nameForm
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
        machines = Machine.objects.filter(oSec00Field03=DB_Name, company=user_company)
        projects = APP_Project.objects.filter(company=user_company)
    else:
        machines = Machine.objects.none()  # Return an empty queryset if no company
        projects = APP_Project.objects.none()  # Return an empty queryset if no company



    form = FormDataSheet(user=request.user, form_type=form_type)
    
    

    print(f"Initial value for oSec01Field02: {form.fields['oSec01Field02'].initial}")
    
    
    # Initialize all section variables
    """ for i in range(1, 11):
       locals()[f"aSection{str(i).zfill(2)}Show"] = "Yes" """

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

    # Initialize visibility dictionaries
    """ for j in range(1, 11):
       locals()[f"aSection{str(j).zfill(2)}Show"] = {f"aSection{str(j).zfill(2)}Field{str(i).zfill(2)}Show": "Yes" for i in range(1, 21)} """
    aSection01FieldShow = {f"aSection01Field{str(i).zfill(2)}Show": "Yes" for i in range(1, 21)}
    aSection02FieldShow = {f"aSection02Field{str(i).zfill(2)}Show": "Yes" for i in range(1, 21)}
    aSection03FieldShow = {f"aSection03Field{str(i).zfill(2)}Show": "Yes" for i in range(1, 21)}
    aSection04FieldShow = {f"aSection04Field{str(i).zfill(2)}Show": "Yes" for i in range(1, 21)}
    aSection05FieldShow = {f"aSection05Field{str(i).zfill(2)}Show": "Yes" for i in range(1, 21)}
    aSection06FieldShow = {f"aSection06Field{str(i).zfill(2)}Show": "Yes" for i in range(1, 21)}
    aSection07FieldShow = {f"aSection07Field{str(i).zfill(2)}Show": "Yes" for i in range(1, 21)}
    aSection08FieldShow = {f"aSection08Field{str(i).zfill(2)}Show": "Yes" for i in range(1, 21)}
    aSection09FieldShow = {f"aSection09Field{str(i).zfill(2)}Show": "Yes" for i in range(1, 21)}
    aSection10FieldShow = {f"aSection10Field{str(i).zfill(2)}Show": "Yes" for i in range(1, 21)}
    

    """ for j in range(1, 11):
        print(form.fields[f'oSec{str(j).zfill(2)}Field01'].initial)  """
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
    """ for j in range(1, 11):
        if form.fields[f'oSec{str(j).zfill(2)}Field01'].initial in ["oooo", None]:
            locals()[f"aSection{str(j).zfill(2)}Show"] = "Hide" """
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
    
   
    # Update visibility based on field counts
    for i in range(0, 10):
        if form.fields[f'oSec01Field{str(i*2+1).zfill(2)}'].initial in ["oooo", None]:
            aSection01FieldShow[f"aSection01Field{str(i*2+1).zfill(2)}Show"] = "Hide"
            aSection01FieldShow[f"aSection01Field{str(i*2+2).zfill(2)}Show"] = "Hide"
    
    for i in range(0, 10):
        if form.fields[f'oSec02Field{str(i*2+1).zfill(2)}'].initial in ["oooo", None]:
            aSection02FieldShow[f"aSection02Field{str(i*2+1).zfill(2)}Show"] = "Hide"
            aSection02FieldShow[f"aSection02Field{str(i*2+2).zfill(2)}Show"] = "Hide"
    
    for i in range(0, 10):
        if form.fields[f'oSec03Field{str(i*2+1).zfill(2)}'].initial in ["oooo", None]:
            aSection03FieldShow[f"aSection03Field{str(i*2+1).zfill(2)}Show"] = "Hide"
            aSection03FieldShow[f"aSection03Field{str(i*2+2).zfill(2)}Show"] = "Hide"
    
    for i in range(0, 10):
        if form.fields[f'oSec04Field{str(i*2+1).zfill(2)}'].initial in ["oooo", None]:
            aSection04FieldShow[f"aSection04Field{str(i*2+1).zfill(2)}Show"] = "Hide"
            aSection04FieldShow[f"aSection04Field{str(i*2+2).zfill(2)}Show"] = "Hide"
    
    for i in range(0, 10):
        if form.fields[f'oSec05Field{str(i*2+1).zfill(2)}'].initial in ["oooo", None]:
            aSection05FieldShow[f"aSection05Field{str(i*2+1).zfill(2)}Show"] = "Hide"
            aSection05FieldShow[f"aSection05Field{str(i*2+2).zfill(2)}Show"] = "Hide"
    
    for i in range(0, 10):
        if form.fields[f'oSec06Field{str(i*2+1).zfill(2)}'].initial in ["oooo", None]:
            aSection06FieldShow[f"aSection06Field{str(i*2+1).zfill(2)}Show"] = "Hide"
            aSection06FieldShow[f"aSection06Field{str(i*2+2).zfill(2)}Show"] = "Hide"
    
    for i in range(0, 10):
        if form.fields[f'oSec07Field{str(i*2+1).zfill(2)}'].initial in ["oooo", None]:
            aSection07FieldShow[f"aSection07Field{str(i*2+1).zfill(2)}Show"] = "Hide"
            aSection07FieldShow[f"aSection07Field{str(i*2+2).zfill(2)}Show"] = "Hide"
    
    for i in range(0, 10):
        if form.fields[f'oSec08Field{str(i*2+1).zfill(2)}'].initial in ["oooo", None]:
            aSection08FieldShow[f"aSection08Field{str(i*2+1).zfill(2)}Show"] = "Hide"
            aSection08FieldShow[f"aSection08Field{str(i*2+2).zfill(2)}Show"] = "Hide"
    
    for i in range(0, 10):
        if form.fields[f'oSec09Field{str(i*2+1).zfill(2)}'].initial in ["oooo", None]:
            aSection09FieldShow[f"aSection09Field{str(i*2+1).zfill(2)}Show"] = "Hide"
            aSection09FieldShow[f"aSection09Field{str(i*2+2).zfill(2)}Show"] = "Hide"
    
    for i in range(0, 10):
        if form.fields[f'oSec10Field{str(i*2+1).zfill(2)}'].initial in ["oooo", None]:
            aSection10FieldShow[f"aSection10Field{str(i*2+1).zfill(2)}Show"] = "Hide"
            aSection10FieldShow[f"aSection10Field{str(i*2+2).zfill(2)}Show"] = "Hide"
    
    # print(projects)

    return render(request, "PageDataSheet.html", {
        "form": form,
        "machines": machines,
        "projects": projects,  
        "aMachineName": aMachineName,  
        "user_company": user_company,
        "sheet_key": sheet_key,
        "sheet_keys": sheet_keys,
        "machineShow": machineShow,
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
        **aSection01FieldShow,
        **aSection02FieldShow,
        **aSection03FieldShow,
        **aSection04FieldShow,
        **aSection05FieldShow,
        **aSection06FieldShow,
        **aSection07FieldShow,
        **aSection08FieldShow,
        **aSection09FieldShow,
        **aSection10FieldShow,
    })







def SavePageDataSheet(request):
    sheet_key = request.POST.get("sheet_key")
    print(sheet_key)
    if sheet_key :
        machineShow = "Yes"
    # Redirect unauthenticated users
    if not request.user.is_authenticated:
        return redirect("login")  
    
    
    ###LOG
    aLogEntry.objects.create(
            user=request.user,
            message=f"at {now()} {request.user} saved accessed Load {sheet_key} "
        )
    
    
    # Get the company of the logged-in user    
    user_company = None
    if request.user.is_authenticated:
        try:
            user_company = UserCompany.objects.get(user=request.user).company
        except UserCompany.DoesNotExist:
            user_company = None

    sheet_keys = AddMachine.objects.exclude(nameForm__isnull=True).exclude(nameForm__exact="None").exclude(nameForm__exact="No").filter(company=user_company).order_by('order')

    #Define Retrieve values from AddMachine model
    try:
        machine_config = AddMachine.objects.get(keyValue=sheet_key, company=user_company)
        form_type = machine_config.nameForm
        DB_Name = machine_config.nameDB
        aMachineName = machine_config.nameMachine
    except AddMachine.DoesNotExist:
        form_type = "None"
        DB_Name = "None"
        aMachineName = "None"
        

    # Assign company filter only if the user has a company
    if user_company:
        machines = Machine.objects.filter(oSec00Field03=DB_Name, company=user_company)
        projects = APP_Project.objects.filter(company=user_company)
    else:
        machines = Machine.objects.none()  # Return an empty queryset if no company
        projects = APP_Project.objects.none()  # Return an empty queryset if no company

    print(form_type)
    
    

    # ============================================
    # 🔵 HANDLE LOAD FROM modelcalc (preview only)
    # ============================================
    if request.method == "POST" and 'loadcalculationdataname' in request.POST:
        machineShow = "Yes"
        selected_project_id = request.POST.get("project")
        keyvalue = sheet_key[:-2] 
        print("Key Value : ",keyvalue)

        
        highlight_fields = []
        form_data = request.POST.copy()
        if selected_project_id:
            print("selected_project_id : ", selected_project_id)
            form_data["project"] = selected_project_id

        if sheet_key and selected_project_id:
            calc_instance = modelcalc.objects.filter(project_id=selected_project_id, company=user_company, oSec00Field03=sheet_key).first()
            if calc_instance:
                mappings = DataTransfer.objects.filter(keyValue=keyvalue, company=user_company)
                print("mappings : ", mappings)
                for mapping in mappings:
                    calc_field = mapping.CalculationField
                    print("calc Data : ", getattr(calc_instance, calc_field))
                    form_field = mapping.SubmittalField
                    if hasattr(calc_instance, calc_field):
                        form_data[form_field] = getattr(calc_instance, calc_field)
                        highlight_fields.append(form_field)
                    
                
                
        print("highlight_fields : ",highlight_fields)
        form = FormDataSheet(initial=form_data, form_type=form_type)

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

        # Initialize visibility dictionaries
        aSection01FieldShow = {f"aSection01Field{str(i).zfill(2)}Show": "Yes" for i in range(1, 21)}
        aSection02FieldShow = {f"aSection02Field{str(i).zfill(2)}Show": "Yes" for i in range(1, 21)}
        aSection03FieldShow = {f"aSection03Field{str(i).zfill(2)}Show": "Yes" for i in range(1, 21)}
        aSection04FieldShow = {f"aSection04Field{str(i).zfill(2)}Show": "Yes" for i in range(1, 21)}
        aSection05FieldShow = {f"aSection05Field{str(i).zfill(2)}Show": "Yes" for i in range(1, 21)}
        aSection06FieldShow = {f"aSection06Field{str(i).zfill(2)}Show": "Yes" for i in range(1, 21)}
        aSection07FieldShow = {f"aSection07Field{str(i).zfill(2)}Show": "Yes" for i in range(1, 21)}
        aSection08FieldShow = {f"aSection08Field{str(i).zfill(2)}Show": "Yes" for i in range(1, 21)}
        aSection09FieldShow = {f"aSection09Field{str(i).zfill(2)}Show": "Yes" for i in range(1, 21)}
        aSection10FieldShow = {f"aSection10Field{str(i).zfill(2)}Show": "Yes" for i in range(1, 21)}
            
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

        # Update visibility based on field counts
        for i in range(0, 10):
            if form.fields[f'oSec01Field{str(i*2+1).zfill(2)}'].initial in ["oooo", None, ""]:
                aSection01FieldShow[f"aSection01Field{str(i*2+1).zfill(2)}Show"] = "Hide"
                aSection01FieldShow[f"aSection01Field{str(i*2+2).zfill(2)}Show"] = "Hide"

        for i in range(0, 10):
            if form.fields[f'oSec02Field{str(i*2+1).zfill(2)}'].initial in ["oooo", None, ""]:
                aSection02FieldShow[f"aSection02Field{str(i*2+1).zfill(2)}Show"] = "Hide"
                aSection02FieldShow[f"aSection02Field{str(i*2+2).zfill(2)}Show"] = "Hide"

        for i in range(0, 10):
            if form.fields[f'oSec03Field{str(i*2+1).zfill(2)}'].initial in ["oooo", None, ""]:
                aSection03FieldShow[f"aSection03Field{str(i*2+1).zfill(2)}Show"] = "Hide"
                aSection03FieldShow[f"aSection03Field{str(i*2+2).zfill(2)}Show"] = "Hide"

        for i in range(0, 10):
            if form.fields[f'oSec04Field{str(i*2+1).zfill(2)}'].initial in ["oooo", None, ""]:
                aSection04FieldShow[f"aSection04Field{str(i*2+1).zfill(2)}Show"] = "Hide"
                aSection04FieldShow[f"aSection04Field{str(i*2+2).zfill(2)}Show"] = "Hide"

        for i in range(0, 10):
            if form.fields[f'oSec05Field{str(i*2+1).zfill(2)}'].initial in ["oooo", None, ""]:
                aSection05FieldShow[f"aSection05Field{str(i*2+1).zfill(2)}Show"] = "Hide"
                aSection05FieldShow[f"aSection05Field{str(i*2+2).zfill(2)}Show"] = "Hide"

        for i in range(0, 10):
            if form.fields[f'oSec06Field{str(i*2+1).zfill(2)}'].initial in ["oooo", None, ""]:
                aSection06FieldShow[f"aSection06Field{str(i*2+1).zfill(2)}Show"] = "Hide"
                aSection06FieldShow[f"aSection06Field{str(i*2+2).zfill(2)}Show"] = "Hide"

        for i in range(0, 10):
            if form.fields[f'oSec07Field{str(i*2+1).zfill(2)}'].initial in ["oooo", None, ""]:
                aSection07FieldShow[f"aSection07Field{str(i*2+1).zfill(2)}Show"] = "Hide"
                aSection07FieldShow[f"aSection07Field{str(i*2+2).zfill(2)}Show"] = "Hide"

        for i in range(0, 10):
            if form.fields[f'oSec08Field{str(i*2+1).zfill(2)}'].initial in ["oooo", None, ""]:
                aSection08FieldShow[f"aSection08Field{str(i*2+1).zfill(2)}Show"] = "Hide"
                aSection08FieldShow[f"aSection08Field{str(i*2+2).zfill(2)}Show"] = "Hide"

        for i in range(0, 10):
            if form.fields[f'oSec09Field{str(i*2+1).zfill(2)}'].initial in ["oooo", None, ""]:
                aSection09FieldShow[f"aSection09Field{str(i*2+1).zfill(2)}Show"] = "Hide"
                aSection09FieldShow[f"aSection09Field{str(i*2+2).zfill(2)}Show"] = "Hide"

        for i in range(0, 10):
            if form.fields[f'oSec10Field{str(i*2+1).zfill(2)}'].initial in ["oooo", None, ""]:
                aSection10FieldShow[f"aSection10Field{str(i*2+1).zfill(2)}Show"] = "Hide"
                aSection10FieldShow[f"aSection10Field{str(i*2+2).zfill(2)}Show"] = "Hide"
                    

        return render(request, "PageDataSheet.html", {
            "form": form,
            "machines": machines,
            "projects": projects,
            "aMachineName": aMachineName,
            "user_company": user_company,
            "sheet_key": sheet_key,
            "sheet_keys": sheet_keys,
            "machineShow": machineShow,
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
            **aSection01FieldShow,
            **aSection02FieldShow,
            **aSection03FieldShow,
            **aSection04FieldShow,
            **aSection05FieldShow,
            **aSection06FieldShow,
            **aSection07FieldShow,
            **aSection08FieldShow,
            **aSection09FieldShow,
            **aSection10FieldShow,
            "highlight_fields": highlight_fields,
        })


    

    # =====================================
    # ✅ HANDLE SAVE TO DATABASE
    # =====================================

    if request.method == "POST" and 'savebuttonname' in request.POST:
        form = FormDataSheet(form_type=form_type, data=request.POST)

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
                    instance.project = APP_Project.objects.get(id=project_id)
                except APP_Project.DoesNotExist:
                    return render(request, "PageDataSheet.html", {"form": form, "sheet_keys": sheet_keys, "error": "Invalid Project ID"})
            else:
                return render(request, "PageDataSheet.html", {"form": form, "sheet_keys": sheet_keys, "error": "Project is required"})

            # Get the company associated with the user
            try:
                user_company = UserCompany.objects.get(user=request.user).company
                instance.company = user_company  # Assign company to the instance
            except UserCompany.DoesNotExist:
                return render(request, "PageDataSheet.html", 
                              {"form": form, 
                               "error": "User is not associated with a company",
                               "aMachineName": aMachineName,
                               "sheet_key" : sheet_key,
                               "machineShow": machineShow,})

            # Save the instance to the database
            instance.save()

            # Refresh form with initial values
            form = FormDataSheet(initial=form.cleaned_data, form_type=form_type)

            # Filter machines by the user’s company
            machines = Machine.objects.filter(oSec00Field03=DB_Name, company=user_company)

            #######################################
            form1 = FormDataSheet_log(form_type=form_type, data=request.POST)

            if form1.is_valid():
                instance1 = form1.save(commit=False)  # Don't save to DB yet

                # Assign common fields
                instance1.oSec00Field01 = request.user.username  # Username
                instance1.oSec00Field02 = datetime.now().strftime("%Y-%m-%d %H:%M:%S")  # Timestamp
                instance1.oSec00Field03 = DB_Name  # Fixed type

                # Handle project assignment
                if project_id:
                    try:
                        instance1.project = APP_Project.objects.get(id=project_id)
                    except APP_Project.DoesNotExist:
                        return render(request, "PageDataSheet.html", {"form": form, "sheet_keys": sheet_keys, "error": "Invalid Project ID"})
                else:
                    return render(request, "PageDataSheet.html", {"form": form, "sheet_keys": sheet_keys, "error": "Project is required"})

                # Get the company associated with the user
                try:
                    user_company = UserCompany.objects.get(user=request.user).company
                    instance1.company = user_company  # Assign company to the instance
                except UserCompany.DoesNotExist:
                    return render(request, "PageDataSheet.html", 
                                  {"form": form, 
                                   "error": "User is not associated with a company",
                                   "aMachineName": aMachineName,
                                   "sheet_key" : sheet_key,
                                   "machineShow": machineShow,})

                # Save the instance to the database
                instance1.save()

                # Refresh form with initial values
                form1 = FormDataSheet_log(initial=form1.cleaned_data, form_type=form_type)
            
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

            # Initialize visibility dictionaries
            aSection01FieldShow = {f"aSection01Field{str(i).zfill(2)}Show": "Yes" for i in range(1, 21)}
            aSection02FieldShow = {f"aSection02Field{str(i).zfill(2)}Show": "Yes" for i in range(1, 21)}
            aSection03FieldShow = {f"aSection03Field{str(i).zfill(2)}Show": "Yes" for i in range(1, 21)}
            aSection04FieldShow = {f"aSection04Field{str(i).zfill(2)}Show": "Yes" for i in range(1, 21)}
            aSection05FieldShow = {f"aSection05Field{str(i).zfill(2)}Show": "Yes" for i in range(1, 21)}
            aSection06FieldShow = {f"aSection06Field{str(i).zfill(2)}Show": "Yes" for i in range(1, 21)}
            aSection07FieldShow = {f"aSection07Field{str(i).zfill(2)}Show": "Yes" for i in range(1, 21)}
            aSection08FieldShow = {f"aSection08Field{str(i).zfill(2)}Show": "Yes" for i in range(1, 21)}
            aSection09FieldShow = {f"aSection09Field{str(i).zfill(2)}Show": "Yes" for i in range(1, 21)}
            aSection10FieldShow = {f"aSection10Field{str(i).zfill(2)}Show": "Yes" for i in range(1, 21)}
            
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

            # Update visibility based on field counts
            for i in range(0, 10):
                if form.fields[f'oSec01Field{str(i*2+1).zfill(2)}'].initial in ["oooo", None, ""]:
                    aSection01FieldShow[f"aSection01Field{str(i*2+1).zfill(2)}Show"] = "Hide"
                    aSection01FieldShow[f"aSection01Field{str(i*2+2).zfill(2)}Show"] = "Hide"

            for i in range(0, 10):
                if form.fields[f'oSec02Field{str(i*2+1).zfill(2)}'].initial in ["oooo", None, ""]:
                    aSection02FieldShow[f"aSection02Field{str(i*2+1).zfill(2)}Show"] = "Hide"
                    aSection02FieldShow[f"aSection02Field{str(i*2+2).zfill(2)}Show"] = "Hide"

            for i in range(0, 10):
                if form.fields[f'oSec03Field{str(i*2+1).zfill(2)}'].initial in ["oooo", None, ""]:
                    aSection03FieldShow[f"aSection03Field{str(i*2+1).zfill(2)}Show"] = "Hide"
                    aSection03FieldShow[f"aSection03Field{str(i*2+2).zfill(2)}Show"] = "Hide"

            for i in range(0, 10):
                if form.fields[f'oSec04Field{str(i*2+1).zfill(2)}'].initial in ["oooo", None, ""]:
                    aSection04FieldShow[f"aSection04Field{str(i*2+1).zfill(2)}Show"] = "Hide"
                    aSection04FieldShow[f"aSection04Field{str(i*2+2).zfill(2)}Show"] = "Hide"

            for i in range(0, 10):
                if form.fields[f'oSec05Field{str(i*2+1).zfill(2)}'].initial in ["oooo", None, ""]:
                    aSection05FieldShow[f"aSection05Field{str(i*2+1).zfill(2)}Show"] = "Hide"
                    aSection05FieldShow[f"aSection05Field{str(i*2+2).zfill(2)}Show"] = "Hide"

            for i in range(0, 10):
                if form.fields[f'oSec06Field{str(i*2+1).zfill(2)}'].initial in ["oooo", None, ""]:
                    aSection06FieldShow[f"aSection06Field{str(i*2+1).zfill(2)}Show"] = "Hide"
                    aSection06FieldShow[f"aSection06Field{str(i*2+2).zfill(2)}Show"] = "Hide"

            for i in range(0, 10):
                if form.fields[f'oSec07Field{str(i*2+1).zfill(2)}'].initial in ["oooo", None, ""]:
                    aSection07FieldShow[f"aSection07Field{str(i*2+1).zfill(2)}Show"] = "Hide"
                    aSection07FieldShow[f"aSection07Field{str(i*2+2).zfill(2)}Show"] = "Hide"

            for i in range(0, 10):
                if form.fields[f'oSec08Field{str(i*2+1).zfill(2)}'].initial in ["oooo", None, ""]:
                    aSection08FieldShow[f"aSection08Field{str(i*2+1).zfill(2)}Show"] = "Hide"
                    aSection08FieldShow[f"aSection08Field{str(i*2+2).zfill(2)}Show"] = "Hide"

            for i in range(0, 10):
                if form.fields[f'oSec09Field{str(i*2+1).zfill(2)}'].initial in ["oooo", None, ""]:
                    aSection09FieldShow[f"aSection09Field{str(i*2+1).zfill(2)}Show"] = "Hide"
                    aSection09FieldShow[f"aSection09Field{str(i*2+2).zfill(2)}Show"] = "Hide"

            for i in range(0, 10):
                if form.fields[f'oSec10Field{str(i*2+1).zfill(2)}'].initial in ["oooo", None, ""]:
                    aSection10FieldShow[f"aSection10Field{str(i*2+1).zfill(2)}Show"] = "Hide"
                    aSection10FieldShow[f"aSection10Field{str(i*2+2).zfill(2)}Show"] = "Hide"
                    


            return render(request, "PageDataSheet.html", {
                "form": form,
                "machines": machines,
                "projects": projects,  
                "aMachineName": aMachineName,  
                "user_company": user_company,
                "sheet_key": sheet_key,
                "sheet_keys": sheet_keys,
                "machineShow": machineShow,
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
                **aSection01FieldShow,
                **aSection02FieldShow,
                **aSection03FieldShow,
                **aSection04FieldShow,
                **aSection05FieldShow,
                **aSection06FieldShow,
                **aSection07FieldShow,
                **aSection08FieldShow,
                **aSection09FieldShow,
                **aSection10FieldShow,
            })

        else:

            machines = Machine.objects.filter(oSec00Field03=DB_Name)
            return render(request, "PageDataSheet.html", {"form": form, "error": "Form contains errors", "machines": machines})

    return redirect("PageDataSheet")  # Redirect for invalid requests



def DeleteMachine(request, machine_id):  
    sheet_key = request.POST.get("sheet_key")
    print(sheet_key)
    if sheet_key :
        machineShow = "Yes"
    machine = get_object_or_404(Machine, id=machine_id)
    aLogEntry.objects.create(
        user=request.user,
        message=f"{request.user} Deleted >>> {machine.oSec00Field03} form the log "
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

    sheet_keys = AddMachine.objects.exclude(nameForm__isnull=True).exclude(nameForm__exact="None").exclude(nameForm__exact="No").filter(company=user_company).order_by('order')

    #Define Retrieve values from AddMachine model
    try:
        machine_config = AddMachine.objects.get(keyValue=sheet_key, company=user_company)
        form_type = machine_config.nameForm
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
        machines = Machine.objects.filter(oSec00Field03=DB_Name, company=user_company)
        projects = APP_Project.objects.filter(company=user_company)
    else:
        machines = Machine.objects.none()  # Return an empty queryset if no company
        projects = APP_Project.objects.none()  # Return an empty queryset if no company



    form = FormDataSheet(user=request.user, form_type=form_type)
    
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

    # Initialize visibility dictionaries
    aSection01FieldShow = {f"aSection01Field{str(i).zfill(2)}Show": "Yes" for i in range(1, 21)}
    aSection02FieldShow = {f"aSection02Field{str(i).zfill(2)}Show": "Yes" for i in range(1, 21)}
    aSection03FieldShow = {f"aSection03Field{str(i).zfill(2)}Show": "Yes" for i in range(1, 21)}
    aSection04FieldShow = {f"aSection04Field{str(i).zfill(2)}Show": "Yes" for i in range(1, 21)}
    aSection05FieldShow = {f"aSection05Field{str(i).zfill(2)}Show": "Yes" for i in range(1, 21)}
    aSection06FieldShow = {f"aSection06Field{str(i).zfill(2)}Show": "Yes" for i in range(1, 21)}
    aSection07FieldShow = {f"aSection07Field{str(i).zfill(2)}Show": "Yes" for i in range(1, 21)}
    aSection08FieldShow = {f"aSection08Field{str(i).zfill(2)}Show": "Yes" for i in range(1, 21)}
    aSection09FieldShow = {f"aSection09Field{str(i).zfill(2)}Show": "Yes" for i in range(1, 21)}
    aSection10FieldShow = {f"aSection10Field{str(i).zfill(2)}Show": "Yes" for i in range(1, 21)}
    
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
    
   
    # Update visibility based on field counts
    for i in range(0, 10):
        if form.fields[f'oSec01Field{str(i*2+1).zfill(2)}'].initial in ["oooo", None]:
            aSection01FieldShow[f"aSection01Field{str(i*2+1).zfill(2)}Show"] = "Hide"
            aSection01FieldShow[f"aSection01Field{str(i*2+2).zfill(2)}Show"] = "Hide"
    
    for i in range(0, 10):
        if form.fields[f'oSec02Field{str(i*2+1).zfill(2)}'].initial in ["oooo", None]:
            aSection02FieldShow[f"aSection02Field{str(i*2+1).zfill(2)}Show"] = "Hide"
            aSection02FieldShow[f"aSection02Field{str(i*2+2).zfill(2)}Show"] = "Hide"
    
    for i in range(0, 10):
        if form.fields[f'oSec03Field{str(i*2+1).zfill(2)}'].initial in ["oooo", None]:
            aSection03FieldShow[f"aSection03Field{str(i*2+1).zfill(2)}Show"] = "Hide"
            aSection03FieldShow[f"aSection03Field{str(i*2+2).zfill(2)}Show"] = "Hide"
    
    for i in range(0, 10):
        if form.fields[f'oSec04Field{str(i*2+1).zfill(2)}'].initial in ["oooo", None]:
            aSection04FieldShow[f"aSection04Field{str(i*2+1).zfill(2)}Show"] = "Hide"
            aSection04FieldShow[f"aSection04Field{str(i*2+2).zfill(2)}Show"] = "Hide"
    
    for i in range(0, 10):
        if form.fields[f'oSec05Field{str(i*2+1).zfill(2)}'].initial in ["oooo", None]:
            aSection05FieldShow[f"aSection05Field{str(i*2+1).zfill(2)}Show"] = "Hide"
            aSection05FieldShow[f"aSection05Field{str(i*2+2).zfill(2)}Show"] = "Hide"
    
    for i in range(0, 10):
        if form.fields[f'oSec06Field{str(i*2+1).zfill(2)}'].initial in ["oooo", None]:
            aSection06FieldShow[f"aSection06Field{str(i*2+1).zfill(2)}Show"] = "Hide"
            aSection06FieldShow[f"aSection06Field{str(i*2+2).zfill(2)}Show"] = "Hide"
    
    for i in range(0, 10):
        if form.fields[f'oSec07Field{str(i*2+1).zfill(2)}'].initial in ["oooo", None]:
            aSection07FieldShow[f"aSection07Field{str(i*2+1).zfill(2)}Show"] = "Hide"
            aSection07FieldShow[f"aSection07Field{str(i*2+2).zfill(2)}Show"] = "Hide"
    
    for i in range(0, 10):
        if form.fields[f'oSec08Field{str(i*2+1).zfill(2)}'].initial in ["oooo", None]:
            aSection08FieldShow[f"aSection08Field{str(i*2+1).zfill(2)}Show"] = "Hide"
            aSection08FieldShow[f"aSection08Field{str(i*2+2).zfill(2)}Show"] = "Hide"
    
    for i in range(0, 10):
        if form.fields[f'oSec09Field{str(i*2+1).zfill(2)}'].initial in ["oooo", None]:
            aSection09FieldShow[f"aSection09Field{str(i*2+1).zfill(2)}Show"] = "Hide"
            aSection09FieldShow[f"aSection09Field{str(i*2+2).zfill(2)}Show"] = "Hide"
    
    for i in range(0, 10):
        if form.fields[f'oSec10Field{str(i*2+1).zfill(2)}'].initial in ["oooo", None]:
            aSection10FieldShow[f"aSection10Field{str(i*2+1).zfill(2)}Show"] = "Hide"
            aSection10FieldShow[f"aSection10Field{str(i*2+2).zfill(2)}Show"] = "Hide"
    
    # print(projects)

    return render(request, "PageDataSheet.html", {
        "form": form,
        "machines": machines,
        "projects": projects,  
        "aMachineName": aMachineName,  
        "user_company": user_company,
        "sheet_key": sheet_key,
        "sheet_keys": sheet_keys,
        "machineShow": machineShow,
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
        **aSection01FieldShow,
        **aSection02FieldShow,
        **aSection03FieldShow,
        **aSection04FieldShow,
        **aSection05FieldShow,
        **aSection06FieldShow,
        **aSection07FieldShow,
        **aSection08FieldShow,
        **aSection09FieldShow,
        **aSection10FieldShow,
    })


    # Redirect after deletion (if needed)
    return redirect(reverse('PageDataSheet'))



def edit_machine(request, machine_id):
    machine = get_object_or_404(Machine, id=machine_id)  # Fetch the existing machine
    aLogEntry.objects.create(
        user=request.user,
        message=f"{request.user} Edited >>> {machine.oSec00Field03} "
    )
    instance=machine
    if request.method == "POST":
        #form = FDS_CO(request.POST)  # Bind the form with posted data
        form = FormDataSheet(data=request.POST)
        
        if form.is_valid():
            # Manually update machine fields
            machine.project = form.cleaned_data.get('project', None)
            machine.oSec01Field01 = form.cleaned_data.get('oSec01Field01', '')
            machine.oSec01Field02 = form.cleaned_data.get('oSec01Field02', '')
            machine.oSec01Field03 = form.cleaned_data.get('oSec01Field03', '')
            machine.oSec01Field04 = form.cleaned_data.get('oSec01Field04', '')
            machine.oSec01Field05 = form.cleaned_data.get('oSec01Field05', '')
            machine.oSec01Field06 = form.cleaned_data.get('oSec01Field06', '')
            machine.oSec01Field07 = form.cleaned_data.get('oSec01Field07', '')
            machine.oSec01Field08 = form.cleaned_data.get('oSec01Field08', '')
            machine.oSec01Field09 = form.cleaned_data.get('oSec01Field09', '')
            machine.oSec01Field10 = form.cleaned_data.get('oSec01Field10', '')
            machine.oSec01Field11 = form.cleaned_data.get('oSec01Field11', '')
            machine.oSec01Field12 = form.cleaned_data.get('oSec01Field12', '')
            machine.oSec01Field13 = form.cleaned_data.get('oSec01Field13', '')
            machine.oSec01Field14 = form.cleaned_data.get('oSec01Field14', '')
            machine.oSec01Field15 = form.cleaned_data.get('oSec01Field15', '')
            machine.oSec01Field16 = form.cleaned_data.get('oSec01Field16', '')
            machine.oSec01Field17 = form.cleaned_data.get('oSec01Field17', '')
            machine.oSec01Field18 = form.cleaned_data.get('oSec01Field18', '')
            machine.oSec01Field19 = form.cleaned_data.get('oSec01Field19', '')
            machine.oSec01Field20 = form.cleaned_data.get('oSec01Field20', '')

            machine.oSec02Field01 = form.cleaned_data.get('oSec02Field01', '')
            machine.oSec02Field02 = form.cleaned_data.get('oSec02Field02', '')
            machine.oSec02Field03 = form.cleaned_data.get('oSec02Field03', '')
            machine.oSec02Field04 = form.cleaned_data.get('oSec02Field04', '')
            machine.oSec02Field05 = form.cleaned_data.get('oSec02Field05', '')
            machine.oSec02Field06 = form.cleaned_data.get('oSec02Field06', '')
            machine.oSec02Field07 = form.cleaned_data.get('oSec02Field07', '')
            machine.oSec02Field08 = form.cleaned_data.get('oSec02Field08', '')
            machine.oSec02Field09 = form.cleaned_data.get('oSec02Field09', '')
            machine.oSec02Field10 = form.cleaned_data.get('oSec02Field10', '')
            machine.oSec02Field11 = form.cleaned_data.get('oSec02Field11', '')
            machine.oSec02Field12 = form.cleaned_data.get('oSec02Field12', '')
            machine.oSec02Field13 = form.cleaned_data.get('oSec02Field13', '')
            machine.oSec02Field14 = form.cleaned_data.get('oSec02Field14', '')
            machine.oSec02Field15 = form.cleaned_data.get('oSec02Field15', '')
            machine.oSec02Field16 = form.cleaned_data.get('oSec02Field16', '')
            machine.oSec02Field17 = form.cleaned_data.get('oSec02Field17', '')
            machine.oSec02Field18 = form.cleaned_data.get('oSec02Field18', '')
            machine.oSec02Field19 = form.cleaned_data.get('oSec02Field19', '')
            machine.oSec02Field20 = form.cleaned_data.get('oSec02Field20', '')

            machine.oSec03Field01 = form.cleaned_data.get('oSec03Field01', '')
            machine.oSec03Field02 = form.cleaned_data.get('oSec03Field02', '')
            machine.oSec03Field03 = form.cleaned_data.get('oSec03Field03', '')
            machine.oSec03Field04 = form.cleaned_data.get('oSec03Field04', '')
            machine.oSec03Field05 = form.cleaned_data.get('oSec03Field05', '')
            machine.oSec03Field06 = form.cleaned_data.get('oSec03Field06', '')
            machine.oSec03Field07 = form.cleaned_data.get('oSec03Field07', '')
            machine.oSec03Field08 = form.cleaned_data.get('oSec03Field08', '')
            machine.oSec03Field09 = form.cleaned_data.get('oSec03Field09', '')
            machine.oSec03Field10 = form.cleaned_data.get('oSec03Field10', '')
            machine.oSec03Field11 = form.cleaned_data.get('oSec03Field11', '')
            machine.oSec03Field12 = form.cleaned_data.get('oSec03Field12', '')
            machine.oSec03Field13 = form.cleaned_data.get('oSec03Field13', '')
            machine.oSec03Field14 = form.cleaned_data.get('oSec03Field14', '')
            machine.oSec03Field15 = form.cleaned_data.get('oSec03Field15', '')
            machine.oSec03Field16 = form.cleaned_data.get('oSec03Field16', '')
            machine.oSec03Field17 = form.cleaned_data.get('oSec03Field17', '')
            machine.oSec03Field18 = form.cleaned_data.get('oSec03Field18', '')
            machine.oSec03Field19 = form.cleaned_data.get('oSec03Field19', '')
            machine.oSec03Field20 = form.cleaned_data.get('oSec03Field20', '')

            machine.oSec04Field01 = form.cleaned_data.get('oSec04Field01', '')
            machine.oSec04Field02 = form.cleaned_data.get('oSec04Field02', '')
            machine.oSec04Field03 = form.cleaned_data.get('oSec04Field03', '')
            machine.oSec04Field04 = form.cleaned_data.get('oSec04Field04', '')
            machine.oSec04Field05 = form.cleaned_data.get('oSec04Field05', '')
            machine.oSec04Field06 = form.cleaned_data.get('oSec04Field06', '')
            machine.oSec04Field07 = form.cleaned_data.get('oSec04Field07', '')
            machine.oSec04Field08 = form.cleaned_data.get('oSec04Field08', '')
            machine.oSec04Field09 = form.cleaned_data.get('oSec04Field09', '')
            machine.oSec04Field10 = form.cleaned_data.get('oSec04Field10', '')
            machine.oSec04Field11 = form.cleaned_data.get('oSec04Field11', '')
            machine.oSec04Field12 = form.cleaned_data.get('oSec04Field12', '')
            machine.oSec04Field13 = form.cleaned_data.get('oSec04Field13', '')
            machine.oSec04Field14 = form.cleaned_data.get('oSec04Field14', '')
            machine.oSec04Field15 = form.cleaned_data.get('oSec04Field15', '')
            machine.oSec04Field16 = form.cleaned_data.get('oSec04Field16', '')
            machine.oSec04Field17 = form.cleaned_data.get('oSec04Field17', '')
            machine.oSec04Field18 = form.cleaned_data.get('oSec04Field18', '')
            machine.oSec04Field19 = form.cleaned_data.get('oSec04Field19', '')
            machine.oSec04Field20 = form.cleaned_data.get('oSec04Field20', '')

            machine.oSec05Field01 = form.cleaned_data.get('oSec05Field01', '')
            machine.oSec05Field02 = form.cleaned_data.get('oSec05Field02', '')
            machine.oSec05Field03 = form.cleaned_data.get('oSec05Field03', '')
            machine.oSec05Field04 = form.cleaned_data.get('oSec05Field04', '')
            machine.oSec05Field05 = form.cleaned_data.get('oSec05Field05', '')
            machine.oSec05Field06 = form.cleaned_data.get('oSec05Field06', '')
            machine.oSec05Field07 = form.cleaned_data.get('oSec05Field07', '')
            machine.oSec05Field08 = form.cleaned_data.get('oSec05Field08', '')
            machine.oSec05Field09 = form.cleaned_data.get('oSec05Field09', '')
            machine.oSec05Field10 = form.cleaned_data.get('oSec05Field10', '')
            machine.oSec05Field11 = form.cleaned_data.get('oSec05Field11', '')
            machine.oSec05Field12 = form.cleaned_data.get('oSec05Field12', '')
            machine.oSec05Field13 = form.cleaned_data.get('oSec05Field13', '')
            machine.oSec05Field14 = form.cleaned_data.get('oSec05Field14', '')
            machine.oSec05Field15 = form.cleaned_data.get('oSec05Field15', '')
            machine.oSec05Field16 = form.cleaned_data.get('oSec05Field16', '')
            machine.oSec05Field17 = form.cleaned_data.get('oSec05Field17', '')
            machine.oSec05Field18 = form.cleaned_data.get('oSec05Field18', '')
            machine.oSec05Field19 = form.cleaned_data.get('oSec05Field19', '')
            machine.oSec05Field20 = form.cleaned_data.get('oSec05Field20', '')

            machine.oSec06Field01 = form.cleaned_data.get('oSec06Field01', '')
            machine.oSec06Field02 = form.cleaned_data.get('oSec06Field02', '')
            machine.oSec06Field03 = form.cleaned_data.get('oSec06Field03', '')
            machine.oSec06Field04 = form.cleaned_data.get('oSec06Field04', '')
            machine.oSec06Field05 = form.cleaned_data.get('oSec06Field05', '')
            machine.oSec06Field06 = form.cleaned_data.get('oSec06Field06', '')
            machine.oSec06Field07 = form.cleaned_data.get('oSec06Field07', '')
            machine.oSec06Field08 = form.cleaned_data.get('oSec06Field08', '')
            machine.oSec06Field09 = form.cleaned_data.get('oSec06Field09', '')
            machine.oSec06Field10 = form.cleaned_data.get('oSec06Field10', '')
            machine.oSec06Field11 = form.cleaned_data.get('oSec06Field11', '')
            machine.oSec06Field12 = form.cleaned_data.get('oSec06Field12', '')
            machine.oSec06Field13 = form.cleaned_data.get('oSec06Field13', '')
            machine.oSec06Field14 = form.cleaned_data.get('oSec06Field14', '')
            machine.oSec06Field15 = form.cleaned_data.get('oSec06Field15', '')
            machine.oSec06Field16 = form.cleaned_data.get('oSec06Field16', '')
            machine.oSec06Field17 = form.cleaned_data.get('oSec06Field17', '')
            machine.oSec06Field18 = form.cleaned_data.get('oSec06Field18', '')
            machine.oSec06Field19 = form.cleaned_data.get('oSec06Field19', '')
            machine.oSec06Field20 = form.cleaned_data.get('oSec06Field20', '')

            machine.oSec07Field01 = form.cleaned_data.get('oSec07Field01', '')
            machine.oSec07Field02 = form.cleaned_data.get('oSec07Field02', '')
            machine.oSec07Field03 = form.cleaned_data.get('oSec07Field03', '')
            machine.oSec07Field04 = form.cleaned_data.get('oSec07Field04', '')
            machine.oSec07Field05 = form.cleaned_data.get('oSec07Field05', '')
            machine.oSec07Field06 = form.cleaned_data.get('oSec07Field06', '')
            machine.oSec07Field07 = form.cleaned_data.get('oSec07Field07', '')
            machine.oSec07Field08 = form.cleaned_data.get('oSec07Field08', '')
            machine.oSec07Field09 = form.cleaned_data.get('oSec07Field09', '')
            machine.oSec07Field10 = form.cleaned_data.get('oSec07Field10', '')
            machine.oSec07Field11 = form.cleaned_data.get('oSec07Field11', '')
            machine.oSec07Field12 = form.cleaned_data.get('oSec07Field12', '')
            machine.oSec07Field13 = form.cleaned_data.get('oSec07Field13', '')
            machine.oSec07Field14 = form.cleaned_data.get('oSec07Field14', '')
            machine.oSec07Field15 = form.cleaned_data.get('oSec07Field15', '')
            machine.oSec07Field16 = form.cleaned_data.get('oSec07Field16', '')
            machine.oSec07Field17 = form.cleaned_data.get('oSec07Field17', '')
            machine.oSec07Field18 = form.cleaned_data.get('oSec07Field18', '')
            machine.oSec07Field19 = form.cleaned_data.get('oSec07Field19', '')
            machine.oSec07Field20 = form.cleaned_data.get('oSec07Field20', '')

            machine.oSec08Field01 = form.cleaned_data.get('oSec08Field01', '')
            machine.oSec08Field02 = form.cleaned_data.get('oSec08Field02', '')
            machine.oSec08Field03 = form.cleaned_data.get('oSec08Field03', '')
            machine.oSec08Field04 = form.cleaned_data.get('oSec08Field04', '')
            machine.oSec08Field05 = form.cleaned_data.get('oSec08Field05', '')
            machine.oSec08Field06 = form.cleaned_data.get('oSec08Field06', '')
            machine.oSec08Field07 = form.cleaned_data.get('oSec08Field07', '')
            machine.oSec08Field08 = form.cleaned_data.get('oSec08Field08', '')
            machine.oSec08Field09 = form.cleaned_data.get('oSec08Field09', '')
            machine.oSec08Field10 = form.cleaned_data.get('oSec08Field10', '')
            machine.oSec08Field11 = form.cleaned_data.get('oSec08Field11', '')
            machine.oSec08Field12 = form.cleaned_data.get('oSec08Field12', '')
            machine.oSec08Field13 = form.cleaned_data.get('oSec08Field13', '')
            machine.oSec08Field14 = form.cleaned_data.get('oSec08Field14', '')
            machine.oSec08Field15 = form.cleaned_data.get('oSec08Field15', '')
            machine.oSec08Field16 = form.cleaned_data.get('oSec08Field16', '')
            machine.oSec08Field17 = form.cleaned_data.get('oSec08Field17', '')
            machine.oSec08Field18 = form.cleaned_data.get('oSec08Field18', '')
            machine.oSec08Field19 = form.cleaned_data.get('oSec08Field19', '')
            machine.oSec08Field20 = form.cleaned_data.get('oSec08Field20', '')

            machine.oSec09Field01 = form.cleaned_data.get('oSec09Field01', '')
            machine.oSec09Field02 = form.cleaned_data.get('oSec09Field02', '')
            machine.oSec09Field03 = form.cleaned_data.get('oSec09Field03', '')
            machine.oSec09Field04 = form.cleaned_data.get('oSec09Field04', '')
            machine.oSec09Field05 = form.cleaned_data.get('oSec09Field05', '')
            machine.oSec09Field06 = form.cleaned_data.get('oSec09Field06', '')
            machine.oSec09Field07 = form.cleaned_data.get('oSec09Field07', '')
            machine.oSec09Field08 = form.cleaned_data.get('oSec09Field08', '')
            machine.oSec09Field09 = form.cleaned_data.get('oSec09Field09', '')
            machine.oSec09Field10 = form.cleaned_data.get('oSec09Field10', '')
            machine.oSec09Field11 = form.cleaned_data.get('oSec09Field11', '')
            machine.oSec09Field12 = form.cleaned_data.get('oSec09Field12', '')
            machine.oSec09Field13 = form.cleaned_data.get('oSec09Field13', '')
            machine.oSec09Field14 = form.cleaned_data.get('oSec09Field14', '')
            machine.oSec09Field15 = form.cleaned_data.get('oSec09Field15', '')
            machine.oSec09Field16 = form.cleaned_data.get('oSec09Field16', '')
            machine.oSec09Field17 = form.cleaned_data.get('oSec09Field17', '')
            machine.oSec09Field18 = form.cleaned_data.get('oSec09Field18', '')
            machine.oSec09Field19 = form.cleaned_data.get('oSec09Field19', '')
            machine.oSec09Field20 = form.cleaned_data.get('oSec09Field20', '')

            machine.oSec10Field01 = form.cleaned_data.get('oSec10Field01', '')
            machine.oSec10Field02 = form.cleaned_data.get('oSec10Field02', '')
            machine.oSec10Field03 = form.cleaned_data.get('oSec10Field03', '')
            machine.oSec10Field04 = form.cleaned_data.get('oSec10Field04', '')
            machine.oSec10Field05 = form.cleaned_data.get('oSec10Field05', '')
            machine.oSec10Field06 = form.cleaned_data.get('oSec10Field06', '')
            machine.oSec10Field07 = form.cleaned_data.get('oSec10Field07', '')
            machine.oSec10Field08 = form.cleaned_data.get('oSec10Field08', '')
            machine.oSec10Field09 = form.cleaned_data.get('oSec10Field09', '')
            machine.oSec10Field10 = form.cleaned_data.get('oSec10Field10', '')
            machine.oSec10Field11 = form.cleaned_data.get('oSec10Field11', '')
            machine.oSec10Field12 = form.cleaned_data.get('oSec10Field12', '')
            machine.oSec10Field13 = form.cleaned_data.get('oSec10Field13', '')
            machine.oSec10Field14 = form.cleaned_data.get('oSec10Field14', '')
            machine.oSec10Field15 = form.cleaned_data.get('oSec10Field15', '')
            machine.oSec10Field16 = form.cleaned_data.get('oSec10Field16', '')
            machine.oSec10Field17 = form.cleaned_data.get('oSec10Field17', '')
            machine.oSec10Field18 = form.cleaned_data.get('oSec10Field18', '')
            machine.oSec10Field19 = form.cleaned_data.get('oSec10Field19', '')
            machine.oSec10Field20 = form.cleaned_data.get('oSec10Field20', '')

            instance.save()  # Save updates to the database
            return JsonResponse({"success": True})
        else:
            return JsonResponse({"success": False, "errors": form.errors})  # Send form validation errors

    return JsonResponse({"success": False, "error": "Invalid request"})




def DataSheetNS_get_datasheet_data(request, machine_id):
    machine = get_object_or_404(Machine, id=machine_id)
    aLogEntry.objects.create(
        user=request.user,
        message=f"{request.user} Get Data for >>> {machine.oSec00Field03} "
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



def get_user_company(request):
    if request.user.is_authenticated:
        try:
            return UserCompany.objects.get(user=request.user).company
        except UserCompany.DoesNotExist:
            return None
    return None


def is_number(value):
    try:
        float(value)
        return True
    except ValueError:
        return False
    
def resolve_fieldvalue(machine, fieldvalue):
    if is_number(fieldvalue):
        return fieldvalue

    # Loop through sections 1 to 10, and odd fields 01–19
    for sec in range(1, 11):
        for i in range(1, 21, 2):
            odd_field = f"oSec{str(sec).zfill(2)}Field{str(i).zfill(2)}"
            even_field = f"oSec{str(sec).zfill(2)}Field{str(i+1).zfill(2)}"
            if fieldvalue == getattr(machine, odd_field, None):
                return getattr(machine, even_field, fieldvalue)

    # If not found, return as-is
    return fieldvalue

# Helper function to define DXF paths
def get_dxf_paths(user_company, category, aType):
    
    company_slug = slugify(user_company.nameCompanies)

        
    dxf_name = None
    if company_slug == "aaaa":
        dxf_name = f"AAA_{category}"
    elif company_slug == "bbbb":
        dxf_name = category

    machine = AddMachine.objects.get(keyValue = aType)
    dxffile_model_name = machine.primarynameDXF
        
    if dxffile_model_name not in ["", None] :
        input_filename = f"{dxffile_model_name}.dxf"
    else :
        input_filename = f"{dxf_name}.dxf"
        
    # Load original path (base DXF)
    company_dxf_path = {
        1: os.path.join(settings.BASE_DIR, "static", "aDxfs", input_filename),
        2: os.path.join(settings.BASE_DIR, "static", "aDxfs", input_filename),
    }
    static_path = company_dxf_path.get(user_company.id)
    if not static_path or not os.path.exists(static_path):
        #raise FileNotFoundError(f"DXF not found: {static_path}")
        print(f"DXF not found: {static_path}")
    
    modified_path = static_path.replace(".dxf", "_new.dxf")

    return static_path, modified_path

# Helper function to modify DXF files
def modify_dxf_file(static_path, modified_path, modifications):
    doc = ezdxf.readfile(static_path)

    for entity in doc.modelspace().query("DIMENSION"):
        if entity.dxf.text in modifications:
            entity.dxf.text = modifications[entity.dxf.text]

        # Update text height and arrow size
        dimstyle = doc.dimstyles.get(entity.dxf.dimstyle)
        if dimstyle:
            dimstyle.dxf.dimtxt = 0.1  # Set text height
            dimstyle.dxf.dimasz = 0.1  # Set arrow size

        entity.render()

    doc.saveas(modified_path)

# Main DXF Processing Function
def process_dxf(request, aMachine_ID, category, modifications, output_filename, aType):
    # Log the request
    aLogEntry.objects.create(
        user=request.user,
        message=f"at {now()} {request.user} Download DXF {category} {aMachine_ID}"
    )

    user_company = get_user_company(request)
    if not user_company:
        return HttpResponse("Unauthorized", status=403)

    static_path, modified_path = get_dxf_paths(user_company, category, aType)
    
    if not os.path.exists(static_path):
        return HttpResponse("File not found", status=404)

    machine = Machine.objects.get(id=aMachine_ID)

    if request.method == "POST":
        modify_dxf_file(static_path, modified_path, modifications(machine))

        # Serve the modified file for download
        with open(modified_path, "rb") as dxf_file:
            response = HttpResponse(dxf_file.read(), content_type="application/dxf")
            response["Content-Disposition"] = f'attachment; filename="{output_filename}"'
            return response

    return HttpResponse("Invalid request", status=400)



# DXF Download Views


def General_DXF_ALL(request, aMachine_ID, aType):
    
    print(aType)
    
    # Redirect unauthenticated users
    if not request.user.is_authenticated:
        return redirect("login")  
    
    
    ###LOG
    aLogEntry.objects.create(
            user=request.user,
            message=f"at {now()} {request.user} DXF download {aType} "
        )
    
    themachine = AddMachine.objects.get(keyValue = aType)
    file_model_name = themachine.nameDXF
    sheetkey = aType[0:-2]

    if file_model_name not in ["", None] :
        file_name = file_model_name
    else :
        file_name = f"{sheetkey}_new"
    
    # Get the company of the logged-in user    
    user_company = None
    firstletter = None
    if request.user.is_authenticated:
        try:
            user_company = UserCompany.objects.get(user=request.user).company
            firstletter = user_company.nameCompanies[0]
        except UserCompany.DoesNotExist:
            user_company = None

    datas = DXF_data.objects.filter(sheetkey = sheetkey)
    print("Data is : ", datas)
    machine = Machine.objects.get(id=aMachine_ID)
    for d in datas:
        print(f"{d.fieldname} : {resolve_fieldvalue(machine, d.fieldvalue)}")


    return process_dxf(
        request,
        aMachine_ID,
        sheetkey,
        lambda machine: {
            data.fieldname : resolve_fieldvalue(machine, data.fieldvalue)
            for data in datas
        },
        f"{file_name}.dxf",
        aType
    )


# DXF Download Views
def FullDrawing(request, aMachine_ID, aType):
    
    # Helper function to define DXF paths
    def get_dxf_paths(user_company, category, aType):
        company_slug = slugify(user_company.nameCompanies)
        fulldrawing_dxf_name = None
        if company_slug == "aaaa":
            fulldrawing_dxf_name = f"Full Drawing {category}"
        elif company_slug == "bbbb":
            fulldrawing_dxf_name = f"BBB_Full Drawing {category}"

        machine = AddMachine.objects.get(keyValue = aType)
        fulldrawingdxffile_model_name = machine.primarynameFullDrawing
        
        if fulldrawingdxffile_model_name not in ["", None] :
            input_filename = f"{fulldrawingdxffile_model_name}.dxf"
        else :
            input_filename = f"{fulldrawing_dxf_name}.dxf"

        # Load original path (base DXF)
        company_dxf_path = {
            1: os.path.join(settings.BASE_DIR, "static", "aDxfs", input_filename),
            2: os.path.join(settings.BASE_DIR, "static", "aDxfs", input_filename),
        }
        static_path = company_dxf_path.get(user_company.id)
        if not static_path or not os.path.exists(static_path):
            #raise FileNotFoundError(f"DXF not found: {static_path}")
            print(f"Full Drawing DXF not found: {static_path}")

        modified_path = static_path.replace(".dxf", "_new.dxf")

        return static_path, modified_path
    
    # Helper function to modify DXF files
    def FullDrawing_modify_dxf_file(static_path, modified_path, modifications):
        doc = ezdxf.readfile(static_path)

        # for entity in doc.modelspace().query("DIMENSION"):
        #     if entity.dxf.text in modifications:
        #         entity.dxf.text = modifications[entity.dxf.text]

        #     # Update text height and arrow size
        #     dimstyle = doc.dimstyles.get(entity.dxf.dimstyle)
        #     if dimstyle:
        #         dimstyle.dxf.dimtxt = 0.1  # Set text height
        #         dimstyle.dxf.dimasz = 0.1  # Set arrow size

        #     entity.render()

        doc.saveas(modified_path)    
        
    
    # Main DXF Processing Function
    def FullDrawing_process_dxf(request, aMachine_ID, category, modifications, output_filename, aType):

        user_company = get_user_company(request)
        if not user_company:
            return HttpResponse("Unauthorized", status=403)

        #static_path  = os.path.join(settings.BASE_DIR, "static", "aDxfs", "AAA", "FullDrawing", f"Full Drawing {category}.dxf")
        #modified_path = static_path.replace(".dxf", "_newFullDrawing.dxf")
                
        static_path, modified_path = get_dxf_paths(user_company, category, aType)
        
        if not os.path.exists(static_path):
            return HttpResponse("File not found", status=404)

        machine = Machine.objects.get(id=aMachine_ID)

        if request.method == "POST":
            FullDrawing_modify_dxf_file(static_path, modified_path, modifications(machine))

            # Serve the modified file for download
            with open(modified_path, "rb") as dxf_file:
                response = HttpResponse(dxf_file.read(), content_type="application/dxf")
                response["Content-Disposition"] = f'attachment; filename="{output_filename}"'
                return response

        return HttpResponse("Invalid request", status=400)
        

    
    # Redirect unauthenticated users
    if not request.user.is_authenticated:
        return redirect("login") 
        
    # Get the company of the logged-in user    
    user_company = None
    firstletter = None
    if request.user.is_authenticated:
        try:
            user_company = UserCompany.objects.get(user=request.user).company
            firstletter = user_company.nameCompanies[0]
        except UserCompany.DoesNotExist:
            user_company = None 

    themachine = AddMachine.objects.get(keyValue = aType)
    file_model_name = themachine.nameFullDrawing
    sheetkey = aType[0:-2]

    if file_model_name not in ["", None] :
        file_name = file_model_name
    else :
        file_name = f"{sheetkey}_newFullDrawing"
        
    ###LOG
    aLogEntry.objects.create(
            user=request.user,
            message=f"at {now()} {request.user} DXF download {aType} "
        )
    
    datas = DXF_data.objects.filter(sheetkey = sheetkey)


    return FullDrawing_process_dxf(
        request,
        aMachine_ID,
        sheetkey,
        lambda machine: {
            data.fieldname : resolve_fieldvalue(machine, data.fieldvalue)
            for data in datas
        },
        f"{file_name}.dxf",
        aType
    )

