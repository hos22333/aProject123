from django.shortcuts import render, redirect
from .forms import formCalcMS, formCalcBC, formCalcGR, formCalcPS, formCalcTH
from .forms import formCalcMX, formCalcRT, formCalcCT, formCalcSC, formCalcBS
from .forms import formCalcNS, formCalcPNch, formCalcPNwa
from .forms import FDS_NS
from .forms import FDS_BS
from .forms import FDS_MSc
from .forms import FDS_MSf
from .forms import FDS_BC
from .forms import FDS_SC 
from .forms import FDS_CO
from .forms import FDS_GR  
from .forms import FDS_SS  
from .forms import FDS_PS  
from .forms import FDS_QV  
from .forms import FDS_TV  
from .forms import FDS_TH  
from .forms import FDS_MX 
from .forms import FDS_TA  

from datetime import datetime
from django.contrib.auth.models import User
from Apps.aApp1.models import UserRole, RoleAutho, Autho
import requests

from django.http import HttpResponse
from docx import Document
import os
import ezdxf
from django.conf import settings


from django.shortcuts import get_object_or_404
from .models import Project
from .models import Machine
from .forms import ProjectForm
from django.http import JsonResponse

from .forms import UserCompanyForm
from django.urls import reverse

from .models import aLogEntry
from django.utils.timezone import now

###################################
###################################
###################################
###################################
###################################
###################################

from django.shortcuts import get_object_or_404
from .models import FormFieldConfig
from .forms import FormFieldConfigForm



def list_configs(request):
    sort_by = request.GET.get('sort', 'id')  # Default sorting by ID
    order = request.GET.get('order', 'asc')  # Default order is ascending

    valid_fields = ['id', 'form_name', 'field_name', 'label', 'initial_value', 'visibility', 'company']
    if sort_by not in valid_fields:
        sort_by = 'id'

    # Apply sorting order
    if order == 'desc':
        sort_by = f'-{sort_by}'

    configs = FormFieldConfig.objects.all().order_by(sort_by)
    
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
###################################
###################################
###################################
###################################


# Function to load the MS page
def load_ms_page(request):
    if not request.user.is_authenticated:
        return redirect('login')  # Redirect to login page if user is not authenticated

    result = check_user_autho(request.user.username, 'MS')
    print('#####')
    print(result)
    print('######')


    form1 = formCalcMS()  # Pass DB values

    return render(request, 'MS.html', {'form1': form1})

# Function to handle form submission
def handle_ms_form(request):
    if not request.user.is_authenticated:
        return redirect('login')  # Redirect to the login page if the user is not authenticated


    if request.method == 'POST' and 'form1_submit' in request.POST:
        form1 = formCalcMS(request.POST)
        if form1.is_valid():
            # Access the cleaned_data dictionary to get individual field values
            oSec01Field01_value = form1.cleaned_data.get('oSec01Field01')
            oSec01Field02_value = form1.cleaned_data.get('oSec01Field02')
            oSec01Field03_value = form1.cleaned_data.get('oSec01Field03')
            oSec01Field04_value = form1.cleaned_data.get('oSec01Field04')
            oSec01Field05_value = form1.cleaned_data.get('oSec01Field05')
            oSec01Field06_value = form1.cleaned_data.get('oSec01Field06')
            oSec01Field07_value = form1.cleaned_data.get('oSec01Field07')
            oSec01Field08_value = form1.cleaned_data.get('oSec01Field08')
            oSec01Field09_value = form1.cleaned_data.get('oSec01Field09')
            oSec01Field10_value = form1.cleaned_data.get('oSec01Field10')
            oSec01Field11_value = form1.cleaned_data.get('oSec01Field11')

            # Calculate new values for fields            
            api_url = "https://us-central1-h1000project1.cloudfunctions.net/f01"
            req_type = "MS"  
            input_data = {
                "MS_ChannelHeight":     oSec01Field01_value,
                "MS_ScreenWidth":       oSec01Field02_value,
                "MS_BeltHeight":        oSec01Field03_value,
                "MS_WaterLevel":        oSec01Field04_value,
                "MS_BarSpacing":        oSec01Field05_value,
                "MS_BarThickness":      oSec01Field06_value,
                "MS_BarWidth":          oSec01Field07_value,
                "MS_InclinationDegree": oSec01Field08_value,
                "MS_SprocketDiameter":  oSec01Field09_value,
                "MS_Velocity":          oSec01Field10_value,
                "MS_FOS":               oSec01Field11_value,
            }

            # Call the function to interact with the API
            response = interact_with_api(api_url, req_type, input_data)
            
            oSec02Field01_result = response["MS_w"]
            oSec02Field02_result = response["MS_p"]
            oSec02Field03_result = response["MS_s"]

            # Save the form with updated values
            instance = form1.save(commit=False)  # Do not save to the database yet
            instance.oSec02Field01 = oSec02Field01_result  # Update S2field1
            instance.oSec02Field02 = oSec02Field02_result  # Update S2field2
            instance.oSec02Field03 = oSec02Field03_result  # Update S2field3
            instance.oSec00Field01 = request.user.username  # Insert username
            instance.oSec00Field02 = datetime.now().strftime('%Y-%m-%d %H:%M:%S')  # Insert current time
            instance.oSec00Field03 = "MS"  # Insert fixed type
            instance.save()  # Save to the database

            # Refresh the form with initial values to display results
            form1 = formCalcMS(initial={
                'oSec01Field01': oSec01Field01_value,
                'oSec01Field02': oSec01Field02_value,
                'oSec01Field03': oSec01Field03_value,
                'oSec01Field04': oSec01Field04_value,
                'oSec01Field05': oSec01Field05_value,
                'oSec01Field06': oSec01Field06_value,
                'oSec01Field07': oSec01Field07_value,
                'oSec01Field08': oSec01Field08_value,
                'oSec01Field09': oSec01Field09_value,
                'oSec01Field10': oSec01Field10_value,
                'oSec01Field11': oSec01Field11_value,
                'oSec02Field01': oSec02Field01_result,
                'oSec02Field02': oSec02Field02_result,
                'oSec02Field03': oSec02Field03_result,
            })

            return render(request, 'MS.html', {'form1': form1})

    return redirect('ms_load')  # Redirect to the page if the request is invalid


def generate_ms_report(request):
    
    if request.method == "POST":
        form1 = formCalcMS(request.POST)
        # Create a new Word document
        doc = Document()
        doc.add_heading('Mechanical Screen Report', level=1)

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
            ],
            "Output": [
                (form1.fields["oSec02Field01"].label, request.POST.get("oSec02Field01", "N/A")),
                (form1.fields["oSec02Field02"].label, request.POST.get("oSec02Field02", "N/A")),
                (form1.fields["oSec02Field03"].label, request.POST.get("oSec02Field03", "N/A")),
            ]
        }

        # Add form data to the Word document
        for section, fields in form_data.items():
            doc.add_heading(section, level=2)
            for field, value in fields:
                doc.add_paragraph(f"{field}: {value}")

        # Prepare the response to download the document
        response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.wordprocessingml.document')
        response['Content-Disposition'] = 'attachment; filename="Mechanical_Screen_Report.docx"'
        doc.save(response)
        return response

    return HttpResponse("Invalid request", status=400)


def modify_ms_dxf(request):
    if request.method == "POST":
        # Define the path to the DXF file in the static directory
        static_path = os.path.join(settings.BASE_DIR, "static", "aDxfs", "MS_General_Drawing.dxf")
        modified_path = os.path.join(settings.BASE_DIR, "static", "aDxfs", "modified_fileNew.dxf")

        # Load the DXF file
        doc = ezdxf.readfile(static_path)

        # Iterate over the modelspace to find all DIMENSION entities
        for entity in doc.modelspace().query("DIMENSION"):
            if entity.dxf.text == "MS_chHeight":
                entity.dxf.text = request.POST.get("oSec01Field01", "000")
            elif entity.dxf.text == "MS_chWidth":
                entity.dxf.text = request.POST.get("oSec01Field02", "000")
            elif entity.dxf.text == "BeltHeight":
                entity.dxf.text = request.POST.get("oSec01Field03", "000")
            elif entity.dxf.text == "MS_angle":
                entity.dxf.text = request.POST.get("oSec01Field08", "000")
            elif entity.dxf.text == "MS_barSpace":
                entity.dxf.text = request.POST.get("oSec01Field05", "000")
            elif entity.dxf.text == "MS_barTh":
                entity.dxf.text = request.POST.get("oSec01Field06", "000")

            # Render the dimension to apply changes
            entity.render()

        # Save the modified DXF file
        doc.saveas(modified_path)

        # Serve the modified file for download
        with open(modified_path, "rb") as dxf_file:
            response = HttpResponse(dxf_file.read(), content_type="application/dxf")
            response["Content-Disposition"] = 'attachment; filename="modified_fileNew.dxf"'
            return response

    return HttpResponse("Invalid request", status=400)




# Function to load the MS page
def load_bc_page(request):
    if not request.user.is_authenticated:
        return redirect('login')  # Redirect to the login page if the user is not authenticated

    result = check_user_autho(request.user.username, 'BC')
    print('#####')
    print(result)
    print('######')

    form1 = formCalcBC()  # Pass DB values

    return render(request, 'BC.html', {'form1': form1})

# Function to handle form submission
def handle_bc_form(request):
    if not request.user.is_authenticated:
        return redirect('login')  # Redirect to the login page if the user is not authenticated

    if request.method == 'POST' and 'form1_submit' in request.POST:
        form1 = formCalcBC(request.POST)
        if form1.is_valid():
            # Access the cleaned_data dictionary to get individual field values
            oSec01Field01_value = form1.cleaned_data.get('oSec01Field01')
            oSec01Field02_value = form1.cleaned_data.get('oSec01Field02')
            oSec01Field03_value = form1.cleaned_data.get('oSec01Field03')
            oSec01Field04_value = form1.cleaned_data.get('oSec01Field04')
            oSec01Field05_value = form1.cleaned_data.get('oSec01Field05')
            oSec01Field06_value = form1.cleaned_data.get('oSec01Field06')
            oSec01Field07_value = form1.cleaned_data.get('oSec01Field07')

            # Calculate new values for fields

            # Calculate new values for fields            
            api_url = "https://us-central1-h1000project1.cloudfunctions.net/f01"
            req_type = "BC"  
            input_data = {
                "BC_Length":     oSec01Field01_value,
                "BC_Width":       oSec01Field02_value,
                "BC_DrumDia":        oSec01Field03_value,
                "BC_Friction":        oSec01Field04_value,
                "BC_Velocity":        oSec01Field05_value,
                "BC_FOS":      oSec01Field06_value,
                "BC_Belt_weight_per_meter":      oSec01Field07_value,
            }

            # Call the function to interact with the API
            response = interact_with_api(api_url, req_type, input_data)
            
            oSec02Field01_result = response["BC_w"]
            oSec02Field02_result = response["BC_p"]
            oSec02Field03_result = response["BC_s"]

            # Save the form with updated values
            instance = form1.save(commit=False)  # Do not save to the database yet
            instance.oSec02Field01 = oSec02Field01_result  # Update S2field1
            instance.oSec02Field02 = oSec02Field02_result  # Update S2field2
            instance.oSec02Field03 = oSec02Field03_result  # Update S2field3
            instance.oSec00Field01 = request.user.username  # Insert username
            instance.oSec00Field02 = datetime.now().strftime('%Y-%m-%d %H:%M:%S')  # Insert current time
            instance.oSec00Field03 = "BC"  # Insert fixed type
            instance.save()  # Save to the database

            # Refresh the form with initial values to display results
            form1 = formCalcBC(initial={
                'oSec01Field01': oSec01Field01_value,
                'oSec01Field02': oSec01Field02_value,
                'oSec01Field03': oSec01Field03_value,
                'oSec01Field04': oSec01Field04_value,
                'oSec01Field05': oSec01Field05_value,
                'oSec01Field06': oSec01Field06_value,
                
                'oSec02Field01': oSec02Field01_result,
                'oSec02Field02': oSec02Field02_result,
                'oSec02Field03': oSec02Field03_result,
            })

            return render(request, 'BC.html', {'form1': form1})
    
    
    return redirect('bc_load')  # Redirect to the page if the request is invalid


def generate_bc_report(request):
    
    if request.method == "POST":
        form1 = formCalcBC(request.POST)
        # Create a new Word document
        doc = Document()
        doc.add_heading('Belt Conveyor Report', level=1)

        # Extract form data
        form_data = {
            "Input": [
                (form1.fields["oSec01Field01"].label, request.POST.get("oSec01Field01", "N/A")),
                (form1.fields["oSec01Field02"].label, request.POST.get("oSec01Field02", "N/A")),
                (form1.fields["oSec01Field03"].label, request.POST.get("oSec01Field03", "N/A")),
                (form1.fields["oSec01Field04"].label, request.POST.get("oSec01Field04", "N/A")),
                (form1.fields["oSec01Field05"].label, request.POST.get("oSec01Field05", "N/A")),
                (form1.fields["oSec01Field06"].label, request.POST.get("oSec01Field06", "N/A")),
            ],
            "Output": [
                (form1.fields["oSec02Field01"].label, request.POST.get("oSec02Field01", "N/A")),
                (form1.fields["oSec02Field02"].label, request.POST.get("oSec02Field02", "N/A")),
                (form1.fields["oSec02Field03"].label, request.POST.get("oSec02Field03", "N/A")),
            ]
        }

        # Add form data to the Word document
        for section, fields in form_data.items():
            doc.add_heading(section, level=2)
            for field, value in fields:
                doc.add_paragraph(f"{field}: {value}")

        # Prepare the response to download the document
        response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.wordprocessingml.document')
        response['Content-Disposition'] = 'attachment; filename="Belt_Conveyor_Report.docx"'
        doc.save(response)
        return response

    return HttpResponse("Invalid request", status=400)


def modify_bc_dxf(request):
    if request.method == "POST":
        # Define the path to the DXF file in the static directory
        static_path = os.path.join(settings.BASE_DIR, "static", "aDxfs", "BC_General_Drawing.dxf")
        modified_path = os.path.join(settings.BASE_DIR, "static", "aDxfs", "BC_General_Drawing_new.dxf")

        # Load the DXF file
        doc = ezdxf.readfile(static_path)

        # Iterate over the modelspace to find all DIMENSION entities
        for entity in doc.modelspace().query("DIMENSION"):
            if entity.dxf.text == "BC_length":
                entity.dxf.text = request.POST.get("oSec01Field01", "000")
            elif entity.dxf.text == "BC_width":
                entity.dxf.text = request.POST.get("oSec01Field02", "000")

            # Render the dimension to apply changes
            entity.render()

        # Save the modified DXF file
        doc.saveas(modified_path)

        # Serve the modified file for download
        with open(modified_path, "rb") as dxf_file:
            response = HttpResponse(dxf_file.read(), content_type="application/dxf")
            response["Content-Disposition"] = 'attachment; filename="BC_General_Drawing_new.dxf"'
            return response

    return HttpResponse("Invalid request", status=400)





# Function to load the MS page
def load_gr_page(request):
    if not request.user.is_authenticated:
        return redirect('login')  # Redirect to the login page if the user is not authenticated

    result = check_user_autho(request.user.username, 'GR')
    print('#####')
    print(result)
    print('######')

    form1 = formCalcGR()  # Pass DB values

    return render(request, 'GR.html', {'form1': form1})

