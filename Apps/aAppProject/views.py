from django.shortcuts import render

from config import settings
from django_q.tasks import async_task
from django_q.models import Task
from .tasks import save_reports_task
from .forms import ProjectForm
from .models import APP_Project
from .models import ReportProgress
from .reports import word_submittal_report, word_calculation_report
from .drive import create_folder, service, check_folder_exists, get_folder_id_by_name, upload_files, get_file_ids_in_folder, download_file, download_file_as_bytes, upload_files_directly
from Apps.aAppMechanical.models import UserCompany
from Apps.aAppSubmittal.models import Machine
from Apps.aAppSubmittal.models import AddMachine
from Apps.aAppMechanical.models import aLogEntry
from Apps.aAppCalculation.models import modelcalc
from Apps.aAppSubmittal.views import get_user_company

import requests
import time


from django.http import FileResponse, HttpResponse
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.shortcuts import render, redirect
from django.utils.timezone import now 
from django.contrib.auth.models import User



import zipfile
from django.utils.text import slugify
from io import BytesIO


import os
import ezdxf

from docx import Document
from docx.shared import Pt, RGBColor
from docx.enum.text import WD_PARAGRAPH_ALIGNMENT,  WD_ALIGN_PARAGRAPH
from docx.oxml import OxmlElement, ns
from docx.shared import Inches
from docx.shared import Pt

from fpdf import FPDF
from PyPDF2 import PdfReader, PdfWriter
from reportlab.pdfgen import canvas
from openpyxl import Workbook

# Create your views here.



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


            instance.save()  # Save the instance (now with company info)

            # Create folder inside the company's directory in the static folder
            company_slug = slugify(instance.company.nameCompanies)  
            company_name = instance.company.nameCompanies
            project_name = slugify(instance.name)       
            
            
            try:
                theproject = APP_Project.objects.get(id = instance.id)
            except APP_Project.DoesNotExist:
                print(f"Skipping project '{project_name}' : not found in APP_Project.")
            
            project_id = theproject.id
            folder_name = f"{project_id}_{company_slug}_{project_name}"

            
            base_static_path = os.path.join(settings.BASE_DIR, 'static', 'aReports')
            company_folder = os.path.join(base_static_path, company_name)
            project_folder = os.path.join(company_folder, folder_name)
            # Create the folders if they don't exist
            os.makedirs(project_folder, exist_ok=True)
            print("project_folder_path : ", project_folder)


            folder_exist, folder_data = check_folder_exists(service, "aReports")
            if folder_exist == True :
                folder_id = folder_data['id']
                company_folder_exist, folder_data = check_folder_exists(service, company_name, folder_id)
                if company_folder_exist == True:
                    company_folder_id = get_folder_id_by_name(service, company_name)
                    create_folder(service, folder_name, company_folder_id)
                else:
                    create_folder(service, company_name, folder_id)
                    company_folder_id = get_folder_id_by_name(service, company_name)
                    create_folder(service, folder_name, company_folder_id)
            else:
                create_folder(service, "aReports")
                folder_id = get_folder_id_by_name(service, "aReports")
                create_folder(service, company_name, folder_id)
                company_folder_id = get_folder_id_by_name(service, company_name)
                create_folder(service, folder_name, company_folder_id)

            
            project_folder_id = get_folder_id_by_name(service, folder_name, company_folder_id)
            
            
            
            print("#######################")
            print("company_name : ", company_name)
            print("#######################")
            
            
            if company_slug == "aaaa":
                for i in range(1 , 6):
                    excel_file_path = os.path.join(project_folder, f'Cost{i}_excel.xlsx')
                    pdf_file_path = os.path.join(project_folder, f'Cost{i}_pdf.pdf')
                    # Create the folders if they don't exist
                    os.makedirs(project_folder, exist_ok=True)

                    ef = Workbook()  # Creates a new workbook with one empty sheet
                    ef.save(excel_file_path)

                    pf = canvas.Canvas(pdf_file_path)
                    pf.showPage()  # Add a blank page
                    pf.save()



                for i in range(1 , 6):
                    excel_buffer = BytesIO()
                    ef = Workbook()  # Creates a new workbook with one empty sheet
                    ef.save(excel_buffer)
                    excel_buffer.seek(0)
                    excel_name = f"Cost{i}_excel.xlsx"
                    excel_mime = 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
                    upload_files_directly(service, excel_buffer, excel_name, excel_mime, project_folder_id)

                    # PDF
                    pdf_buffer = BytesIO()
                    pdf = canvas.Canvas(pdf_buffer)
                    pdf.showPage()
                    pdf.save()
                    pdf_buffer.seek(0)
                    pdf_name = f"Cost{i}_pdf.pdf"
                    pdf_mime = 'application/pdf'
                    upload_files_directly(service, pdf_buffer, pdf_name, pdf_mime, project_folder_id)





            
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
        projects = APP_Project.objects.filter(company=user_company)
    else:
        projects = APP_Project.objects.none()  # Return an empty queryset if no company
    
    #projects = Project.objects.all()
    return render(request, 'project_list.html', {'form': form, 'projects': projects})
 
    