# Function to handle form submission
def handle_gr_form(request):
    if not request.user.is_authenticated:
        return redirect('login')  # Redirect to the login page if the user is not authenticated

    if request.method == 'POST' and 'form1_submit' in request.POST:
        form1 = formCalcGR(request.POST)
        if form1.is_valid():
            # Access the cleaned_data dictionary to get individual field values
            oSec01Field01_value = form1.cleaned_data.get('oSec01Field01')
            oSec01Field02_value = form1.cleaned_data.get('oSec01Field02')
            oSec01Field03_value = form1.cleaned_data.get('oSec01Field03')
            oSec01Field04_value = form1.cleaned_data.get('oSec01Field04')
            oSec01Field05_value = form1.cleaned_data.get('oSec01Field05')
            oSec01Field06_value = form1.cleaned_data.get('oSec01Field06')
            oSec01Field07_value = form1.cleaned_data.get('oSec01Field07')
            oSec01Field08_value = form1.cleaned_data.get('oSec01Field08')

            # Calculate new values for fields

            # Calculate new values for fields            
            api_url = "https://us-central1-h1000project1.cloudfunctions.net/f01"
            req_type = "GR"  
            input_data = {
                "GR_n_channel":     oSec01Field01_value,
                "GR_channel_width":       oSec01Field02_value,
                "GR_civil_width":        oSec01Field03_value,
                "GR_bridge_length":        oSec01Field04_value,
                "GR_wheel_diameter":        oSec01Field05_value,
                "GR_Friction":      oSec01Field06_value,
                "GR_Velocity":      oSec01Field07_value,
                "GR_FOS":      oSec01Field08_value,
            }

            # Call the function to interact with the API
            response = interact_with_api(api_url, req_type, input_data)
            
            oSec02Field01_result = response["GR_out3"]
            oSec02Field02_result = response["GR_out1"]
            oSec02Field03_result = response["GR_out2"]
            oSec02Field04_result = response["GR_out4"]
            oSec02Field05_result = response["GR_out5"]
            oSec02Field06_result = response["GR_out6"]
            
            # Save the form with updated values
            instance = form1.save(commit=False)  # Do not save to the database yet
            instance.oSec02Field01 = oSec02Field01_result  # Update S2field1
            instance.oSec02Field02 = oSec02Field02_result  # Update S2field2
            instance.oSec02Field03 = oSec02Field03_result  # Update S2field3
            instance.oSec02Field04 = oSec02Field04_result  # Update S2field1
            instance.oSec02Field05 = oSec02Field05_result  # Update S2field2
            instance.oSec02Field06 = oSec02Field06_result  # Update S2field3
            instance.oSec00Field01 = request.user.username  # Insert username
            instance.oSec00Field02 = datetime.now().strftime('%Y-%m-%d %H:%M:%S')  # Insert current time
            instance.oSec00Field03 = "GR"  # Insert fixed type
            instance.save()  # Save to the database

            # Refresh the form with initial values to display results
            form1 = formCalcGR(initial={
                'oSec01Field01': oSec01Field01_value,
                'oSec01Field02': oSec01Field02_value,
                'oSec01Field03': oSec01Field03_value,
                'oSec01Field04': oSec01Field04_value,
                'oSec01Field05': oSec01Field05_value,
                'oSec01Field06': oSec01Field06_value,
                'oSec01Field07': oSec01Field07_value,
                'oSec01Field08': oSec01Field08_value,
                
                'oSec02Field01': oSec02Field01_result,
                'oSec02Field02': oSec02Field02_result,
                'oSec02Field03': oSec02Field03_result,
                'oSec02Field04': oSec02Field04_result,
                'oSec02Field05': oSec02Field05_result,
                'oSec02Field06': oSec02Field06_result,
            })

            return render(request, 'GR.html', {'form1': form1})
    
    
    return redirect('gr_load')  # Redirect to the page if the request is invalid


def generate_gr_report(request):
    
    if request.method == "POST":
        form1 = formCalcGR(request.POST)
        # Create a new Word document
        doc = Document()
        doc.add_heading('Gritremoval Report', level=1)

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
            ],
            "Output": [
                (form1.fields["oSec02Field01"].label, request.POST.get("oSec02Field01", "N/A")),
                (form1.fields["oSec02Field02"].label, request.POST.get("oSec02Field02", "N/A")),
                (form1.fields["oSec02Field03"].label, request.POST.get("oSec02Field03", "N/A")),
                (form1.fields["oSec02Field04"].label, request.POST.get("oSec02Field04", "N/A")),
                (form1.fields["oSec02Field05"].label, request.POST.get("oSec02Field05", "N/A")),
                (form1.fields["oSec02Field06"].label, request.POST.get("oSec02Field06", "N/A")),
            ]
        }

        # Add form data to the Word document
        for section, fields in form_data.items():
            doc.add_heading(section, level=2)
            for field, value in fields:
                doc.add_paragraph(f"{field}: {value}")

        # Prepare the response to download the document
        response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.wordprocessingml.document')
        response['Content-Disposition'] = 'attachment; filename="Gritremoval_Report.docx"'
        doc.save(response)
        return response

    return HttpResponse("Invalid request", status=400)


def modify_gr_dxf(request):
    if request.method == "POST":
        # Define the path to the DXF file in the static directory
        static_path = os.path.join(settings.BASE_DIR, "static", "aDxfs", "MS_DXF_B.dxf")
        modified_path = os.path.join(settings.BASE_DIR, "static", "aDxfs", "modified_file.dxf")

        # Load the DXF file
        doc = ezdxf.readfile(static_path)

        # Iterate over the modelspace to find all DIMENSION entities
        for entity in doc.modelspace().query("DIMENSION"):
            if entity.dxf.text == "CHH111":
                entity.dxf.text = request.POST.get("oSec01Field01", "000")
            elif entity.dxf.text == "CHW111":
                entity.dxf.text = request.POST.get("oSec01Field02", "000")
            elif entity.dxf.text == "BeltHeight":
                entity.dxf.text = request.POST.get("oSec01Field03", "000")
            elif entity.dxf.text == "DEG111":
                entity.dxf.text = request.POST.get("oSec01Field08", "000")

            # Render the dimension to apply changes
            entity.render()

        # Save the modified DXF file
        doc.saveas(modified_path)

        # Serve the modified file for download
        with open(modified_path, "rb") as dxf_file:
            response = HttpResponse(dxf_file.read(), content_type="application/dxf")
            response["Content-Disposition"] = 'attachment; filename="modified_file.dxf"'
            return response

    return HttpResponse("Invalid request", status=400)






# Function to load the MS page
def load_ps_page(request):
    if not request.user.is_authenticated:
        return redirect('login')  # Redirect to the login page if the user is not authenticated

    result = check_user_autho(request.user.username, 'PS')
    print('#####')
    print(result)
    print('######')

    form1 = formCalcPS() 
    return render(request, 'PS.html', {'form1': form1})

# Function to handle form submission
def handle_ps_form(request):
    if not request.user.is_authenticated:
        return redirect('login')  # Redirect to the login page if the user is not authenticated

    if request.method == 'POST' and 'form1_submit' in request.POST:
        form1 = formCalcPS(request.POST)
        if form1.is_valid():
            # Access the cleaned_data dictionary to get individual field values
            oSec01Field01_value = form1.cleaned_data.get('oSec01Field01')
            oSec01Field02_value = form1.cleaned_data.get('oSec01Field02')
            oSec01Field03_value = form1.cleaned_data.get('oSec01Field03')
            oSec01Field04_value = form1.cleaned_data.get('oSec01Field04')

            # Calculate new values for fields

            # Calculate new values for fields            
            api_url = "https://us-central1-h1000project1.cloudfunctions.net/f01"
            req_type = "PS"  
            input_data = {
                "PS_walkway_length":     oSec01Field01_value,
                "PS_Friction":       oSec01Field02_value,
                "PS_Velocity":        oSec01Field03_value,
                "PS_FOS":        oSec01Field04_value,
            }

            # Call the function to interact with the API
            response = interact_with_api(api_url, req_type, input_data)
            
            oSec02Field01_result = response["PS_out2"]
            oSec02Field02_result = response["PS_out1"]
            oSec02Field03_result = '000'
            oSec02Field04_result = response["PS_out3"]
            oSec02Field05_result = response["PS_out4"]
            
            # Save the form with updated values
            instance = form1.save(commit=False)  # Do not save to the database yet
            instance.oSec02Field01 = oSec02Field01_result  # Update S2field1
            instance.oSec02Field02 = oSec02Field02_result  # Update S2field2
            instance.oSec02Field03 = oSec02Field03_result  # Update S2field3
            instance.oSec02Field04 = oSec02Field04_result  # Update S2field1
            instance.oSec00Field01 = request.user.username  # Insert username
            instance.oSec00Field02 = datetime.now().strftime('%Y-%m-%d %H:%M:%S')  # Insert current time
            instance.oSec00Field03 = "PS"  # Insert fixed type
            instance.save()  # Save to the database

            # Refresh the form with initial values to display results
            form1 = formCalcPS(initial={
                'oSec01Field01': oSec01Field01_value,
                'oSec01Field02': oSec01Field02_value,
                'oSec01Field03': oSec01Field03_value,
                'oSec01Field04': oSec01Field04_value,
                
                'oSec02Field01': oSec02Field01_result,
                'oSec02Field02': oSec02Field02_result,
                'oSec02Field03': oSec02Field03_result,
                'oSec02Field04': oSec02Field04_result,
                'oSec02Field05': oSec02Field05_result,
            })

            return render(request, 'PS.html', {'form1': form1})
    
    
    return redirect('ps_load')  # Redirect to the page if the request is invalid



def generate_ps_report(request):
    
    if request.method == "POST":
        form1 = formCalcPS(request.POST)
        # Create a new Word document
        doc = Document()
        doc.add_heading('PST Report', level=1)

        # Extract form data
        form_data = {
            "Input": [
                (form1.fields["oSec01Field01"].label, request.POST.get("oSec01Field01", "N/A")),
                (form1.fields["oSec01Field02"].label, request.POST.get("oSec01Field02", "N/A")),
                (form1.fields["oSec01Field03"].label, request.POST.get("oSec01Field03", "N/A")),
                (form1.fields["oSec01Field04"].label, request.POST.get("oSec01Field04", "N/A")),
            ],
            "Output": [
                (form1.fields["oSec02Field01"].label, request.POST.get("oSec02Field01", "N/A")),
                (form1.fields["oSec02Field02"].label, request.POST.get("oSec02Field02", "N/A")),
                (form1.fields["oSec02Field03"].label, request.POST.get("oSec02Field03", "N/A")),
                (form1.fields["oSec02Field04"].label, request.POST.get("oSec02Field04", "N/A")),
                (form1.fields["oSec02Field05"].label, request.POST.get("oSec02Field05", "N/A")),
            ]
        }

        # Add form data to the Word document
        for section, fields in form_data.items():
            doc.add_heading(section, level=2)
            for field, value in fields:
                doc.add_paragraph(f"{field}: {value}")

        # Prepare the response to download the document
        response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.wordprocessingml.document')
        response['Content-Disposition'] = 'attachment; filename="PST_Report.docx"'
        doc.save(response)
        return response

    return HttpResponse("Invalid request", status=400)


def modify_ps_dxf(request):
    if request.method == "POST":
        # Define the path to the DXF file in the static directory
        static_path = os.path.join(settings.BASE_DIR, "static", "aDxfs", "PS_General_Drawing.dxf")
        modified_path = os.path.join(settings.BASE_DIR, "static", "aDxfs", "PS_General_Drawing_new.dxf")

        # Load the DXF file
        doc = ezdxf.readfile(static_path)

        # Iterate over the modelspace to find all DIMENSION entities
        for entity in doc.modelspace().query("DIMENSION"):
            if entity.dxf.text == "PS_walkwayLength":
                entity.dxf.text = request.POST.get("oSec01Field01", "000")

            # Render the dimension to apply changes
            entity.render()

        # Save the modified DXF file
        doc.saveas(modified_path)

        # Serve the modified file for download
        with open(modified_path, "rb") as dxf_file:
            response = HttpResponse(dxf_file.read(), content_type="application/dxf")
            response["Content-Disposition"] = 'attachment; filename="PS_General_Drawing_new.dxf"'
            return response

    return HttpResponse("Invalid request", status=400)




def load_th_page(request):
    if not request.user.is_authenticated:
        return redirect('login')  # Redirect to the login page if the user is not authenticated

    result = check_user_autho(request.user.username, 'TH')
    print('#####')
    print(result)
    print('######')

    form1 = formCalcTH() 
    
    return render(request, 'TH.html', {'form1': form1})

# Function to handle form submission
def handle_th_form(request):
    if not request.user.is_authenticated:
        return redirect('login')  # Redirect to the login page if the user is not authenticated

    if request.method == 'POST' and 'form1_submit' in request.POST:
        form1 = formCalcTH(request.POST)
        if form1.is_valid():
            # Access the cleaned_data dictionary to get individual field values
            oSec01Field01_value = form1.cleaned_data.get('oSec01Field01')
            oSec01Field02_value = form1.cleaned_data.get('oSec01Field02')
            oSec01Field03_value = form1.cleaned_data.get('oSec01Field03')
            oSec01Field04_value = form1.cleaned_data.get('oSec01Field04')
            oSec01Field05_value = form1.cleaned_data.get('oSec01Field05')
            oSec01Field06_value = form1.cleaned_data.get('oSec01Field06')
            oSec01Field07_value = form1.cleaned_data.get('oSec01Field07')
            oSec01Field08_value = form1.cleaned_data.get('oSec01Field08')

            # Calculate new values for fields

            # Calculate new values for fields            
            api_url = "https://us-central1-h1000project1.cloudfunctions.net/f01"
            req_type = "TH"  
            input_data = {
                "TH_diameter":     oSec01Field01_value,
                "TH_n_arm":       oSec01Field02_value,
                "TH_Velocity":        oSec01Field03_value,
                "TH_FOS":        oSec01Field04_value,
            }

            # Call the function to interact with the API
            response = interact_with_api(api_url, req_type, input_data)
            
            oSec02Field01_result = response["TH_w"]
            oSec02Field02_result = response["TH_p"]
            oSec02Field03_result = response["TH_s"]
            
            # Save the form with updated values
            instance = form1.save(commit=False)  # Do not save to the database yet
            instance.oSec02Field01 = oSec02Field01_result  # Update S2field1
            instance.oSec02Field02 = oSec02Field02_result  # Update S2field1
            instance.oSec02Field03 = oSec02Field03_result  # Update S2field1
            instance.oSec00Field01 = request.user.username  # Insert username
            instance.oSec00Field02 = datetime.now().strftime('%Y-%m-%d %H:%M:%S')  # Insert current time
            instance.oSec00Field03 = "TH"  # Insert fixed type
            instance.save()  # Save to the database

            # Refresh the form with initial values to display results
            form1 = formCalcTH(initial={
                'oSec01Field01': oSec01Field01_value,
                'oSec01Field02': oSec01Field02_value,
                'oSec01Field03': oSec01Field03_value,
                'oSec01Field04': oSec01Field04_value,
                'oSec01Field05': oSec01Field05_value,
                'oSec01Field06': oSec01Field06_value,
                'oSec01Field07': oSec01Field07_value,
                'oSec01Field08': oSec01Field08_value,
                
                'oSec02Field01': oSec02Field01_result,
                'oSec02Field02': oSec02Field02_result,
                'oSec02Field03': oSec02Field03_result,
            })

            return render(request, 'TH.html', {'form1': form1})
    
    
    return redirect('th_load')  # Redirect to the page if the request is invalid



def generate_th_report(request):
    
    if request.method == "POST":
        form1 = formCalcTH(request.POST)
        # Create a new Word document
        doc = Document()
        doc.add_heading('Thickener Report', level=1)

        # Extract form data
        form_data = {
            "Input": [
                (form1.fields["oSec01Field01"].label, request.POST.get("oSec01Field01", "N/A")),
                (form1.fields["oSec01Field02"].label, request.POST.get("oSec01Field02", "N/A")),
                (form1.fields["oSec01Field03"].label, request.POST.get("oSec01Field03", "N/A")),
                (form1.fields["oSec01Field04"].label, request.POST.get("oSec01Field04", "N/A")),
            ],
            "Output": [
                (form1.fields["oSec02Field01"].label, request.POST.get("oSec02Field01", "N/A")),
                (form1.fields["oSec02Field02"].label, request.POST.get("oSec02Field02", "N/A")),
                (form1.fields["oSec02Field03"].label, request.POST.get("oSec02Field03", "N/A")),
                (form1.fields["oSec02Field04"].label, request.POST.get("oSec02Field04", "N/A")),
                (form1.fields["oSec02Field05"].label, request.POST.get("oSec02Field05", "N/A")),
            ]
        }

        # Add form data to the Word document
        for section, fields in form_data.items():
            doc.add_heading(section, level=2)
            for field, value in fields:
                doc.add_paragraph(f"{field}: {value}")

        # Prepare the response to download the document
        response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.wordprocessingml.document')
        response['Content-Disposition'] = 'attachment; filename="Thickener_Report.docx"'
        doc.save(response)
        return response

    return HttpResponse("Invalid request", status=400)


def modify_th_dxf(request):
    if request.method == "POST":
        # Define the path to the DXF file in the static directory
        static_path = os.path.join(settings.BASE_DIR, "static", "aDxfs", "TH_General_Drawing.dxf")
        modified_path = os.path.join(settings.BASE_DIR, "static", "aDxfs", "TH_General_Drawing_new.dxf")

        # Load the DXF file
        doc = ezdxf.readfile(static_path)

        # Iterate over the modelspace to find all DIMENSION entities
        for entity in doc.modelspace().query("DIMENSION"):
            if entity.dxf.text == "TH_dia":
                entity.dxf.text = request.POST.get("oSec01Field01", "000")

            # Render the dimension to apply changes
            entity.render()

        # Save the modified DXF file
        doc.saveas(modified_path)

        # Serve the modified file for download
        with open(modified_path, "rb") as dxf_file:
            response = HttpResponse(dxf_file.read(), content_type="application/dxf")
            response["Content-Disposition"] = 'attachment; filename="TH_General_Drawing_new.dxf"'
            return response

    return HttpResponse("Invalid request", status=400)





# Function to load the MS page
def load_mx_page(request):
    if not request.user.is_authenticated:
        return redirect('login')  # Redirect to the login page if the user is not authenticated

    result = check_user_autho(request.user.username, 'MX')
    print('#####')
    print(result)
    print('######')

    form1 = formCalcMX()
    
    return render(request, 'MX.html', {'form1': form1})

# Function to handle form submission
def handle_mx_form(request):
    if not request.user.is_authenticated:
        return redirect('login')  # Redirect to the login page if the user is not authenticated

    if request.method == 'POST' and 'form1_submit' in request.POST:
        print('qqqqqqqq')
        form1 = formCalcMX(request.POST)        
        print('qqqqqqqq')
        if form1.is_valid():                   
            print('qqqqqqqq')
            # Access the cleaned_data dictionary to get individual field values
            oSec01Field01_value = form1.cleaned_data.get('oSec01Field01')
            oSec01Field02_value = form1.cleaned_data.get('oSec01Field02')
            oSec01Field03_value = form1.cleaned_data.get('oSec01Field03')
            oSec01Field04_value = form1.cleaned_data.get('oSec01Field04')
            oSec01Field05_value = form1.cleaned_data.get('oSec01Field05')
            oSec01Field06_value = form1.cleaned_data.get('oSec01Field06')
            oSec01Field07_value = form1.cleaned_data.get('oSec01Field07')
            oSec01Field08_value = form1.cleaned_data.get('oSec01Field08')
                   
            print('qqqqqqqq')

            # Calculate new values for fields

            # Calculate new values for fields            
            api_url = "https://us-central1-h1000project1.cloudfunctions.net/f01"
            req_type = "MX"  
            input_data = {
                "MX_length":        oSec01Field01_value,
                "MX_width":         oSec01Field02_value,
                "MX_water_depth":           oSec01Field03_value,
                "MX_tank_depth":            oSec01Field04_value,
                "MX_impeller_coefficient":  oSec01Field05_value,
                "MX_velocity_gradient":     oSec01Field06_value,
                "MX_impeller_diameter_factor":  oSec01Field07_value,
                "MX_safety_factor":             oSec01Field08_value,
            }

            # Call the function to interact with the API
            response = interact_with_api(api_url, req_type, input_data)
            
            oSec02Field01_result = '000'
            oSec02Field02_result = response["MX_p"]
            oSec02Field03_result = response["MX_s"]
            oSec02Field04_result = response["MX_d"]
            oSec02Field05_result = response["MX_shaftL"]
            oSec02Field06_result = response["MX_shaftD"]
            oSec02Field07_result = response["MX_Type"]

            # Save the form with updated values
            instance = form1.save(commit=False)  # Do not save to the database yet
            instance.oSec02Field01 = oSec02Field01_result  # Update S2field1
            instance.oSec00Field01 = request.user.username  # Insert username
            instance.oSec00Field02 = datetime.now().strftime('%Y-%m-%d %H:%M:%S')  # Insert current time
            instance.oSec00Field03 = "MX"  # Insert fixed type
            instance.save()  # Save to the database

            # Refresh the form with initial values to display results
            form1 = formCalcMX(initial={
                'oSec01Field01': oSec01Field01_value,
                'oSec01Field02': oSec01Field02_value,
                'oSec01Field03': oSec01Field03_value,
                'oSec01Field04': oSec01Field04_value,
                'oSec01Field05': oSec01Field05_value,
                'oSec01Field06': oSec01Field06_value,
                'oSec01Field07': oSec01Field07_value,
                'oSec01Field08': oSec01Field08_value,
                
                'oSec02Field01': oSec02Field01_result,
                'oSec02Field02': oSec02Field02_result,
                'oSec02Field03': oSec02Field03_result,
                'oSec02Field04': oSec02Field04_result,
                'oSec02Field05': oSec02Field05_result,
                'oSec02Field06': oSec02Field06_result,
                'oSec02Field07': oSec02Field07_result,
            })

            return render(request, 'MX.html', {'form1': form1})
    
    
    return redirect('mx_load')  # Redirect to the page if the request is invalid



def generate_mx_report(request):
    
    if request.method == "POST":
        form1 = formCalcMX(request.POST)
        # Create a new Word document
        doc = Document()
        doc.add_heading('Mixer Report', level=1)

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
            ],
            "Output": [
                (form1.fields["oSec02Field01"].label, request.POST.get("oSec02Field01", "N/A")),
                (form1.fields["oSec02Field02"].label, request.POST.get("oSec02Field02", "N/A")),
                (form1.fields["oSec02Field03"].label, request.POST.get("oSec02Field03", "N/A")),
                (form1.fields["oSec02Field04"].label, request.POST.get("oSec02Field04", "N/A")),
                (form1.fields["oSec02Field05"].label, request.POST.get("oSec02Field05", "N/A")),
                (form1.fields["oSec02Field06"].label, request.POST.get("oSec02Field06", "N/A")),
                (form1.fields["oSec02Field07"].label, request.POST.get("oSec02Field07", "N/A")),
            ]
        }

        # Add form data to the Word document
        for section, fields in form_data.items():
            doc.add_heading(section, level=2)
            for field, value in fields:
                doc.add_paragraph(f"{field}: {value}")

        # Prepare the response to download the document
        response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.wordprocessingml.document')
        response['Content-Disposition'] = 'attachment; filename="Mixer_Report.docx"'
        doc.save(response)
        return response

    return HttpResponse("Invalid request", status=400)


def modify_mx_dxf(request):
    if request.method == "POST":
        # Define the path to the DXF file in the static directory
        static_path = os.path.join(settings.BASE_DIR, "static", "aDxfs", "MS_DXF_B.dxf")
        modified_path = os.path.join(settings.BASE_DIR, "static", "aDxfs", "modified_file.dxf")

        # Load the DXF file
        doc = ezdxf.readfile(static_path)

        # Iterate over the modelspace to find all DIMENSION entities
        for entity in doc.modelspace().query("DIMENSION"):
            if entity.dxf.text == "CHH111":
                entity.dxf.text = request.POST.get("oSec01Field01", "000")
            elif entity.dxf.text == "CHW111":
                entity.dxf.text = request.POST.get("oSec01Field02", "000")
            elif entity.dxf.text == "BeltHeight":
                entity.dxf.text = request.POST.get("oSec01Field03", "000")
            elif entity.dxf.text == "DEG111":
                entity.dxf.text = request.POST.get("oSec01Field08", "000")

            # Render the dimension to apply changes
            entity.render()

        # Save the modified DXF file
        doc.saveas(modified_path)

        # Serve the modified file for download
        with open(modified_path, "rb") as dxf_file:
            response = HttpResponse(dxf_file.read(), content_type="application/dxf")
            response["Content-Disposition"] = 'attachment; filename="modified_file.dxf"'
            return response

    return HttpResponse("Invalid request", status=400)




def load_rt_page(request):
    if not request.user.is_authenticated:
        return redirect('login')  # Redirect to the login page if the user is not authenticated

    result = check_user_autho(request.user.username, 'RT')
    print('#####')
    print(result)
    print('######')

    form1 = formCalcRT()  
    
    return render(request, 'RT.html', {'form1': form1})

# Function to handle form submission
def handle_rt_form(request):
    if not request.user.is_authenticated:
        return redirect('login')  # Redirect to the login page if the user is not authenticated

    if request.method == 'POST' and 'form1_submit' in request.POST:
        form1 = formCalcRT(request.POST)
        if form1.is_valid():
            # Access the cleaned_data dictionary to get individual field values
            oSec01Field01_value = form1.cleaned_data.get('oSec01Field01')
            oSec01Field02_value = form1.cleaned_data.get('oSec01Field02')
            oSec01Field03_value = form1.cleaned_data.get('oSec01Field03')
            oSec01Field04_value = form1.cleaned_data.get('oSec01Field04')
            oSec01Field05_value = form1.cleaned_data.get('oSec01Field05')
            oSec01Field06_value = form1.cleaned_data.get('oSec01Field06')
            oSec01Field07_value = form1.cleaned_data.get('oSec01Field07')
            oSec01Field08_value = form1.cleaned_data.get('oSec01Field08')

            # Calculate new values for fields

            # Calculate new values for fields            
            api_url = "https://us-central1-h1000project1.cloudfunctions.net/f01"
            req_type = "RT"  
            input_data = {
                "RT_Length":        oSec01Field01_value,
                "RT_Width":         oSec01Field02_value,
                "RT_Hight":           oSec01Field03_value,
                "RT_ShellTH":            oSec01Field04_value,
                "RT_BaseTH":    oSec01Field05_value,
                "RT_N_Spliter":     oSec01Field06_value,
            }

            # Call the function to interact with the API
            response = interact_with_api(api_url, req_type, input_data)
            
            oSec02Field01_result = response["RT_w10"]

            # Save the form with updated values
            instance = form1.save(commit=False)  # Do not save to the database yet
            instance.oSec02Field01 = oSec02Field01_result  # Update S2field1
            instance.oSec00Field01 = request.user.username  # Insert username
            instance.oSec00Field02 = datetime.now().strftime('%Y-%m-%d %H:%M:%S')  # Insert current time
            instance.oSec00Field03 = "RT"  # Insert fixed type
            instance.save()  # Save to the database

            # Refresh the form with initial values to display results
            form1 = formCalcRT(initial={
                'oSec01Field01': oSec01Field01_value,
                'oSec01Field02': oSec01Field02_value,
                'oSec01Field03': oSec01Field03_value,
                'oSec01Field04': oSec01Field04_value,
                'oSec01Field05': oSec01Field05_value,
                'oSec01Field06': oSec01Field06_value,
                'oSec01Field07': oSec01Field07_value,
                'oSec01Field08': oSec01Field08_value,
                
                'oSec02Field01': oSec02Field01_result,
            })

            return render(request, 'RT.html', {'form1': form1})
    
    
    return redirect('rt_load')  # Redirect to the page if the request is invalid


def generate_rt_report(request):
    
    if request.method == "POST":
        form1 = formCalcRT(request.POST)
        # Create a new Word document
        doc = Document()
        doc.add_heading('Rect Tanks Report', level=1)

        # Extract form data
        form_data = {
            "Input": [
                (form1.fields["oSec01Field01"].label, request.POST.get("oSec01Field01", "N/A")),
                (form1.fields["oSec01Field02"].label, request.POST.get("oSec01Field02", "N/A")),
                (form1.fields["oSec01Field03"].label, request.POST.get("oSec01Field03", "N/A")),
                (form1.fields["oSec01Field04"].label, request.POST.get("oSec01Field04", "N/A")),
                (form1.fields["oSec01Field05"].label, request.POST.get("oSec01Field05", "N/A")),
                (form1.fields["oSec01Field06"].label, request.POST.get("oSec01Field06", "N/A")),
            ],
            "Output": [
                (form1.fields["oSec02Field01"].label, request.POST.get("oSec02Field01", "N/A")),
            ]
        }

        # Add form data to the Word document
        for section, fields in form_data.items():
            doc.add_heading(section, level=2)
            for field, value in fields:
                doc.add_paragraph(f"{field}: {value}")

        # Prepare the response to download the document
        response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.wordprocessingml.document')
        response['Content-Disposition'] = 'attachment; filename="Rect_Tank_Report.docx"'
        doc.save(response)
        return response

    return HttpResponse("Invalid request", status=400)


def modify_rt_dxf(request):
    if request.method == "POST":
        # Define the path to the DXF file in the static directory
        static_path = os.path.join(settings.BASE_DIR, "static", "aDxfs", "MS_DXF_B.dxf")
        modified_path = os.path.join(settings.BASE_DIR, "static", "aDxfs", "modified_file.dxf")

        # Load the DXF file
        doc = ezdxf.readfile(static_path)

        # Iterate over the modelspace to find all DIMENSION entities
        for entity in doc.modelspace().query("DIMENSION"):
            if entity.dxf.text == "CHH111":
                entity.dxf.text = request.POST.get("oSec01Field01", "000")
            elif entity.dxf.text == "CHW111":
                entity.dxf.text = request.POST.get("oSec01Field02", "000")
            elif entity.dxf.text == "BeltHeight":
                entity.dxf.text = request.POST.get("oSec01Field03", "000")
            elif entity.dxf.text == "DEG111":
                entity.dxf.text = request.POST.get("oSec01Field08", "000")

            # Render the dimension to apply changes
            entity.render()

        # Save the modified DXF file
        doc.saveas(modified_path)

        # Serve the modified file for download
        with open(modified_path, "rb") as dxf_file:
            response = HttpResponse(dxf_file.read(), content_type="application/dxf")
            response["Content-Disposition"] = 'attachment; filename="modified_file.dxf"'
            return response

    return HttpResponse("Invalid request", status=400)






# Function to load the MS page
def load_ct_page(request):
    if not request.user.is_authenticated:
        return redirect('login')  # Redirect to the login page if the user is not authenticated

    result = check_user_autho(request.user.username, 'CT')
    print('#####')
    print(result)
    print('######')

    form1 = formCalcCT()  
    
    return render(request, 'PageCT.html', {'form1': form1})


# Function to handle form submission
def handle_ct_form(request):
    if not request.user.is_authenticated:
        return redirect('login')  # Redirect to the login page if the user is not authenticated

    if request.method == 'POST' and 'form1_submit' in request.POST:
        print("111")
        form1 = formCalcCT(request.POST)
        if form1.is_valid():
            print("222")
            # Access the cleaned_data dictionary to get individual field values
            oSec01Field01_value = form1.cleaned_data.get('oSec01Field01')
            oSec01Field02_value = form1.cleaned_data.get('oSec01Field02')

            # Calculate new values for fields

            # Calculate new values for fields            
            api_url = "https://us-central1-h1000project1.cloudfunctions.net/f01"
            req_type = "CT"  
            input_data = {
                "CT_Diameter":        oSec01Field01_value,
                "CT_Height":         oSec01Field02_value,
            }

            # Call the function to interact with the API
            response = interact_with_api(api_url, req_type, input_data)
            
            oSec02Field01_result = response["O_Tank_Weight"]
            oSec02Field02_result = response["O_Tank_Volume"]
            oSec02Field03_result = response["O_Tank_Shell_Th"]
            oSec02Field04_result = response["O_Tank_Base_Th"]
            oSec02Field05_result = response["O_Tank_Shell_Weight"]
            oSec02Field06_result = response["O_Tank_Base_Weight"]
            oSec02Field07_result = response["O_Tank_Base_UPN_Weight"]
            oSec02Field08_result = response["O_Tank_Cover_Weight"]

            # Save the form with updated values
            instance = form1.save(commit=False)  # Do not save to the database yet
            instance.oSec02Field01 = oSec02Field01_result  # Update S2field1
            instance.oSec02Field02 = oSec02Field02_result  # Update S2field1
            instance.oSec02Field03 = oSec02Field03_result  # Update S2field1
            instance.oSec02Field04 = oSec02Field04_result  # Update S2field1
            instance.oSec02Field05 = oSec02Field05_result  # Update S2field1
            instance.oSec02Field06 = oSec02Field06_result  # Update S2field1
            instance.oSec02Field07 = oSec02Field07_result  # Update S2field1
            instance.oSec02Field08 = oSec02Field08_result  # Update S2field1
            
            instance.oSec00Field01 = request.user.username  # Insert username
            instance.oSec00Field02 = datetime.now().strftime('%Y-%m-%d %H:%M:%S')  # Insert current time
            instance.oSec00Field03 = "CT"  # Insert fixed type
            instance.save()  # Save to the database

            # Refresh the form with initial values to display results
            form1 = formCalcCT(initial={
                'oSec01Field01': oSec01Field01_value,
                'oSec01Field02': oSec01Field02_value,
                
                'oSec02Field01': oSec02Field01_result,
                'oSec02Field02': oSec02Field02_result,
                'oSec02Field03': oSec02Field03_result,
                'oSec02Field04': oSec02Field04_result,
                'oSec02Field05': oSec02Field05_result,
                'oSec02Field06': oSec02Field06_result,
                'oSec02Field07': oSec02Field07_result,
                'oSec02Field08': oSec02Field08_result,
            })

            return render(request, 'PageCT.html', {'form1': form1})
    
    
    return redirect('ct_load')  # Redirect to the page if the request is invalid