def edit_project(request, project_id):
    project = get_object_or_404(APP_Project, id=project_id)
    
    if request.method == "POST":
        
        form = ProjectForm(request.POST, instance=project)
        if form.is_valid():
            form.save()
            if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                return JsonResponse({'success': True})
            return redirect('project_list')
        else:
            if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                return JsonResponse({'success': False, 'form': form.as_p()})
    else:
        form = ProjectForm(instance=project)
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            return JsonResponse({'success': True, 'form': form.as_p()})

    return render(request, 'edit_project.html', {'form': form})


def delete_project(request, project_id):
    if request.method == "POST":
        project = get_object_or_404(APP_Project, id=project_id)
        
        project.delete()

        # Otherwise, redirect to the project list page
        return redirect('project_list')

    return JsonResponse({'success': False, 'error': 'Invalid request'})


def get_machines(request, project_id):
    try:
        project = APP_Project.objects.get(id=project_id)
        machines = Machine.objects.filter(project=project)

        
        
        data = {
            "project_name": project.name,
            "machines": list(machines.values("oSec00Field01", "oSec00Field02", "oSec00Field03",
                                             "oSec01Field01", "oSec01Field02", "oSec01Field03",
                                             "oSec01Field04", "oSec01Field05", "oSec01Field06",
                                             "oSec01Field07", "oSec01Field08", "oSec01Field09",
                                             "oSec01Field10", "oSec01Field11", "oSec01Field12",
                                             "oSec01Field13", "oSec01Field14", "oSec01Field15",
                                             "oSec01Field16", "oSec01Field17", "oSec01Field18",
                                             "oSec01Field19", "oSec01Field20",
                                             "oSec02Field01", "oSec02Field02", "oSec02Field03",
                                             "oSec02Field04", "oSec02Field05", "oSec02Field06",
                                             "oSec02Field07", "oSec02Field08", "oSec02Field09",
                                             "oSec02Field10", "oSec02Field11", "oSec02Field12",
                                             "oSec02Field13", "oSec02Field14", "oSec02Field15",
                                             "oSec02Field16", "oSec02Field17", "oSec02Field18",
                                             "oSec02Field19", "oSec02Field20",
                                             "oSec03Field01", "oSec03Field02", "oSec03Field03",
                                             "oSec03Field04", "oSec03Field05", "oSec03Field06",
                                             "oSec03Field07", "oSec03Field08", "oSec03Field09",
                                             "oSec03Field10", "oSec03Field11", "oSec03Field12",
                                             "oSec03Field13", "oSec03Field14", "oSec03Field15",
                                             "oSec03Field16", "oSec03Field17", "oSec03Field18",
                                             "oSec03Field19", "oSec03Field20",
                                             "oSec04Field01", "oSec04Field02", "oSec04Field03",
                                             "oSec04Field04", "oSec04Field05", "oSec04Field06",
                                             "oSec04Field07", "oSec04Field08", "oSec04Field09",
                                             "oSec04Field10", "oSec04Field11", "oSec04Field12",
                                             "oSec04Field13", "oSec04Field14", "oSec04Field15",
                                             "oSec04Field16", "oSec04Field17", "oSec04Field18",
                                             "oSec04Field19", "oSec04Field20",
                                             "oSec05Field01", "oSec05Field02", "oSec05Field03",
                                             "oSec05Field04", "oSec05Field05", "oSec05Field06",
                                             "oSec05Field07", "oSec05Field08", "oSec05Field09",
                                             "oSec05Field10", "oSec05Field11", "oSec05Field12",
                                             "oSec05Field13", "oSec05Field14", "oSec05Field15",
                                             "oSec05Field16", "oSec05Field17", "oSec05Field18",
                                             "oSec05Field19", "oSec05Field20",
                                             "oSec06Field01", "oSec06Field02", "oSec06Field03",
                                             "oSec06Field04", "oSec06Field05", "oSec06Field06",
                                             "oSec06Field07", "oSec06Field08", "oSec06Field09",
                                             "oSec06Field10", "oSec06Field11", "oSec06Field12",
                                             "oSec06Field13", "oSec06Field14", "oSec06Field15",
                                             "oSec06Field16", "oSec06Field17", "oSec06Field18",
                                             "oSec06Field19", "oSec06Field20",
                                             "oSec07Field01", "oSec07Field02", "oSec07Field03",
                                             "oSec07Field04", "oSec07Field05", "oSec07Field06",
                                             "oSec07Field07", "oSec07Field08", "oSec07Field09",
                                             "oSec07Field10", "oSec07Field11", "oSec07Field12",
                                             "oSec07Field13", "oSec07Field14", "oSec07Field15",
                                             "oSec07Field16", "oSec07Field17", "oSec07Field18",
                                             "oSec07Field19", "oSec07Field20",
                                             "oSec08Field01", "oSec08Field02", "oSec08Field03",
                                             "oSec08Field04", "oSec08Field05", "oSec08Field06",
                                             "oSec08Field07", "oSec08Field08", "oSec08Field09",
                                             "oSec08Field10", "oSec08Field11", "oSec08Field12",
                                             "oSec08Field13", "oSec08Field14", "oSec08Field15",
                                             "oSec08Field16", "oSec08Field17", "oSec08Field18",
                                             "oSec08Field19", "oSec08Field20",
                                             "oSec09Field01", "oSec09Field02", "oSec09Field03",
                                             "oSec09Field04", "oSec09Field05", "oSec09Field06",
                                             "oSec09Field07", "oSec09Field08", "oSec09Field09",
                                             "oSec09Field10", "oSec09Field11", "oSec09Field12",
                                             "oSec09Field13", "oSec09Field14", "oSec09Field15",
                                             "oSec09Field16", "oSec09Field17", "oSec09Field18",
                                             "oSec09Field19", "oSec09Field20",
                                             "oSec10Field01", "oSec10Field02", "oSec10Field03",
                                             "oSec10Field04", "oSec10Field05", "oSec10Field06",
                                             "oSec10Field07", "oSec10Field08", "oSec10Field09",
                                             "oSec10Field10", "oSec10Field11", "oSec10Field12",
                                             "oSec10Field13", "oSec10Field14", "oSec10Field15",
                                             "oSec10Field16", "oSec10Field17", "oSec10Field18",
                                             "oSec10Field19", "oSec10Field20"))
        }
        return JsonResponse(data)
    except APP_Project.DoesNotExist:
        return JsonResponse({"error": "Project not found"}, status=404)
   
    