def generate_ct_report(request):
    
    if request.method == "POST":
        form1 = formCalcCT(request.POST)
        # Create a new Word document
        doc = Document()
        doc.add_heading('Circular Tanks Report', level=1)

        # Extract form data
        form_data = {
            "Input": [
                (form1.fields["oSec01Field01"].label, request.POST.get("oSec01Field01", "N/A")),
                (form1.fields["oSec01Field02"].label, request.POST.get("oSec01Field02", "N/A")),
            ],
            "Output": [
                (form1.fields["oSec02Field01"].label, request.POST.get("oSec02Field01", "N/A")),
                (form1.fields["oSec02Field02"].label, request.POST.get("oSec02Field02", "N/A")),
                (form1.fields["oSec02Field03"].label, request.POST.get("oSec02Field03", "N/A")),
                (form1.fields["oSec02Field04"].label, request.POST.get("oSec02Field04", "N/A")),
                (form1.fields["oSec02Field05"].label, request.POST.get("oSec02Field05", "N/A")),
                (form1.fields["oSec02Field06"].label, request.POST.get("oSec02Field06", "N/A")),
                (form1.fields["oSec02Field07"].label, request.POST.get("oSec02Field07", "N/A")),
            ]
        }

        # Add form data to the Word document
        for section, fields in form_data.items():
            doc.add_heading(section, level=2)
            for field, value in fields:
                doc.add_paragraph(f"{field}: {value}")

        # Prepare the response to download the document
        response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.wordprocessingml.document')
        response['Content-Disposition'] = 'attachment; filename="Circular_Tank_Report.docx"'
        doc.save(response)
        return response

    return HttpResponse("Invalid request", status=400)


def modify_ct_dxf(request):
    if request.method == "POST":
        # Define the path to the DXF file in the static directory
        static_path = os.path.join(settings.BASE_DIR, "static", "aDxfs", "MS_DXF_B.dxf")
        modified_path = os.path.join(settings.BASE_DIR, "static", "aDxfs", "modified_file.dxf")

        # Load the DXF file
        doc = ezdxf.readfile(static_path)

        # Iterate over the modelspace to find all DIMENSION entities
        for entity in doc.modelspace().query("DIMENSION"):
            if entity.dxf.text == "CHH111":
                entity.dxf.text = request.POST.get("oSec01Field01", "000")
            elif entity.dxf.text == "CHW111":
                entity.dxf.text = request.POST.get("oSec01Field02", "000")
            elif entity.dxf.text == "BeltHeight":
                entity.dxf.text = request.POST.get("oSec01Field03", "000")
            elif entity.dxf.text == "DEG111":
                entity.dxf.text = request.POST.get("oSec01Field08", "000")

            # Render the dimension to apply changes
            entity.render()

        # Save the modified DXF file
        doc.saveas(modified_path)

        # Serve the modified file for download
        with open(modified_path, "rb") as dxf_file:
            response = HttpResponse(dxf_file.read(), content_type="application/dxf")
            response["Content-Disposition"] = 'attachment; filename="modified_file.dxf"'
            return response

    return HttpResponse("Invalid request", status=400)

    
    
    
    
    
    
    

# Function to load the MS page
def load_sc_page(request):
    if not request.user.is_authenticated:
        return redirect('login')  # Redirect to the login page if the user is not authenticated

    result = check_user_autho(request.user.username, 'SC')
    print('#####')
    print(result)
    print('######')

    form1 = formCalcSC()  # Pass DB values
    
    return render(request, 'PageSC.html', {'form1': form1})


# Function to handle form submission
def handle_sc_form(request):
    if not request.user.is_authenticated:
        return redirect('login')  # Redirect to the login page if the user is not authenticated

    if request.method == 'POST' and 'form1_submit' in request.POST:
        form1 = formCalcSC(request.POST)
        if form1.is_valid():
            # Access the cleaned_data dictionary to get individual field values
            oSec01Field01_value = form1.cleaned_data.get('oSec01Field01')
            oSec01Field02_value = form1.cleaned_data.get('oSec01Field02')
            oSec01Field03_value = form1.cleaned_data.get('oSec01Field03')
            oSec01Field04_value = form1.cleaned_data.get('oSec01Field04')

            # Calculate new values for fields            
            api_url = "https://us-central1-h1000project1.cloudfunctions.net/f01"
            req_type = "SC"  
            input_data = {
                "SC_Density":        oSec01Field01_value,
                "SC_Length":         oSec01Field02_value,
                "SC_Diameter":       oSec01Field02_value,
                "SC_Safety":         oSec01Field02_value,
            }

            # Call the function to interact with the API
            response = interact_with_api(api_url, req_type, input_data)
            
            oSec02Field01_result = response["SC_o1"]
            oSec02Field02_result = response["SC_o2"]
            oSec02Field03_result = response["SC_o3"]
            oSec02Field04_result = response["SC_o4"]
            oSec02Field05_result = response["SC_o5"]
            oSec02Field06_result = response["SC_o6"]

            # Save the form with updated values
            instance = form1.save(commit=False)  # Do not save to the database yet
            instance.oSec02Field01 = oSec02Field01_result  # Update S2field1
            instance.oSec02Field02 = oSec02Field02_result  # Update S2field1
            instance.oSec02Field03 = oSec02Field03_result  # Update S2field1
            instance.oSec02Field04 = oSec02Field04_result  # Update S2field1
            instance.oSec02Field05 = oSec02Field05_result  # Update S2field1
            instance.oSec02Field06 = oSec02Field06_result  # Update S2field1
            
            instance.oSec00Field01 = request.user.username  # Insert username
            instance.oSec00Field02 = datetime.now().strftime('%Y-%m-%d %H:%M:%S')  # Insert current time
            instance.oSec00Field03 = "SC"  # Insert fixed type
            instance.save()  # Save to the database

            # Refresh the form with initial values to display results
            form1 = formCalcSC(initial={
                'oSec01Field01': oSec01Field01_value,
                'oSec01Field02': oSec01Field02_value,
                'oSec01Field03': oSec01Field03_value,
                'oSec01Field04': oSec01Field04_value,
                
                'oSec02Field01': oSec02Field01_result,
                'oSec02Field02': oSec02Field02_result,
                'oSec02Field03': oSec02Field03_result,
                'oSec02Field04': oSec02Field04_result,
                'oSec02Field05': oSec02Field05_result,
                'oSec02Field06': oSec02Field06_result,
            })

            return render(request, 'PageSC.html', {'form1': form1})
    
    
    return redirect('sc_load')  # Redirect to the page if the request is invalid


def generate_sc_report(request):
    
    if request.method == "POST":
        form1 = formCalcCT(request.POST)
        # Create a new Word document
        doc = Document()
        doc.add_heading('Circular Tanks Report', level=1)

        # Extract form data
        form_data = {
            "Input": [
                (form1.fields["oSec01Field01"].label, request.POST.get("oSec01Field01", "N/A")),
                (form1.fields["oSec01Field02"].label, request.POST.get("oSec01Field02", "N/A")),
            ],
            "Output": [
                (form1.fields["oSec02Field01"].label, request.POST.get("oSec02Field01", "N/A")),
                (form1.fields["oSec02Field02"].label, request.POST.get("oSec02Field02", "N/A")),
                (form1.fields["oSec02Field03"].label, request.POST.get("oSec02Field03", "N/A")),
                (form1.fields["oSec02Field04"].label, request.POST.get("oSec02Field04", "N/A")),
                (form1.fields["oSec02Field05"].label, request.POST.get("oSec02Field05", "N/A")),
                (form1.fields["oSec02Field06"].label, request.POST.get("oSec02Field06", "N/A")),
                (form1.fields["oSec02Field07"].label, request.POST.get("oSec02Field07", "N/A")),
            ]
        }

        # Add form data to the Word document
        for section, fields in form_data.items():
            doc.add_heading(section, level=2)
            for field, value in fields:
                doc.add_paragraph(f"{field}: {value}")

        # Prepare the response to download the document
        response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.wordprocessingml.document')
        response['Content-Disposition'] = 'attachment; filename="Circular_Tank_Report.docx"'
        doc.save(response)
        return response

    return HttpResponse("Invalid request", status=400)


def modify_sc_dxf(request):
    if request.method == "POST":
        # Define the path to the DXF file in the static directory
        static_path = os.path.join(settings.BASE_DIR, "static", "aDxfs", "MS_DXF_B.dxf")
        modified_path = os.path.join(settings.BASE_DIR, "static", "aDxfs", "modified_file.dxf")

        # Load the DXF file
        doc = ezdxf.readfile(static_path)

        # Iterate over the modelspace to find all DIMENSION entities
        for entity in doc.modelspace().query("DIMENSION"):
            if entity.dxf.text == "CHH111":
                entity.dxf.text = request.POST.get("oSec01Field01", "000")
            elif entity.dxf.text == "CHW111":
                entity.dxf.text = request.POST.get("oSec01Field02", "000")
            elif entity.dxf.text == "BeltHeight":
                entity.dxf.text = request.POST.get("oSec01Field03", "000")
            elif entity.dxf.text == "DEG111":
                entity.dxf.text = request.POST.get("oSec01Field08", "000")

            # Render the dimension to apply changes
            entity.render()

        # Save the modified DXF file
        doc.saveas(modified_path)

        # Serve the modified file for download
        with open(modified_path, "rb") as dxf_file:
            response = HttpResponse(dxf_file.read(), content_type="application/dxf")
            response["Content-Disposition"] = 'attachment; filename="modified_file.dxf"'
            return response

    return HttpResponse("Invalid request", status=400)

    
###############
###############
###############
###############

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






#######################




# Function to load the MS page
def load_bs_page(request):
    if not request.user.is_authenticated:
        return redirect('login')  # Redirect to login page if user is not authenticated

    result = check_user_autho(request.user.username, 'BS')
    print('#####')
    print(result)
    print('######')

    form1 = formCalcBS()  # Pass DB values

    return render(request, 'PageBS.html', {'form1': form1})

# Function to handle form submission
def handle_bs_form(request):
    if not request.user.is_authenticated:
        return redirect('login')  # Redirect to the login page if the user is not authenticated


    if request.method == 'POST' and 'form1_submit' in request.POST:
        form1 = formCalcBS(request.POST)
        if form1.is_valid():
            # Access the cleaned_data dictionary to get individual field values
            oSec01Field01_value = form1.cleaned_data.get('oSec01Field01')
            oSec01Field02_value = form1.cleaned_data.get('oSec01Field02')
            oSec01Field03_value = form1.cleaned_data.get('oSec01Field03')
            oSec01Field04_value = form1.cleaned_data.get('oSec01Field04')
            oSec01Field05_value = form1.cleaned_data.get('oSec01Field05')
            oSec01Field06_value = form1.cleaned_data.get('oSec01Field06')

            # Calculate new values for fields            
            api_url = "https://us-central1-h1000project1.cloudfunctions.net/f01"
            req_type = "BS"  
            input_data = {
                "BS_Bar_Dia":     oSec01Field01_value,
                "BS_Bar_Space":       oSec01Field02_value,
                "BS_Screen_Height":        oSec01Field03_value,
                "BS_Screen_Width":        oSec01Field04_value,
                "BS_Screen_Depth":        oSec01Field05_value,
                "BS_Plate_Th":      oSec01Field06_value,
            }

            # Call the function to interact with the API
            response = interact_with_api(api_url, req_type, input_data)
            
            oSec02Field01_result = response["O_Weight_allBars"]
            oSec02Field02_result = response["O_Plate_weight"]
            oSec02Field03_result = response["O_Total_weight"]

            # Save the form with updated values
            instance = form1.save(commit=False)  # Do not save to the database yet
            instance.oSec02Field01 = oSec02Field01_result  # Update S2field1
            instance.oSec02Field02 = oSec02Field02_result  # Update S2field2
            instance.oSec02Field03 = oSec02Field03_result  # Update S2field3
            instance.oSec00Field01 = request.user.username  # Insert username
            instance.oSec00Field02 = datetime.now().strftime('%Y-%m-%d %H:%M:%S')  # Insert current time
            instance.oSec00Field03 = "BS"  # Insert fixed type
            instance.save()  # Save to the database

            # Refresh the form with initial values to display results
            form1 = formCalcBS(initial={
                'oSec01Field01': oSec01Field01_value,
                'oSec01Field02': oSec01Field02_value,
                'oSec01Field03': oSec01Field03_value,
                'oSec01Field04': oSec01Field04_value,
                'oSec01Field05': oSec01Field05_value,
                'oSec01Field06': oSec01Field06_value,

                'oSec02Field01': oSec02Field01_result,
                'oSec02Field02': oSec02Field02_result,
                'oSec02Field03': oSec02Field03_result,
            })

            return render(request, 'PageBS.html', {'form1': form1})

    return redirect('ms_load')  # Redirect to the page if the request is invalid


def generate_bs_report(request):
    
    if request.method == "POST":
        form1 = formCalcBS(request.POST)
        # Create a new Word document
        doc = Document()
        doc.add_heading('Basket Screen Report', level=1)

        # Extract form data
        form_data = {
            "Input": [
                (form1.fields["oSec01Field01"].label, request.POST.get("oSec01Field01", "N/A")),
                (form1.fields["oSec01Field02"].label, request.POST.get("oSec01Field02", "N/A")),
                (form1.fields["oSec01Field03"].label, request.POST.get("oSec01Field03", "N/A")),
                (form1.fields["oSec01Field04"].label, request.POST.get("oSec01Field04", "N/A")),
                (form1.fields["oSec01Field05"].label, request.POST.get("oSec01Field05", "N/A")),
                (form1.fields["oSec01Field06"].label, request.POST.get("oSec01Field06", "N/A")),
            ],
            "Output": [
                (form1.fields["oSec02Field01"].label, request.POST.get("oSec02Field01", "N/A")),
                (form1.fields["oSec02Field02"].label, request.POST.get("oSec02Field02", "N/A")),
                (form1.fields["oSec02Field03"].label, request.POST.get("oSec02Field03", "N/A")),
            ]
        }

        # Add form data to the Word document
        for section, fields in form_data.items():
            doc.add_heading(section, level=2)
            for field, value in fields:
                doc.add_paragraph(f"{field}: {value}")

        # Prepare the response to download the document
        response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.wordprocessingml.document')
        response['Content-Disposition'] = 'attachment; filename="Basket_Screen_Report.docx"'
        doc.save(response)
        return response

    return HttpResponse("Invalid request", status=400)


def modify_bs_dxf(request):
    
    if request.method == "POST":
        form1 = formCalcBS(request.POST)
    return render(request, 'PageBS.html', {'form1': form1})

    # if request.method == "POST":
    #     # Define the path to the DXF file in the static directory
    #     static_path = os.path.join(settings.BASE_DIR, "static", "aDxfs", "MS_General_Drawing.dxf")
    #     modified_path = os.path.join(settings.BASE_DIR, "static", "aDxfs", "modified_fileNew.dxf")

    #     # Load the DXF file
    #     doc = ezdxf.readfile(static_path)

    #     # Iterate over the modelspace to find all DIMENSION entities
    #     for entity in doc.modelspace().query("DIMENSION"):
    #         if entity.dxf.text == "MS_chHeight":
    #             entity.dxf.text = request.POST.get("oSec01Field01", "000")
    #         elif entity.dxf.text == "MS_chWidth":
    #             entity.dxf.text = request.POST.get("oSec01Field02", "000")
    #         elif entity.dxf.text == "BeltHeight":
    #             entity.dxf.text = request.POST.get("oSec01Field03", "000")
    #         elif entity.dxf.text == "MS_angle":
    #             entity.dxf.text = request.POST.get("oSec01Field08", "000")
    #         elif entity.dxf.text == "MS_barSpace":
    #             entity.dxf.text = request.POST.get("oSec01Field05", "000")
    #         elif entity.dxf.text == "MS_barTh":
    #             entity.dxf.text = request.POST.get("oSec01Field06", "000")

    #         # Render the dimension to apply changes
    #         entity.render()

    #     # Save the modified DXF file
    #     doc.saveas(modified_path)

    #     # Serve the modified file for download
    #     with open(modified_path, "rb") as dxf_file:
    #         response = HttpResponse(dxf_file.read(), content_type="application/dxf")
    #         response["Content-Disposition"] = 'attachment; filename="modified_fileNew.dxf"'
    #         return response

    # return HttpResponse("Invalid request", status=400)

###############################




# Function to load the MS page
def load_ns_page(request):
    if not request.user.is_authenticated:
        return redirect('login')  # Redirect to login page if user is not authenticated

    result = check_user_autho(request.user.username, 'BS')
    print('#####')
    print(result)
    print('######')

    form1 = formCalcNS()  # Pass DB values

    return render(request, 'PageNS.html', {'form1': form1})

# Function to handle form submission
def handle_ns_form(request):
    if not request.user.is_authenticated:
        return redirect('login')  # Redirect to the login page if the user is not authenticated

    
    print("Line 1866")


    if request.method == 'POST' and 'form1_submit' in request.POST:
        
        print("Line 1871")
        
        form1 = formCalcNS(request.POST)
        
        print("Line 1875")

        if form1.is_valid():
            
            print("Line 1879")
            # Access the cleaned_data dictionary to get individual field values
            oSec01Field01_value = form1.cleaned_data.get('oSec01Field01')
            oSec01Field02_value = form1.cleaned_data.get('oSec01Field02')
            oSec01Field03_value = form1.cleaned_data.get('oSec01Field03')
            oSec01Field04_value = form1.cleaned_data.get('oSec01Field04')
            oSec01Field05_value = form1.cleaned_data.get('oSec01Field05')
            oSec01Field06_value = form1.cleaned_data.get('oSec01Field06')
            oSec01Field07_value = form1.cleaned_data.get('oSec01Field07')
            oSec01Field08_value = form1.cleaned_data.get('oSec01Field08')

            # Calculate new values for fields            
            api_url = "https://us-central1-h1000project1.cloudfunctions.net/f01"
            req_type = "NS"  
            input_data = {
                "NS_Ch_Height":         oSec01Field01_value,
                "NS_Ch_Width":          oSec01Field02_value,
                "NS_WaterLv":           oSec01Field03_value,
                "NS_WaterLv_Margin":    oSec01Field04_value,
                "NS_Bar_Spacing":       oSec01Field05_value,
                "NS_Bar_Th":            oSec01Field06_value,
                "NS_Bar_Width":         oSec01Field07_value,
                "NS_Angle":             oSec01Field08_value,
            }

            # Call the function to interact with the API
            response = interact_with_api(api_url, req_type, input_data)
            
            oSec02Field01_result = response["O_Weight"]

            # Save the form with updated values
            instance = form1.save(commit=False)  # Do not save to the database yet
            instance.oSec02Field01 = oSec02Field01_result  # Update S2field1            
            instance.oSec00Field01 = request.user.username  # Insert username
            instance.oSec00Field02 = datetime.now().strftime('%Y-%m-%d %H:%M:%S')  # Insert current time
            instance.oSec00Field03 = "NS"  # Insert fixed type
            instance.save()  # Save to the database

            # Refresh the form with initial values to display results
            form1 = formCalcNS(initial={
                'oSec01Field01': oSec01Field01_value,
                'oSec01Field02': oSec01Field02_value,
                'oSec01Field03': oSec01Field03_value,
                'oSec01Field04': oSec01Field04_value,
                'oSec01Field05': oSec01Field05_value,
                'oSec01Field06': oSec01Field06_value,
                'oSec01Field07': oSec01Field07_value,
                'oSec01Field08': oSec01Field08_value,

                'oSec02Field01': oSec02Field01_result,
            })

            return render(request, 'PageNS.html', {'form1': form1})

    return redirect('ms_load')  # Redirect to the page if the request is invalid


def generate_ns_report(request):
    
    if request.method == "POST":
        form1 = formCalcNS(request.POST)
        # Create a new Word document
        doc = Document()
        doc.add_heading('Manual Screen Report', level=1)

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
            ],
            "Output": [
                (form1.fields["oSec02Field01"].label, request.POST.get("oSec02Field01", "N/A")),
            ]
        }

        # Add form data to the Word document
        for section, fields in form_data.items():
            doc.add_heading(section, level=2)
            for field, value in fields:
                doc.add_paragraph(f"{field}: {value}")

        # Prepare the response to download the document
        response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.wordprocessingml.document')
        response['Content-Disposition'] = 'attachment; filename="Manual_Screen_Report.docx"'
        doc.save(response)
        return response

    return HttpResponse("Invalid request", status=400)


def modify_ns_dxf(request):
    
    if request.method == "POST":
        form1 = formCalcBS(request.POST)
    return render(request, 'PageNS.html', {'form1': form1})

    # if request.method == "POST":
    #     # Define the path to the DXF file in the static directory
    #     static_path = os.path.join(settings.BASE_DIR, "static", "aDxfs", "MS_General_Drawing.dxf")
    #     modified_path = os.path.join(settings.BASE_DIR, "static", "aDxfs", "modified_fileNew.dxf")

    #     # Load the DXF file
    #     doc = ezdxf.readfile(static_path)

    #     # Iterate over the modelspace to find all DIMENSION entities
    #     for entity in doc.modelspace().query("DIMENSION"):
    #         if entity.dxf.text == "MS_chHeight":
    #             entity.dxf.text = request.POST.get("oSec01Field01", "000")
    #         elif entity.dxf.text == "MS_chWidth":
    #             entity.dxf.text = request.POST.get("oSec01Field02", "000")
    #         elif entity.dxf.text == "BeltHeight":
    #             entity.dxf.text = request.POST.get("oSec01Field03", "000")
    #         elif entity.dxf.text == "MS_angle":
    #             entity.dxf.text = request.POST.get("oSec01Field08", "000")
    #         elif entity.dxf.text == "MS_barSpace":
    #             entity.dxf.text = request.POST.get("oSec01Field05", "000")
    #         elif entity.dxf.text == "MS_barTh":
    #             entity.dxf.text = request.POST.get("oSec01Field06", "000")

    #         # Render the dimension to apply changes
    #         entity.render()

    #     # Save the modified DXF file
    #     doc.saveas(modified_path)

    #     # Serve the modified file for download
    #     with open(modified_path, "rb") as dxf_file:
    #         response = HttpResponse(dxf_file.read(), content_type="application/dxf")
    #         response["Content-Disposition"] = 'attachment; filename="modified_fileNew.dxf"'
    #         return response

    # return HttpResponse("Invalid request", status=400)


###############################




def load_pnch_page(request):
    if not request.user.is_authenticated:
        return redirect('login')  # Redirect to login page if user is not authenticated

    result = check_user_autho(request.user.username, 'PNch')
    print('#####')
    print(result)
    print('######')

    # Fetch initial values from DB

    form1 = formCalcPNch()  # Pass DB values

    return render(request, 'PagePNch.html', {'form1': form1})



def handle_pnch_form(request):
    if not request.user.is_authenticated:
        return redirect('login')  # Redirect to the login page if the user is not authenticated

    
    print("aaa")


    if request.method == 'POST' and 'form1_submit' in request.POST:
        
        print("aaa")
        
        form1 = formCalcPNch(request.POST)
        if form1.is_valid():
            # Access the cleaned_data dictionary to get individual field values
            oSec01Field01_value = form1.cleaned_data.get('oSec01Field01')
            oSec01Field02_value = form1.cleaned_data.get('oSec01Field02')
            oSec01Field03_value = form1.cleaned_data.get('oSec01Field03')
            oSec01Field04_value = form1.cleaned_data.get('oSec01Field04')
            oSec01Field05_value = form1.cleaned_data.get('oSec01Field05')
            oSec01Field06_value = form1.cleaned_data.get('oSec01Field06')
            oSec01Field07_value = form1.cleaned_data.get('oSec01Field07')
            oSec01Field08_value = form1.cleaned_data.get('oSec01Field08')
            oSec01Field09_value = form1.cleaned_data.get('oSec01Field09')
            oSec01Field10_value = form1.cleaned_data.get('oSec01Field10')
            
            
            print(oSec01Field08_value)
            print(oSec01Field09_value)
            print(oSec01Field10_value)

            # Calculate new values for fields            
            api_url = "https://us-central1-h1000project1.cloudfunctions.net/f01"
            req_type = "PNch"  
            input_data = {
                "PNch_Channel_Height":              oSec01Field01_value,
                "PNch_Frame_Height_Over_Channel":   oSec01Field02_value,
                "PNch_Channel_Width":               oSec01Field03_value,
                "PNch_Gate_Margin_Width":           oSec01Field04_value,
                "PNch_Water_Lv":                    oSec01Field05_value,
                "PNch_Gate_Margin_Over_Water_Lv":   oSec01Field06_value,
                "PNch_Gate_Th":                     oSec01Field07_value,
                "PNch_Gate_Other_PLs":              oSec01Field08_value,
                "PNch_HeadStock":                   oSec01Field09_value,
                "PNch_Frame_Weight_Per_M":          oSec01Field10_value,
            }

            # Call the function to interact with the API
            response = interact_with_api(api_url, req_type, input_data)
            
            oSec02Field01_result = response["O_Frame_Perimeter"]
            oSec02Field02_result = response["O_Frame_Weight"]
            oSec02Field03_result = response["O_Gate_PL_Weight"]
            oSec02Field04_result = response["O_Gate_Stiffener_N"]
            oSec02Field05_result = response["O_Gate_Stiffener_Weight"]
            oSec02Field06_result = response["O_Gate_Weight"]
            oSec02Field07_result = response["O_Total_Weight"]

            # Save the form with updated values
            instance = form1.save(commit=False)  # Do not save to the database yet
            instance.oSec02Field01 = oSec02Field01_result      
            instance.oSec02Field02 = oSec02Field02_result        
            instance.oSec02Field03 = oSec02Field03_result      
            instance.oSec02Field04 = oSec02Field04_result        
            instance.oSec02Field05 = oSec02Field05_result       
            instance.oSec02Field06 = oSec02Field06_result         
            instance.oSec02Field07 = oSec02Field07_result            
            instance.oSec00Field01 = request.user.username  # Insert username
            instance.oSec00Field02 = datetime.now().strftime('%Y-%m-%d %H:%M:%S')  # Insert current time
            instance.oSec00Field03 = "PNch"  # Insert fixed type
            instance.save()  # Save to the database

            # Refresh the form with initial values to display results
            form1 = formCalcPNch(initial={
                'oSec01Field01': oSec01Field01_value,
                'oSec01Field02': oSec01Field02_value,
                'oSec01Field03': oSec01Field03_value,
                'oSec01Field04': oSec01Field04_value,
                'oSec01Field05': oSec01Field05_value,
                'oSec01Field06': oSec01Field06_value,
                'oSec01Field07': oSec01Field07_value,
                'oSec01Field08': oSec01Field08_value,
                'oSec01Field09': oSec01Field09_value,
                'oSec01Field10': oSec01Field10_value,

                'oSec02Field01': oSec02Field01_result,
                'oSec02Field02': oSec02Field02_result,
                'oSec02Field03': oSec02Field03_result,
                'oSec02Field04': oSec02Field04_result,
                'oSec02Field05': oSec02Field05_result,
                'oSec02Field06': oSec02Field06_result,
                'oSec02Field07': oSec02Field07_result,
            })
            
            print(oSec01Field08_value)
            print(oSec01Field09_value)
            print(oSec01Field10_value)

            return render(request, 'PagePNch.html', {'form1': form1})

    return redirect('ms_load')  # Redirect to the page if the request is invalid


def generate_pnch_report(request):
    
    if request.method == "POST":
        form1 = formCalcPNch(request.POST)
        # Create a new Word document
        doc = Document()
        doc.add_heading('Channel Penstock Report', level=1)

        # Extract form data
        form_data = {
            "Input": [
                (form1.fields["oSec01Field01"].label, request.POST.get("oSec01Field01", "N/A")),
                (form1.fields["oSec01Field02"].label, request.POST.get("oSec01Field02", "N/A")),
                (form1.fields["oSec01Field03"].label, request.POST.get("oSec01Field03", "N/A")),
                (form1.fields["oSec01Field04"].label, request.POST.get("oSec01Field04", "N/A")),
                (form1.fields["oSec01Field05"].label, request.POST.get("oSec01Field05", "N/A")),
                (form1.fields["oSec01Field06"].label, request.POST.get("oSec01Field06", "N/A")),
            ],
            "Output": [
                (form1.fields["oSec02Field01"].label, request.POST.get("oSec02Field01", "N/A")),
                (form1.fields["oSec02Field02"].label, request.POST.get("oSec02Field02", "N/A")),
                (form1.fields["oSec02Field03"].label, request.POST.get("oSec02Field03", "N/A")),
                (form1.fields["oSec02Field04"].label, request.POST.get("oSec02Field04", "N/A")),
                (form1.fields["oSec02Field05"].label, request.POST.get("oSec02Field05", "N/A")),
                (form1.fields["oSec02Field06"].label, request.POST.get("oSec02Field06", "N/A")),
                (form1.fields["oSec02Field07"].label, request.POST.get("oSec02Field07", "N/A")),
            ]
        }

        # Add form data to the Word document
        for section, fields in form_data.items():
            doc.add_heading(section, level=2)
            for field, value in fields:
                doc.add_paragraph(f"{field}: {value}")

        # Prepare the response to download the document
        response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.wordprocessingml.document')
        response['Content-Disposition'] = 'attachment; filename="Channel_Penstock_Report.docx"'
        doc.save(response)
        return response

    return HttpResponse("Invalid request", status=400)


def modify_pnch_dxf(request):
    
    if request.method == "POST":
        form1 = formCalcBS(request.POST)
    return render(request, 'PageNS.html', {'form1': form1})

    # if request.method == "POST":
    #     # Define the path to the DXF file in the static directory
    #     static_path = os.path.join(settings.BASE_DIR, "static", "aDxfs", "MS_General_Drawing.dxf")
    #     modified_path = os.path.join(settings.BASE_DIR, "static", "aDxfs", "modified_fileNew.dxf")

    #     # Load the DXF file
    #     doc = ezdxf.readfile(static_path)

    #     # Iterate over the modelspace to find all DIMENSION entities
    #     for entity in doc.modelspace().query("DIMENSION"):
    #         if entity.dxf.text == "MS_chHeight":
    #             entity.dxf.text = request.POST.get("oSec01Field01", "000")
    #         elif entity.dxf.text == "MS_chWidth":
    #             entity.dxf.text = request.POST.get("oSec01Field02", "000")
    #         elif entity.dxf.text == "BeltHeight":
    #             entity.dxf.text = request.POST.get("oSec01Field03", "000")
    #         elif entity.dxf.text == "MS_angle":
    #             entity.dxf.text = request.POST.get("oSec01Field08", "000")
    #         elif entity.dxf.text == "MS_barSpace":
    #             entity.dxf.text = request.POST.get("oSec01Field05", "000")
    #         elif entity.dxf.text == "MS_barTh":
    #             entity.dxf.text = request.POST.get("oSec01Field06", "000")

    #         # Render the dimension to apply changes
    #         entity.render()

    #     # Save the modified DXF file
    #     doc.saveas(modified_path)

    #     # Serve the modified file for download
    #     with open(modified_path, "rb") as dxf_file:
    #         response = HttpResponse(dxf_file.read(), content_type="application/dxf")
    #         response["Content-Disposition"] = 'attachment; filename="modified_fileNew.dxf"'
    #         return response

    # return HttpResponse("Invalid request", status=400)



###############################




def load_pnwa_page(request):
    if not request.user.is_authenticated:
        return redirect('login')  # Redirect to login page if user is not authenticated

    result = check_user_autho(request.user.username, 'PNch')
    print('#####')
    print(result)
    print('######')


    form1 = formCalcPNwa()  

    return render(request, 'PagePNwa.html', {'form1': form1})