def get_calc_machines(request, project_id):
    try:
        project = APP_Project.objects.get(id=project_id)
        machines = modelcalc.objects.filter(project=project)
        
        
        
        data = {
            "project_name": project.name,
            "machines": list(machines.values("oSec00Field01", "oSec00Field02", "oSec00Field03",
                                             "oSec01Field01", "oSec01Field02", "oSec01Field03",
                                             "oSec01Field04", "oSec01Field05", "oSec01Field06",
                                             "oSec01Field07", "oSec01Field08", "oSec01Field09",
                                             "oSec01Field10", "oSec01Field11", "oSec01Field12",
                                             "oSec01Field13", "oSec01Field14", "oSec01Field15",
                                             "oSec01Field16", "oSec01Field17", "oSec01Field18",
                                             "oSec01Field19", "oSec01Field20", "oSec01Field21",
                                             "oSec01Field22", "oSec01Field23", "oSec01Field24", 
                                             "oSec01Field25", "oSec01Field26", "oSec01Field27", 
                                             "oSec01Field28", "oSec01Field29", "oSec01Field30",
                                             "oSec02Field01", "oSec02Field02", "oSec02Field03",
                                             "oSec02Field04", "oSec02Field05", "oSec02Field06",
                                             "oSec02Field07", "oSec02Field08", "oSec02Field09",
                                             "oSec02Field10", "oSec02Field11", "oSec02Field12",
                                             "oSec02Field13", "oSec02Field14", "oSec02Field15",
                                             "oSec02Field16", "oSec02Field17", "oSec02Field18",
                                             "oSec02Field19", "oSec02Field20", "oSec02Field21",
                                             "oSec02Field22", "oSec02Field23", "oSec02Field24", 
                                             "oSec02Field25", "oSec02Field26", "oSec02Field27", 
                                             "oSec02Field28", "oSec02Field29", "oSec02Field30",))
        }
        return JsonResponse(data)
    except APP_Project.DoesNotExist:
        return JsonResponse({"error": "Project not found"}, status=404)