def handle_pnwa_form(request):
    if not request.user.is_authenticated:
        return redirect('login')  # Redirect to the login page if the user is not authenticated

    print("aaa")
    if request.method == 'POST' and 'form1_submit' in request.POST:
                
        print("aaa")
        
        form1 = formCalcPNwa(request.POST)
        if form1.is_valid():
            
            print("form is valid")
            # Access the cleaned_data dictionary to get individual field values
            oSec01Field01_value = form1.cleaned_data.get('oSec01Field01')
            oSec01Field02_value = form1.cleaned_data.get('oSec01Field02')
            oSec01Field03_value = form1.cleaned_data.get('oSec01Field03')
            oSec01Field04_value = form1.cleaned_data.get('oSec01Field04')
            oSec01Field05_value = form1.cleaned_data.get('oSec01Field05')
            oSec01Field06_value = form1.cleaned_data.get('oSec01Field06')
            oSec01Field07_value = form1.cleaned_data.get('oSec01Field07')
            oSec01Field08_value = form1.cleaned_data.get('oSec01Field08')
            oSec01Field09_value = form1.cleaned_data.get('oSec01Field09')
            oSec01Field10_value = form1.cleaned_data.get('oSec01Field10')
            

            # Calculate new values for fields            
            api_url = "https://us-central1-h1000project1.cloudfunctions.net/f01"
            req_type = "PNwa"  
            input_data = {
                "aInput01":   oSec01Field01_value,
                "aInput02":   oSec01Field02_value,
                "aInput03":   oSec01Field03_value,
                "aInput04":   oSec01Field04_value,
                "aInput05":   oSec01Field05_value,
                "aInput06":   oSec01Field06_value,
                "aInput07":   oSec01Field07_value,
                "aInput08":   oSec01Field08_value,
                "aInput09":   oSec01Field09_value,
                "aInput10":   oSec01Field10_value,
            }

            # Call the function to interact with the API
            response = interact_with_api(api_url, req_type, input_data)
            
            oSec02Field01_result = response["O_PNwa_Out01"]
            oSec02Field02_result = response["O_PNwa_Out02"]
            oSec02Field03_result = response["O_PNwa_Out03"]
            oSec02Field04_result = response["O_PNwa_Out04"]
            oSec02Field05_result = response["O_PNwa_Out05"]
            oSec02Field06_result = response["O_PNwa_Out06"]
            oSec02Field07_result = response["O_PNwa_Out07"]

            # Save the form with updated values
            instance = form1.save(commit=False)  # Do not save to the database yet
            instance.oSec02Field01 = oSec02Field01_result      
            instance.oSec02Field02 = oSec02Field02_result        
            instance.oSec02Field03 = oSec02Field03_result      
            instance.oSec02Field04 = oSec02Field04_result        
            instance.oSec02Field05 = oSec02Field05_result       
            instance.oSec02Field06 = oSec02Field06_result         
            instance.oSec02Field07 = oSec02Field07_result  
                      
            instance.oSec00Field01 = request.user.username  # Insert username
            instance.oSec00Field02 = datetime.now().strftime('%Y-%m-%d %H:%M:%S')  # Insert current time
            instance.oSec00Field03 = "PNwa"  # Insert fixed type
            instance.save()  # Save to the database

            # Refresh the form with initial values to display results
            form1 = formCalcPNwa(initial={
                'oSec01Field01': oSec01Field01_value,
                'oSec01Field02': oSec01Field02_value,
                'oSec01Field03': oSec01Field03_value,
                'oSec01Field04': oSec01Field04_value,
                'oSec01Field05': oSec01Field05_value,
                'oSec01Field06': oSec01Field06_value,
                'oSec01Field07': oSec01Field07_value,
                'oSec01Field08': oSec01Field08_value,
                'oSec01Field09': oSec01Field09_value,
                'oSec01Field10': oSec01Field10_value,

                'oSec02Field01': oSec02Field01_result,
                'oSec02Field02': oSec02Field02_result,
                'oSec02Field03': oSec02Field03_result,
                'oSec02Field04': oSec02Field04_result,
                'oSec02Field05': oSec02Field05_result,
                'oSec02Field06': oSec02Field06_result,
                'oSec02Field07': oSec02Field07_result,
            })
                        
            return render(request, 'PagePNwa.html', {'form1': form1})

    return redirect('ms_load')  # Redirect to the page if the request is invalid


def generate_pnwa_report(request):
    
    if request.method == "POST":
        form1 = formCalcPNwa(request.POST)
        # Create a new Word document
        doc = Document()
        doc.add_heading('Wall Penstock Report', level=1)

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
            ],
            "Output": [
                (form1.fields["oSec02Field01"].label, request.POST.get("oSec02Field01", "N/A")),
                (form1.fields["oSec02Field02"].label, request.POST.get("oSec02Field02", "N/A")),
                (form1.fields["oSec02Field03"].label, request.POST.get("oSec02Field03", "N/A")),
                (form1.fields["oSec02Field04"].label, request.POST.get("oSec02Field04", "N/A")),
                (form1.fields["oSec02Field05"].label, request.POST.get("oSec02Field05", "N/A")),
                (form1.fields["oSec02Field06"].label, request.POST.get("oSec02Field06", "N/A")),
                (form1.fields["oSec02Field07"].label, request.POST.get("oSec02Field07", "N/A")),
            ]
        }

        # Add form data to the Word document
        for section, fields in form_data.items():
            doc.add_heading(section, level=2)
            for field, value in fields:
                doc.add_paragraph(f"{field}: {value}")

        # Prepare the response to download the document
        response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.wordprocessingml.document')
        response['Content-Disposition'] = 'attachment; filename="Wall_Penstock_Report.docx"'
        doc.save(response)
        return response

    return HttpResponse("Invalid request", status=400)


def modify_pnwa_dxf(request):
    
    if request.method == "POST":
        form1 = formCalcBS(request.POST)
    return render(request, 'PageNS.html', {'form1': form1})

    # if request.method == "POST":
    #     # Define the path to the DXF file in the static directory
    #     static_path = os.path.join(settings.BASE_DIR, "static", "aDxfs", "MS_General_Drawing.dxf")
    #     modified_path = os.path.join(settings.BASE_DIR, "static", "aDxfs", "modified_fileNew.dxf")

    #     # Load the DXF file
    #     doc = ezdxf.readfile(static_path)

    #     # Iterate over the modelspace to find all DIMENSION entities
    #     for entity in doc.modelspace().query("DIMENSION"):
    #         if entity.dxf.text == "MS_chHeight":
    #             entity.dxf.text = request.POST.get("oSec01Field01", "000")
    #         elif entity.dxf.text == "MS_chWidth":
    #             entity.dxf.text = request.POST.get("oSec01Field02", "000")
    #         elif entity.dxf.text == "BeltHeight":
    #             entity.dxf.text = request.POST.get("oSec01Field03", "000")
    #         elif entity.dxf.text == "MS_angle":
    #             entity.dxf.text = request.POST.get("oSec01Field08", "000")
    #         elif entity.dxf.text == "MS_barSpace":
    #             entity.dxf.text = request.POST.get("oSec01Field05", "000")
    #         elif entity.dxf.text == "MS_barTh":
    #             entity.dxf.text = request.POST.get("oSec01Field06", "000")

    #         # Render the dimension to apply changes
    #         entity.render()

    #     # Save the modified DXF file
    #     doc.saveas(modified_path)

    #     # Serve the modified file for download
    #     with open(modified_path, "rb") as dxf_file:
    #         response = HttpResponse(dxf_file.read(), content_type="application/dxf")
    #         response["Content-Disposition"] = 'attachment; filename="modified_fileNew.dxf"'
    #         return response

    # return HttpResponse("Invalid request", status=400)



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



def project_list(request):
    if request.method == "POST":
        form = ProjectForm(request.POST)
        if form.is_valid():
            
            instance = form.save(commit=False)  # Don't save to DB yet

            
            # Get the company associated with the user
            try:
                user_company = UserCompany.objects.get(user=request.user).company
                instance.company = user_company  # Assign company to the instance
            except UserCompany.DoesNotExist:
                return render(request, 'project_list', {"form": form, "error": "User is not associated with a company"})


            form.save()
            return redirect('project_list')
    else:
        form = ProjectForm()
        
        
    # Get the company of the logged-in user
    user_company = None
    if request.user.is_authenticated:
        try:
            user_company = UserCompany.objects.get(user=request.user).company
        except UserCompany.DoesNotExist:
            user_company = None

    # Assign company filter only if the user has a company
    if user_company:
        #machines = Machine.objects.filter(oSec00Field03=DB_Name, company=user_company)
        projects = Project.objects.filter(company=user_company)
    else:
        projects = Project.objects.none()  # Return an empty queryset if no company
    
    #projects = Project.objects.all()
    return render(request, 'project_list.html', {'form': form, 'projects': projects})



def edit_project(request, project_id):
    project = get_object_or_404(Project, id=project_id)
    
    if request.method == "POST":
        form = ProjectForm(request.POST, instance=project)
        if form.is_valid():
            form.save()
            
            # Check if request is AJAX
            if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                return JsonResponse({'success': True})
            
            # Redirect to project list page for normal form submission
            return redirect('project_list')

        else:
            if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                return JsonResponse({'success': False, 'errors': form.errors})

    # If it's a normal GET request, render the edit page
    form = ProjectForm(instance=project)
    
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return JsonResponse({'success': True, 'form': form.as_p()})
    
    return render(request, 'edit_project.html', {'form': form})



def delete_project(request, project_id):
    if request.method == "POST":
        project = get_object_or_404(Project, id=project_id)
        project.delete()

        # Otherwise, redirect to the project list page
        return redirect('project_list')

    return JsonResponse({'success': False, 'error': 'Invalid request'})



def get_machines(request, project_id):
    try:
        project = Project.objects.get(id=project_id)
        machines = Machine.objects.filter(project=project)
        
        data = {
            "project_name": project.name,
            "machines": list(machines.values("oSec00Field01", "oSec00Field02", "oSec00Field03",
                                             "oSec01Field01", "oSec01Field02", "oSec01Field03",
                                             "oSec01Field04", "oSec01Field05"))
        }
        return JsonResponse(data)
    except Project.DoesNotExist:
        return JsonResponse({"error": "Project not found"}, status=404)


# def generate_report(request, project_id):
#     try:
#         project = Project.objects.get(id=project_id)
#         machines = Machine.objects.filter(project=project)

#         # Create a Word document
#         doc = Document()
#         doc.add_heading(f'Project Report: {project.name}', level=1)

#         # Add project details in a two-column table
#         doc.add_heading("Project Details", level=2)
#         project_table = doc.add_table(rows=0, cols=2)

#         project_data = {
#             "Name": project.name,
#             "Client Name": project.client_name,
#             "Capacity": project.capacity,
#         }

#         for key, value in project_data.items():
#             row_cells = project_table.add_row().cells
#             row_cells[0].text = key
#             row_cells[1].text = str(value)

#         doc.add_paragraph("\n" + "=" * 50 + "\n")

#         # Add machine details
#         doc.add_heading("Machines", level=2)

#         for machine in machines:
#             doc.add_paragraph(f"Machine ID: {machine.id}", style="Heading3")
#             doc.add_paragraph("Sec01")

#             machine_table = doc.add_table(rows=0, cols=2)

#             machine_data = {
#                 "Username": machine.oSec00Field01,
#                 "Created At": machine.oSec00Field02,
#                 "Type": machine.oSec00Field03,
#                 machine.oSec01Field01 : machine.oSec01Field02,
#                 machine.oSec01Field03 : machine.oSec01Field04,
#                 machine.oSec01Field05 : machine.oSec01Field06,
#                 machine.oSec01Field07 : machine.oSec01Field08,
#                 machine.oSec01Field09 : machine.oSec01Field10,
#             }

#             for key, value in machine_data.items():
#                 row_cells = machine_table.add_row().cells
#                 row_cells[0].text = key
#                 row_cells[1].text = str(value)

#             doc.add_paragraph("\n")
#             doc.add_paragraph("Sec02")

#             machine_table = doc.add_table(rows=0, cols=2)

#             machine_data = {
#                 machine.oSec02Field01 : machine.oSec02Field02,
#                 machine.oSec02Field03 : machine.oSec02Field04,
#                 machine.oSec02Field05 : machine.oSec02Field06,
#                 machine.oSec02Field07 : machine.oSec02Field08,
#                 machine.oSec02Field09 : machine.oSec02Field10,
#             }

#             for key, value in machine_data.items():
#                 row_cells = machine_table.add_row().cells
#                 row_cells[0].text = key
#                 row_cells[1].text = str(value)

#             doc.add_paragraph("\n")
#             doc.add_paragraph("Sec03")

#             machine_table = doc.add_table(rows=0, cols=2)

#             machine_data = {
#                 machine.oSec03Field01 : machine.oSec03Field02,
#                 machine.oSec03Field03 : machine.oSec03Field04,
#                 machine.oSec03Field05 : machine.oSec03Field06,
#                 machine.oSec03Field07 : machine.oSec03Field08,
#                 machine.oSec03Field09 : machine.oSec03Field10,
#             }

#             for key, value in machine_data.items():
#                 row_cells = machine_table.add_row().cells
#                 row_cells[0].text = key
#                 row_cells[1].text = str(value)

#             doc.add_paragraph("\n")

#         # Save the document to a response
#         response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.wordprocessingml.document')
#         response['Content-Disposition'] = f'attachment; filename={project.name}_report.docx'
#         doc.save(response)
#         return response

#     except Project.DoesNotExist:
#         return HttpResponse("Project not found", status=404)








from django.http import HttpResponse
from docx import Document
from docx.shared import Pt, RGBColor
from docx.enum.text import WD_PARAGRAPH_ALIGNMENT
from docx.oxml import OxmlElement, ns
from .models import Project, Machine  # Assuming these models exist
from docx.shared import Inches

def add_header_footer(doc):
    """Adds header and footer with page numbers in the format 'Page X of Y'."""
    section = doc.sections[0]

    # Header
    header = section.header
    header_para = header.paragraphs[0] if header.paragraphs else header.add_paragraph()
    header_para.add_run("Company Name\n")
    header_para.add_run("Project Name\n")
    header_para.add_run("Date: " + datetime.now().strftime('%Y-%m-%d %H:%M:%S') + "\n")
    header_para.alignment = WD_PARAGRAPH_ALIGNMENT.CENTER

    # Adding logo
    #run_logo = header_para.add_run()  # Corrected reference to header paragraph
    #run_logo.add_picture("Logo.PNG", width=Inches(1.0))  # Adjust width as needed

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
                shading_elm.set(ns.qn("w:fill"), "ADD8E6")  # Light Gray color
                cell._tc.get_or_add_tcPr().append(shading_elm)



from docx.shared import Pt

from docx.shared import Pt

def generate_report(request, project_id):
    """Generates a Word report for a given project."""
    try:
        project = Project.objects.get(id=project_id)
        machines = Machine.objects.filter(project=project)

        # Create a Word document
        doc = Document()

        # Add header and footer with page numbers
        add_header_footer(doc)

        # Add project title
        doc.add_heading(f'Project Report: {project.name}', level=1)

        # Add project details
        doc.add_heading("Project Details", level=2)

        project_data = [
            ("Field", "Value"),
            ("Name", project.name),
            ("Client Name", project.client_name),
            ("Capacity", project.capacity),
        ]
        add_table(doc, project_data)     

        doc.add_paragraph("\n")
        doc.add_page_break()     
        doc.add_paragraph("\n")

        # Add machine details
        for index, machine in enumerate(machines, start=1):  # Add numbering
            machine_name = machine.oSec00Field03
            section_titles = []

            if machine_name == "DataSheetNS":
                machine_name = "Manual Screen" 
                section_titles = ["General Data", "Design Data", "Material Data", "Channel Data", " ", " ", " ", " ", " ", " "]

            if machine_name == "DataSheetMSc":
                machine_name = "Mechanical Screen" 
                section_titles = ["General Data", "Design Data", "Gearmotor Data", "Control panel Data", "Material Data", "Other Data", " ", " ", " ", " "]

            if machine_name == "DataSheetBC":
                machine_name = "Belt Conveyor"
                section_titles = ["General Data", "Design Data", "Gearbox Data", "Motor Data", "Material Data", " ", " ", " ", " ", " "]

            if machine_name == "DataSheetCO":
                machine_name = "Container"
                section_titles = ["General Data", "Design Data", "Material Data", " ", " ", " ", " ", " ", " ", " "]

            if machine_name == "DataSheetGR":
                machine_name = "Gritremoval"
                section_titles = ["General Data", "Design Data", "Walkway, Handrail, Wheel Data", "Scrapper Data", "Gearmotor Data", "Scrapper Data", "Drive unit", "Control panel Data", "Material Data ", " "]

            if machine_name == "DataSheetSS":
                machine_name = "Sand Silo"

            if machine_name == "DataSheetPS":
                machine_name = "Primary Sedimentation"

            if machine_name == "DataSheetQV":
                machine_name = "Quick Valve"

            if machine_name == "DataSheetTV":
                machine_name = "Telescopic Valve"
                
            if machine_name == "DataSheetTH":
                machine_name = "Sludge Thickener"

            # Add machine title with font size 14 and numbering
            machine_title = doc.add_paragraph(f"{index}. {machine_name}", style="Heading3")
            machine_title.runs[0].font.size = Pt(14)

            for i in range(1, 11):  # Loop from Sec01 to Sec10
                section_name = f"Sec{i:02d}"
                section_data = [("Field", "Value")]

                for j in range(1, 21, 2):  # Step by 2 to avoid duplication
                    key = getattr(machine, f"o{section_name}Field{j:02d}", "").strip()
                    value = getattr(machine, f"o{section_name}Field{j+1:02d}", "").strip()

                    if key and value and key.lower() != "oooo" and value.lower() != "oooo":
                        section_data.append((key, value))

                if len(section_data) > 1:  # If the section has valid data, create a table
                    section_title = section_titles[i-1] if i-1 < len(section_titles) else f"Section {i}"
                    doc.add_paragraph(f"{section_name}: {section_title}", style="Heading3")  # Only one title now

                    add_table(doc, section_data)  # Removed redundant title

            doc.add_page_break()     

        # Save the document to a response
        response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.wordprocessingml.document')
        response['Content-Disposition'] = f'attachment; filename={project.name}_report.docx'
        doc.save(response)
        return response

    except Project.DoesNotExist:
        return HttpResponse("Project not found", status=404)






###
###



def assign_user_to_company(request):
    if request.method == "POST":
        form = UserCompanyForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("assign_user_to_company")  # Redirect to a success page
    else:
        form = UserCompanyForm()
    
    return render(request, "assign_user_to_company.html", {"form": form})





###
###





def DataSheetNS_Save(request):
    print(">>> Save_DataSheetNS view called")  # Debugging

    if request.method == 'POST' and 'form_DataSheetNS_submit' in request.POST:
        print(">>> Received POST request")  # Debugging

        form_DataSheetNS = FDS_NS(request.POST)

        if form_DataSheetNS.is_valid():
            print(">>> Form is valid")  # Debugging

            instance = form_DataSheetNS.save(commit=False)  # Do not save yet

            # Assign required fields
            instance.oSec00Field01 = request.user.username  # Username
            instance.oSec00Field02 = datetime.now().strftime('%Y-%m-%d %H:%M:%S')  # Timestamp
            instance.oSec00Field03 = "DataSheetNS"  # Fixed type

            # Ensure a project is assigned before saving
            project_id = request.POST.get('project')  # Get project_id from form
            if project_id:
                try:
                    instance.project = Project.objects.get(id=project_id)  # Assign project
                except Project.DoesNotExist:
                    print(">>> Error: Project ID not found")  # Debugging
                    return render(request, 'PageDataSheet_ManualScreen.html', {
                        'form_DataSheetNS': form_DataSheetNS,
                        'error': 'Invalid Project ID'
                    })

            else:
                print(">>> Error: No Project ID provided")  # Debugging
                return render(request, 'PageDataSheet_ManualScreen.html', {
                    'form_DataSheetNS': form_DataSheetNS,
                    'error': 'Project is required'
                })

            # Save the instance
            instance.save()
            print(">>> Data Saved Successfully")  # Debugging

            # Refresh the form with initial values
            form_DataSheetNS = FDS_NS(initial=form_DataSheetNS.cleaned_data)
            
            machines = Machine.objects.filter(oSec00Field03="DataSheetNS")
            


            return render(request, 'PageDataSheet_ManualScreen.html', {
                'form': form_DataSheetNS,
                'success': 'Data saved successfully!',
                "machines": machines
            })

        else:
            print(">>> Form is NOT valid:", form_DataSheetNS.errors)  # Debugging
            return render(request, 'PageDataSheet_ManualScreen.html', {
                'form_DataSheetNS': form_DataSheetNS,
                'error': 'Form contains errors',
                "machines": machines
            })

    print(">>> Invalid request, redirecting to ms_load")  # Debugging
    return redirect('ms_load')


def DataSheetNS_Delete(request, machine_id):
    machine = get_object_or_404(Machine, id=machine_id)
    machine.delete()
    
    # Redirect to the 'load_data_sheet' view with sheet_key='A'
    return redirect(reverse('load_data_sheet', kwargs={'sheet_key': 'A'}))


def DataSheetNS_edit(request, id):
    machine = get_object_or_404(Machine, id=id)  # Fetch the machine instance
    if request.method == "POST":
        form = formDataSheetNS(request.POST, instance=machine)  # Bind the existing instance
        if form.is_valid():
            form.save()  # Save updates
            return redirect('load_DataSheetNS')  # Redirect to list page
    else:
        form = formDataSheetNS(instance=machine)  # Load form with existing data
    
    return render(request, 'PageNS_DataSheet_edit.html', {'form': form, 'machine': machine})


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
        # Add other fields if necessary
    }

    return JsonResponse(data)



###
###
###
###












# Mapping of keys to form classes and templates
DATA_SHEET_CONFIG = {
    "A":    {"form_class": FDS_NS,  "template": "PageDataSheet_ManualScreen.html",              "needs_user": True, "DB_Name": "DataSheetNS"},
    "B":    {"form_class": FDS_BS,  "template": "PageDataSheet_BasketScreen.html",              "needs_user": True, "DB_Name": "DataSheetBS"},
    "C":    {"form_class": FDS_MSc, "template": "PageDataSheet_MechanicalCoarseScreen.html",    "needs_user": True, "DB_Name": "DataSheetMSc"},
    "D":    {"form_class": FDS_MSf, "template": "PageDataSheet_MechanicalFineScreen.html",      "needs_user": True, "DB_Name": "DataSheetMSf"},
    "E":    {"form_class": FDS_BC,  "template": "PageDataSheet_BeltConveyor.html",              "needs_user": True, "DB_Name": "DataSheetBC"},
    "F":    {"form_class": FDS_SC,  "template": "PageDataSheet_ScrewConveyor.html",             "needs_user": True, "DB_Name": "DataSheetSC"},
    "G":    {"form_class": FDS_CO,  "template": "PageDataSheet_Container.html",                 "needs_user": True, "DB_Name": "DataSheetCO"},
    "H":    {"form_class": FDS_GR,  "template": "PageDataSheet_GritGreaseRemoval.html",         "needs_user": True, "DB_Name": "DataSheetGR"},
    "I":    {"form_class": FDS_SS,  "template": "PageDataSheet_SandSilo.html",                  "needs_user": True, "DB_Name": "DataSheetSS"},
    "J":    {"form_class": FDS_PS,  "template": "PageDataSheet_PrimarySedimentationTank.html",  "needs_user": True, "DB_Name": "DataSheetPS"},
    "K":    {"form_class": FDS_QV,  "template": "PageDataSheet_QuickValve.html",                "needs_user": True, "DB_Name": "DataSheetQV"},
    "L":    {"form_class": FDS_TV,  "template": "PageDataSheet_TelescopicValve.html",           "needs_user": True, "DB_Name": "DataSheetTV"},
    "M":    {"form_class": FDS_TH,  "template": "PageDataSheet_SludgeThickener.html",           "needs_user": True, "DB_Name": "DataSheetTH"},
    "N":    {"form_class": FDS_MX,  "template": "PageDataSheet_Mixers.html",                    "needs_user": True, "DB_Name": "DataSheetMX"},
    "O":    {"form_class": FDS_TA,  "template": "PageDataSheet_Tanks.html",                     "needs_user": True, "DB_Name": "DataSheetTA"},
}


from django.shortcuts import render, get_object_or_404
from .models import Machine, UserCompany  # Import your models

def load_data_sheet(request, sheet_key):
    ###LOG
    aLogEntry.objects.create(
            user=request.user,
            message=f"at {now()} {request.user} accessed Load {sheet_key} "
        )
    print(f"at {now()} {User} accessed Load {sheet_key} ")
    ###LOG

    print(UserCompany.objects.get(user=request.user).company)

    if not request.user.is_authenticated:
        return redirect("login")  # Redirect unauthenticated users

    config = config = DATA_SHEET_CONFIG.get(sheet_key)
    if not config:
        return redirect("some_error_page")  # Handle invalid keys

    form_class = config["form_class"]
    template = config["template"]
    needs_user = config["needs_user"]
    DB_Name = config["DB_Name"]

    # Get the company of the logged-in user
    user_company = None
    if request.user.is_authenticated:
        try:
            user_company = UserCompany.objects.get(user=request.user).company
        except UserCompany.DoesNotExist:
            user_company = None

    # Assign company filter only if the user has a company
    if user_company:
        machines = Machine.objects.filter(oSec00Field03=DB_Name, company=user_company)
        projects = Project.objects.filter(company=user_company)
    else:
        machines = Machine.objects.none()  # Return an empty queryset if no company
        projects = Project.objects.none()  # Return an empty queryset if no company

    # If the form needs user association, provide it
    form = form_class() if not needs_user else form_class(user=request.user)
    
    print(projects)

    return render(request, template, {
    "form": form,
    "machines": machines,
    "projects": projects,  
    "user_company": user_company,
})






# Mapping between data types and their respective forms and templates
DATA_SHEET_CONFIG_BBB = {
    "AA":    {"form_class": FDS_NS,  "template": "PageDataSheet_ManualScreen.html",              "needs_user": True, "DB_Name": "DataSheetNS"},
    "BB":    {"form_class": FDS_BS,  "template": "PageDataSheet_BasketScreen.html",              "needs_user": True, "DB_Name": "DataSheetBS"},
    "CC":    {"form_class": FDS_MSc, "template": "PageDataSheet_MechanicalCoarseScreen.html",    "needs_user": True, "DB_Name": "DataSheetMSc"},
    "DD":    {"form_class": FDS_MSf, "template": "PageDataSheet_MechanicalFineScreen.html",      "needs_user": True, "DB_Name": "DataSheetMSf"},
    "EE":    {"form_class": FDS_BC,  "template": "PageDataSheet_BeltConveyor.html",              "needs_user": True, "DB_Name": "DataSheetBC"},
    "FF":    {"form_class": FDS_SC,  "template": "PageDataSheet_ScrewConveyor.html",             "needs_user": True, "DB_Name": "DataSheetSC"},
    "GG":    {"form_class": FDS_CO,  "template": "PageDataSheet_Container.html",                 "needs_user": True, "DB_Name": "DataSheetCO"},
    "HH":    {"form_class": FDS_GR,  "template": "PageDataSheet_GritGreaseRemoval.html",         "needs_user": True, "DB_Name": "DataSheetGR"},
    "II":    {"form_class": FDS_SS,  "template": "PageDataSheet_SandSilo.html",                  "needs_user": True, "DB_Name": "DataSheetSS"},
    "JJ":    {"form_class": FDS_PS,  "template": "PageDataSheet_PrimarySedimentationTank.html",  "needs_user": True, "DB_Name": "DataSheetPS"},
    "KK":    {"form_class": FDS_QV,  "template": "PageDataSheet_QuickValve.html",                "needs_user": True, "DB_Name": "DataSheetQV"},
    "LL":    {"form_class": FDS_TV,  "template": "PageDataSheet_TelescopicValve.html",           "needs_user": True, "DB_Name": "DataSheetTV"},
    "MM":    {"form_class": FDS_TH,  "template": "PageDataSheet_SludgeThickener.html",           "needs_user": True, "DB_Name": "DataSheetTH"},
    "NN":    {"form_class": FDS_MX,  "template": "PageDataSheet_Mixers.html",                    "needs_user": True, "DB_Name": "DataSheetMX"},
    "OO":    {"form_class": FDS_TA,  "template": "PageDataSheet_Tanks.html",                     "needs_user": True, "DB_Name": "DataSheetTA"},
}



from django.shortcuts import render, redirect
from datetime import datetime
from .models import Machine, Project, UserCompany  # Import necessary models

def save_data_sheet(request, data_type):
    
    ###LOG
    aLogEntry.objects.create(
            user=request.user,
            message=f"at {now()} {request.user} accessed Save {data_type} "
        )    
    ###LOG
    

    if not request.user.is_authenticated:
        return redirect("ms_load")  # Redirect if user is not logged in

    if data_type not in DATA_SHEET_CONFIG_BBB:
        return redirect("ms_load")  # Redirect if data type is invalid

    config = DATA_SHEET_CONFIG_BBB[data_type]
    form_class = config["form_class"]
    template = config["template"]
    DB_Name = config["DB_Name"]

    if request.method == "POST":
        form = form_class(request.POST)

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
                    return render(request, template, {"form": form, "error": "Invalid Project ID"})
            else:
                return render(request, template, {"form": form, "error": "Project is required"})

            # Get the company associated with the user
            try:
                user_company = UserCompany.objects.get(user=request.user).company
                instance.company = user_company  # Assign company to the instance
            except UserCompany.DoesNotExist:
                return render(request, template, {"form": form, "error": "User is not associated with a company"})

            # Save the instance to the database
            instance.save()

            # Refresh form with initial values
            form = form_class(initial=form.cleaned_data)

            # Filter machines by the user’s company
            machines = Machine.objects.filter(oSec00Field03=DB_Name, company=user_company)

            return render(request, template, {"form": form, "success": "Data saved successfully!", "machines": machines})

        else:
            # If the form has errors, return all machines for this DB_Name (no company filtering)
            machines = Machine.objects.filter(oSec00Field03=DB_Name)
            return render(request, template, {"form": form, "error": "Form contains errors", "machines": machines})

    return redirect("ms_load")  # Redirect for invalid requests




def General_DXF_NS(request, aMachine_ID):
    ###LOG
    aLogEntry.objects.create(
            user=request.user,
            message=f"at {now()} {request.user} Download DXF NS {aMachine_ID} "
        )
    
    ###LOG
    ###### Get the company ######
    user_company = None
    if request.user.is_authenticated:
        try:
            user_company = UserCompany.objects.get(user=request.user).company
        except UserCompany.DoesNotExist:
            user_company = None
            
    ###### Get the company ######
    
    print(aMachine_ID)
    
    machine = Machine.objects.get(id=aMachine_ID)
    print(machine.oSec02Field04)
    print(machine.oSec02Field06)    
    
    if request.method == "POST":
        # Define the path to the DXF file in the static directory
        static_path = os.path.join(settings.BASE_DIR, "static", "aDxfs", "NS.dxf")
        modified_path = os.path.join(settings.BASE_DIR, "static", "aDxfs", "NS_new.dxf")
               
        # Load the DXF file
        doc = ezdxf.readfile(static_path)

        # Iterate over the modelspace to find all DIMENSION entities
        for entity in doc.modelspace().query("DIMENSION"):
            if entity.dxf.text == "ScreenLength":
                #entity.dxf.text = request.POST.get("oSec01Field01", "000")
                entity.dxf.text = machine.oSec02Field06
            elif entity.dxf.text == "BarLength":
                entity.dxf.text = "500"
            elif entity.dxf.text == "ScreenWidth":
                entity.dxf.text = machine.oSec02Field04
            elif entity.dxf.text == "BarTh":
                entity.dxf.text = "10"
            elif entity.dxf.text == "BarSpacing":
                entity.dxf.text = machine.oSec02Field10
                            
            
            # Update text height and arrow size via dimstyle
            dimstyle_name = entity.dxf.dimstyle
            dimstyle = doc.dimstyles.get(dimstyle_name)
            if dimstyle:
                dimstyle.dxf.dimtxt = 0.1  # Set text height
                dimstyle.dxf.dimasz = 0.1  # Set arrow size

            # Render the dimension to apply changes
            entity.render()

        # Save the modified DXF file
        doc.saveas(modified_path)

        # Serve the modified file for download
        with open(modified_path, "rb") as dxf_file:
            response = HttpResponse(dxf_file.read(), content_type="application/dxf")
            response["Content-Disposition"] = 'attachment; filename="NS_new_new.dxf"'
            return response

    return HttpResponse("Invalid request", status=400)