################################################################

def get_report_progress(request, project_id):
    try:
        progress = ReportProgress.objects.filter( project_id=project_id).latest('updated_at')
        return JsonResponse({
            "percent": progress.percent,
            "status": progress.status
        })
    except ReportProgress.DoesNotExist:
        return JsonResponse({"percent": 0, "status": "not_started"})
    except Exception as e:
        return JsonResponse({"percent": 0, "status": f"error: {str(e)}"})



def save_reports(request, project_id):
    print("###############################")
    print("###############################")
    print("###############################")
    print("###############################")
    print("###############################")    
    print("start, save_reports, project_id : ", project_id)
    user = request.user
    project = APP_Project.objects.get(pk=project_id)
    ReportProgress.objects.update_or_create(
        user=user,
        project_id=project_id,
        status=f"{project.name}_starting",
        percent=5,
        
    )

    user_id = request.user.id
    group_id = f"user-{user_id}-project-{project_id}"

    # Check if a task with this group is still pending or running
    existing_task = Task.objects.filter(group=group_id, success__isnull=True).first()
    if existing_task:
        return JsonResponse({'message': 'Report generation is already in progress. Please wait.'}, status=429)
    
    async_task('Apps.aAppProject.tasks.save_reports_task', project_id, user_id,q_options={ 'group': group_id, 'timeout': 600 })

    
    
    return JsonResponse({'message': 'Report generation started.'}, status=202)


def download_project_reports(request, project_id):

    project = APP_Project.objects.get(id=project_id)
    company_name = slugify(project.company.nameCompanies)
    project_name = slugify(project.name)
    folder_name = slugify(f"{project_id}_{company_name}_{project_name}")

    folder_path = os.path.join(settings.BASE_DIR, 'static', 'aReports', company_name, folder_name)

    # In-memory zip
    buffer = BytesIO()
    with zipfile.ZipFile(buffer, 'w', zipfile.ZIP_DEFLATED) as zip_file:
        for root, _, files in os.walk(folder_path):
            for file in files:
                abs_path = os.path.join(root, file)
                rel_path = os.path.relpath(abs_path, folder_path)
                zip_file.write(abs_path, arcname=rel_path)

    buffer.seek(0)
    response = HttpResponse(buffer, content_type='application/zip')
    response['Content-Disposition'] = f'attachment; filename="{folder_name}_reports.zip"'
    return response


def download_drive_project_reports(request, project_id):

    project = APP_Project.objects.get(id=project_id)
    company_slug = slugify(project.company.nameCompanies)
    company_name = project.company.nameCompanies
    project_name = slugify(project.name)
    folder_name = slugify(f"{project_id}_{company_slug}_{project_name}")


    folder_id = get_folder_id_by_name( service , "aReports")
    company_folder_id = get_folder_id_by_name( service , company_name, folder_id)
    project_folder_id = get_folder_id_by_name( service , folder_name, company_folder_id )

    files_in_folder = get_file_ids_in_folder(service, project_folder_id)

    
    # Create in-memory ZIP file
    zip_buffer = BytesIO()
    with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for file_id, file_name in files_in_folder:
            file_data = download_file_as_bytes(service, file_id)  # <- returns file content
            if file_data is None:
                continue 
            zipf.writestr(file_name, file_data)

    zip_buffer.seek(0)  # Move pointer to the beginning

    response = HttpResponse(zip_buffer, content_type='application/zip')
    response['Content-Disposition'] = f'attachment; filename="{folder_name}_reports.zip"'
    return response