def General_DXF_MS(request, aMachine_ID):
    print(aMachine_ID)
    if request.method == "POST":
        # Define the path to the DXF file in the static directory
        static_path = os.path.join(settings.BASE_DIR, "static", "aDxfs", "MS.dxf")
        modified_path = os.path.join(settings.BASE_DIR, "static", "aDxfs", "MS_new.dxf")
               
        # Load the DXF file
        doc = ezdxf.readfile(static_path)

        # Iterate over the modelspace to find all DIMENSION entities
        for entity in doc.modelspace().query("DIMENSION"):
            if entity.dxf.text == "ScreenLength":
                #entity.dxf.text = request.POST.get("oSec01Field01", "000")
                entity.dxf.text = "1000"
            elif entity.dxf.text == "BarLength":
                entity.dxf.text = "500"
            elif entity.dxf.text == "ScreenWidth":
                entity.dxf.text = "600"
            elif entity.dxf.text == "BarTh":
                entity.dxf.text = "10"
            elif entity.dxf.text == "BarSpacing":
                entity.dxf.text = "25"
                            
            
            # Update text height and arrow size via dimstyle
            dimstyle_name = entity.dxf.dimstyle
            dimstyle = doc.dimstyles.get(dimstyle_name)
            if dimstyle:
                dimstyle.dxf.dimtxt = 0.1  # Set text height
                dimstyle.dxf.dimasz = 0.1  # Set arrow size

            # Render the dimension to apply changes
            entity.render()

        # Save the modified DXF file
        doc.saveas(modified_path)

        # Serve the modified file for download
        with open(modified_path, "rb") as dxf_file:
            response = HttpResponse(dxf_file.read(), content_type="application/dxf")
            response["Content-Disposition"] = 'attachment; filename="MS_new_new.dxf"'
            return response

    return HttpResponse("Invalid request", status=400)




def General_DXF_BC(request, aMachine_ID):
    print(aMachine_ID)
    if request.method == "POST":
        # Define the path to the DXF file in the static directory
        static_path = os.path.join(settings.BASE_DIR, "static", "aDxfs", "BC.dxf")
        modified_path = os.path.join(settings.BASE_DIR, "static", "aDxfs", "BC_new.dxf")
               
        # Load the DXF file
        doc = ezdxf.readfile(static_path)

        # Iterate over the modelspace to find all DIMENSION entities
        for entity in doc.modelspace().query("DIMENSION"):
            if entity.dxf.text == "ScreenLength":
                #entity.dxf.text = request.POST.get("oSec01Field01", "000")
                entity.dxf.text = "1000"
            elif entity.dxf.text == "BarLength":
                entity.dxf.text = "500"
            elif entity.dxf.text == "ScreenWidth":
                entity.dxf.text = "600"
            elif entity.dxf.text == "BarTh":
                entity.dxf.text = "10"
            elif entity.dxf.text == "BarSpacing":
                entity.dxf.text = "25"
                            
            
            # Update text height and arrow size via dimstyle
            dimstyle_name = entity.dxf.dimstyle
            dimstyle = doc.dimstyles.get(dimstyle_name)
            if dimstyle:
                dimstyle.dxf.dimtxt = 0.1  # Set text height
                dimstyle.dxf.dimasz = 0.1  # Set arrow size

            # Render the dimension to apply changes
            entity.render()

        # Save the modified DXF file
        doc.saveas(modified_path)

        # Serve the modified file for download
        with open(modified_path, "rb") as dxf_file:
            response = HttpResponse(dxf_file.read(), content_type="application/dxf")
            response["Content-Disposition"] = 'attachment; filename="BC_new_new.dxf"'
            return response

    return HttpResponse("Invalid request", status=400)



def General_DXF_CO(request, aMachine_ID):
    print(aMachine_ID)
    if request.method == "POST":
        # Define the path to the DXF file in the static directory
        static_path = os.path.join(settings.BASE_DIR, "static", "aDxfs", "CO.dxf")
        modified_path = os.path.join(settings.BASE_DIR, "static", "aDxfs", "CO_new.dxf")
               
        # Load the DXF file
        doc = ezdxf.readfile(static_path)

        # Iterate over the modelspace to find all DIMENSION entities
        for entity in doc.modelspace().query("DIMENSION"):
            if entity.dxf.text == "ScreenLength":
                #entity.dxf.text = request.POST.get("oSec01Field01", "000")
                entity.dxf.text = "1000"
            elif entity.dxf.text == "BarLength":
                entity.dxf.text = "500"
            elif entity.dxf.text == "ScreenWidth":
                entity.dxf.text = "600"
            elif entity.dxf.text == "BarTh":
                entity.dxf.text = "10"
            elif entity.dxf.text == "BarSpacing":
                entity.dxf.text = "25"
                            
            
            # Update text height and arrow size via dimstyle
            dimstyle_name = entity.dxf.dimstyle
            dimstyle = doc.dimstyles.get(dimstyle_name)
            if dimstyle:
                dimstyle.dxf.dimtxt = 0.1  # Set text height
                dimstyle.dxf.dimasz = 0.1  # Set arrow size

            # Render the dimension to apply changes
            entity.render()

        # Save the modified DXF file
        doc.saveas(modified_path)

        # Serve the modified file for download
        with open(modified_path, "rb") as dxf_file:
            response = HttpResponse(dxf_file.read(), content_type="application/dxf")
            response["Content-Disposition"] = 'attachment; filename="CO_new_new.dxf"'
            return response

    return HttpResponse("Invalid request", status=400)




def General_DXF_GR(request, aMachine_ID):
    print(aMachine_ID)
    if request.method == "POST":
        # Define the path to the DXF file in the static directory
        static_path = os.path.join(settings.BASE_DIR, "static", "aDxfs", "GR.dxf")
        modified_path = os.path.join(settings.BASE_DIR, "static", "aDxfs", "GR_new.dxf")
               
        # Load the DXF file
        doc = ezdxf.readfile(static_path)

        # Iterate over the modelspace to find all DIMENSION entities
        for entity in doc.modelspace().query("DIMENSION"):
            if entity.dxf.text == "ScreenLength":
                #entity.dxf.text = request.POST.get("oSec01Field01", "000")
                entity.dxf.text = "1000"
            elif entity.dxf.text == "BarLength":
                entity.dxf.text = "500"
            elif entity.dxf.text == "ScreenWidth":
                entity.dxf.text = "600"
            elif entity.dxf.text == "BarTh":
                entity.dxf.text = "10"
            elif entity.dxf.text == "BarSpacing":
                entity.dxf.text = "25"
                            
            
            # Update text height and arrow size via dimstyle
            dimstyle_name = entity.dxf.dimstyle
            dimstyle = doc.dimstyles.get(dimstyle_name)
            if dimstyle:
                dimstyle.dxf.dimtxt = 0.1  # Set text height
                dimstyle.dxf.dimasz = 0.1  # Set arrow size

            # Render the dimension to apply changes
            entity.render()

        # Save the modified DXF file
        doc.saveas(modified_path)

        # Serve the modified file for download
        with open(modified_path, "rb") as dxf_file:
            response = HttpResponse(dxf_file.read(), content_type="application/dxf")
            response["Content-Disposition"] = 'attachment; filename="GR_new_new.dxf"'
            return response

    return HttpResponse("Invalid request", status=400)




def General_DXF_SS(request, aMachine_ID):
    print(aMachine_ID)
    if request.method == "POST":
        # Define the path to the DXF file in the static directory
        static_path = os.path.join(settings.BASE_DIR, "static", "aDxfs", "SS.dxf")
        modified_path = os.path.join(settings.BASE_DIR, "static", "aDxfs", "SS_new.dxf")
               
        # Load the DXF file
        doc = ezdxf.readfile(static_path)

        # Iterate over the modelspace to find all DIMENSION entities
        for entity in doc.modelspace().query("DIMENSION"):
            if entity.dxf.text == "ScreenLength":
                #entity.dxf.text = request.POST.get("oSec01Field01", "000")
                entity.dxf.text = "1000"
            elif entity.dxf.text == "BarLength":
                entity.dxf.text = "500"
            elif entity.dxf.text == "ScreenWidth":
                entity.dxf.text = "600"
            elif entity.dxf.text == "BarTh":
                entity.dxf.text = "10"
            elif entity.dxf.text == "BarSpacing":
                entity.dxf.text = "25"
                            
            
            # Update text height and arrow size via dimstyle
            dimstyle_name = entity.dxf.dimstyle
            dimstyle = doc.dimstyles.get(dimstyle_name)
            if dimstyle:
                dimstyle.dxf.dimtxt = 0.1  # Set text height
                dimstyle.dxf.dimasz = 0.1  # Set arrow size

            # Render the dimension to apply changes
            entity.render()

        # Save the modified DXF file
        doc.saveas(modified_path)

        # Serve the modified file for download
        with open(modified_path, "rb") as dxf_file:
            response = HttpResponse(dxf_file.read(), content_type="application/dxf")
            response["Content-Disposition"] = 'attachment; filename="SS_new_new.dxf"'
            return response

    return HttpResponse("Invalid request", status=400)




def General_DXF_PST(request, aMachine_ID):
    print(aMachine_ID)
    if request.method == "POST":
        # Define the path to the DXF file in the static directory
        static_path = os.path.join(settings.BASE_DIR, "static", "aDxfs", "PST.dxf")
        modified_path = os.path.join(settings.BASE_DIR, "static", "aDxfs", "PST_new.dxf")
               
        # Load the DXF file
        doc = ezdxf.readfile(static_path)

        # Iterate over the modelspace to find all DIMENSION entities
        for entity in doc.modelspace().query("DIMENSION"):
            if entity.dxf.text == "ScreenLength":
                #entity.dxf.text = request.POST.get("oSec01Field01", "000")
                entity.dxf.text = "1000"
            elif entity.dxf.text == "BarLength":
                entity.dxf.text = "500"
            elif entity.dxf.text == "ScreenWidth":
                entity.dxf.text = "600"
            elif entity.dxf.text == "BarTh":
                entity.dxf.text = "10"
            elif entity.dxf.text == "BarSpacing":
                entity.dxf.text = "25"
                            
            
            # Update text height and arrow size via dimstyle
            dimstyle_name = entity.dxf.dimstyle
            dimstyle = doc.dimstyles.get(dimstyle_name)
            if dimstyle:
                dimstyle.dxf.dimtxt = 0.1  # Set text height
                dimstyle.dxf.dimasz = 0.1  # Set arrow size

            # Render the dimension to apply changes
            entity.render()

        # Save the modified DXF file
        doc.saveas(modified_path)

        # Serve the modified file for download
        with open(modified_path, "rb") as dxf_file:
            response = HttpResponse(dxf_file.read(), content_type="application/dxf")
            response["Content-Disposition"] = 'attachment; filename="PST_new_new.dxf"'
            return response

    return HttpResponse("Invalid request", status=400)




def General_DXF_QV(request, aMachine_ID):
    print(aMachine_ID)
    if request.method == "POST":
        # Define the path to the DXF file in the static directory
        static_path = os.path.join(settings.BASE_DIR, "static", "aDxfs", "QV.dxf")
        modified_path = os.path.join(settings.BASE_DIR, "static", "aDxfs", "QV_new.dxf")
               
        # Load the DXF file
        doc = ezdxf.readfile(static_path)

        # Iterate over the modelspace to find all DIMENSION entities
        for entity in doc.modelspace().query("DIMENSION"):
            if entity.dxf.text == "ScreenLength":
                #entity.dxf.text = request.POST.get("oSec01Field01", "000")
                entity.dxf.text = "1000"
            elif entity.dxf.text == "BarLength":
                entity.dxf.text = "500"
            elif entity.dxf.text == "ScreenWidth":
                entity.dxf.text = "600"
            elif entity.dxf.text == "BarTh":
                entity.dxf.text = "10"
            elif entity.dxf.text == "BarSpacing":
                entity.dxf.text = "25"
                            
            
            # Update text height and arrow size via dimstyle
            dimstyle_name = entity.dxf.dimstyle
            dimstyle = doc.dimstyles.get(dimstyle_name)
            if dimstyle:
                dimstyle.dxf.dimtxt = 0.1  # Set text height
                dimstyle.dxf.dimasz = 0.1  # Set arrow size

            # Render the dimension to apply changes
            entity.render()

        # Save the modified DXF file
        doc.saveas(modified_path)

        # Serve the modified file for download
        with open(modified_path, "rb") as dxf_file:
            response = HttpResponse(dxf_file.read(), content_type="application/dxf")
            response["Content-Disposition"] = 'attachment; filename="QV_new_new.dxf"'
            return response

    return HttpResponse("Invalid request", status=400)




def General_DXF_TV(request, aMachine_ID):
    print(aMachine_ID)
    if request.method == "POST":
        # Define the path to the DXF file in the static directory
        static_path = os.path.join(settings.BASE_DIR, "static", "aDxfs", "TV.dxf")
        modified_path = os.path.join(settings.BASE_DIR, "static", "aDxfs", "TV_new.dxf")
               
        # Load the DXF file
        doc = ezdxf.readfile(static_path)

        # Iterate over the modelspace to find all DIMENSION entities
        for entity in doc.modelspace().query("DIMENSION"):
            if entity.dxf.text == "ScreenLength":
                #entity.dxf.text = request.POST.get("oSec01Field01", "000")
                entity.dxf.text = "1000"
            elif entity.dxf.text == "BarLength":
                entity.dxf.text = "500"
            elif entity.dxf.text == "ScreenWidth":
                entity.dxf.text = "600"
            elif entity.dxf.text == "BarTh":
                entity.dxf.text = "10"
            elif entity.dxf.text == "BarSpacing":
                entity.dxf.text = "25"
                            
            
            # Update text height and arrow size via dimstyle
            dimstyle_name = entity.dxf.dimstyle
            dimstyle = doc.dimstyles.get(dimstyle_name)
            if dimstyle:
                dimstyle.dxf.dimtxt = 0.1  # Set text height
                dimstyle.dxf.dimasz = 0.1  # Set arrow size

            # Render the dimension to apply changes
            entity.render()

        # Save the modified DXF file
        doc.saveas(modified_path)

        # Serve the modified file for download
        with open(modified_path, "rb") as dxf_file:
            response = HttpResponse(dxf_file.read(), content_type="application/dxf")
            response["Content-Disposition"] = 'attachment; filename="TV_new_new.dxf"'
            return response

    return HttpResponse("Invalid request", status=400)




def General_DXF_TH(request, aMachine_ID):
    print(aMachine_ID)
    if request.method == "POST":
        # Define the path to the DXF file in the static directory
        static_path = os.path.join(settings.BASE_DIR, "static", "aDxfs", "TH.dxf")
        modified_path = os.path.join(settings.BASE_DIR, "static", "aDxfs", "TH_new.dxf")
               
        # Load the DXF file
        doc = ezdxf.readfile(static_path)

        # Iterate over the modelspace to find all DIMENSION entities
        for entity in doc.modelspace().query("DIMENSION"):
            if entity.dxf.text == "ScreenLength":
                #entity.dxf.text = request.POST.get("oSec01Field01", "000")
                entity.dxf.text = "1000"
            elif entity.dxf.text == "BarLength":
                entity.dxf.text = "500"
            elif entity.dxf.text == "ScreenWidth":
                entity.dxf.text = "600"
            elif entity.dxf.text == "BarTh":
                entity.dxf.text = "10"
            elif entity.dxf.text == "BarSpacing":
                entity.dxf.text = "25"
                            
            
            # Update text height and arrow size via dimstyle
            dimstyle_name = entity.dxf.dimstyle
            dimstyle = doc.dimstyles.get(dimstyle_name)
            if dimstyle:
                dimstyle.dxf.dimtxt = 0.1  # Set text height
                dimstyle.dxf.dimasz = 0.1  # Set arrow size

            # Render the dimension to apply changes
            entity.render()

        # Save the modified DXF file
        doc.saveas(modified_path)

        # Serve the modified file for download
        with open(modified_path, "rb") as dxf_file:
            response = HttpResponse(dxf_file.read(), content_type="application/dxf")
            response["Content-Disposition"] = 'attachment; filename="TH_new_new.dxf"'
            return response

    return HttpResponse("Invalid request", status=400)


