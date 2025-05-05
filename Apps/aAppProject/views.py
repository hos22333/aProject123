from django.shortcuts import render

from config import settings
from .forms import ProjectForm
from .models import APP_Project
from Apps.aAppMechanical.models import UserCompany
from Apps.aAppSubmittal.models import Machine
from Apps.aAppSubmittal.models import AddMachine
from Apps.aAppMechanical.models import aLogEntry
from Apps.aAppCalculation.models import modelcalc
from Apps.aAppSubmittal.views import get_user_company

import requests
import cloudconvert
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
from docx.enum.text import WD_PARAGRAPH_ALIGNMENT
from docx.oxml import OxmlElement, ns
from docx.shared import Inches
from docx.shared import Pt

from fpdf import FPDF

from PyPDF2 import PdfReader, PdfWriter

# Create your views here.



def project_list(request):
    if request.method == "POST":
        aLogEntry.objects.create(
            user=request.user,
            message=f"{request.user} Entered the project list "
        )
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
            company_name = slugify(instance.company.nameCompanies)  
            project_name = slugify(instance.name)       
            project_id = APP_Project.objects.get(name = project_name).id
            folder_name = f"{project_id}_{company_name}_{project_name}"

            
            base_static_path = os.path.join(settings.BASE_DIR, 'static', 'aReports')
            company_folder = os.path.join(base_static_path, company_name)
            project_folder = os.path.join(company_folder, folder_name)


            # Create the folders if they don't exist
            os.makedirs(project_folder, exist_ok=True)


            aLogEntry.objects.create(
                user=request.user,
                message=f"{request.user} Created a project {request.POST.get("name")} "
            )
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
        aLogEntry.objects.create(
            user=request.user,
            message=f"{request.user} Edited >>> {project.name} "
        )
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
        aLogEntry.objects.create(
            user=request.user,
            message=f"{request.user} Deleted >>> {project.name} "
        )
        project.delete()

        # Otherwise, redirect to the project list page
        return redirect('project_list')

    return JsonResponse({'success': False, 'error': 'Invalid request'})



def get_machines(request, project_id):
    try:
        project = APP_Project.objects.get(id=project_id)
        machines = Machine.objects.filter(project=project)

        aLogEntry.objects.create(
            user=request.user,
            message=f"{request.user} Get Data for >>>{project.name} "
        )
        
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
        
        aLogEntry.objects.create(
            user=request.user,
            message=f"{request.user} Get Data for >>> {project.name} "
        )
        
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












def generate_report(request, project_id):
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
            return generate_report_AAA(request, project_id)

        elif aCompany.company.nameCompanies == "BBBB":
            print("Company 2")
            return generate_report_BBB(request, project_id)

        else:
            return HttpResponse("Invalid company ID", status=400)

    except UserCompany.DoesNotExist:
        return HttpResponse("User does not belong to a company", status=403)

    except APP_Project.DoesNotExist:
        return HttpResponse("Project not found", status=404)




def generate_report_AAA(request, project_id):
    
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

        aCompany = UserCompany.objects.get(user=request.user)
        project = APP_Project.objects.get(id=project_id)
        machines = Machine.objects.filter(project=project)
        
        
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

        # Add machine details
        for index, machine in enumerate(machines, start=1):  # Add numbering
            machine_name = machine.oSec00Field03
            section_titles = []
            

            if machine_name == "DataSheetNS":
                machine_name = "Manual Screen" 
                section_titles = ["General Data", "Design Data", "Material Data", "Channel Data", " ", " ", " ", " ", " ", " "]

            if machine_name == "DataSheetMS":
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

    except APP_Project.DoesNotExist:
        return HttpResponse("Project not found", status=404)





def generate_report_BBB(request, project_id):
    
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

        aCompany = UserCompany.objects.get(user=request.user)
        project = APP_Project.objects.get(id=project_id)
        machines = Machine.objects.filter(project=project)
        
        
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

        # Add machine details
        for index, machine in enumerate(machines, start=1):  # Add numbering
            machine_name = machine.oSec00Field03
            section_titles = []

            if machine_name == "DataSheetNS":
                machine_name = "Manual Screen" 
                section_titles = ["General Data", "Design Data", "Material Data", "Channel Data", " ", " ", " ", " ", " ", " "]

            if machine_name == "DataSheetMS":
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

    except APP_Project.DoesNotExist:
        return HttpResponse("Project not found", status=404)




def generate_calculation_report(request, project_id):
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
            return generate_calculation_report_AAA(request, project_id)

        elif aCompany.company.nameCompanies == "BBBB":
            print("Company 2")
            return generate_calculation_report_BBB(request, project_id)

        else:
            return HttpResponse("Invalid company ID", status=400)

    except UserCompany.DoesNotExist:
        return HttpResponse("User does not belong to a company", status=403)

    except APP_Project.DoesNotExist:
        return HttpResponse("Project not found", status=404)




def generate_calculation_report_AAA(request, project_id):
    
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

        aCompany = UserCompany.objects.get(user=request.user)
        project = APP_Project.objects.get(id=project_id)
        machines = modelcalc.objects.filter(project=project)
        
        
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

        # Add machine details
        for index, machine in enumerate(machines, start=1):  # Add numbering
            machine_name = machine.oSec00Field03
            section_titles = []

            if machine_name == "NS":
                machine_name = "Manual Screen" 
                section_titles = ["General Data", "Design Data", "Material Data", "Channel Data", " ", " ", " ", " ", " ", " "]

            if machine_name == "MS":
                machine_name = "Mechanical Screen" 
                section_titles = ["General Data", "Design Data", "Gearmotor Data", "Control panel Data", "Material Data", "Other Data", " ", " ", " ", " "]

            if machine_name == "BC":
                machine_name = "Belt Conveyor"
                section_titles = ["General Data", "Design Data", "Gearbox Data", "Motor Data", "Material Data", " ", " ", " ", " ", " "]

            if machine_name == "CO":
                machine_name = "Container"
                section_titles = ["General Data", "Design Data", "Material Data", " ", " ", " ", " ", " ", " ", " "]

            if machine_name == "GR":
                machine_name = "Gritremoval"
                section_titles = ["General Data", "Design Data", "Walkway, Handrail, Wheel Data", "Scrapper Data", "Gearmotor Data", "Scrapper Data", "Drive unit", "Control panel Data", "Material Data ", " "]

            if machine_name == "SS":
                machine_name = "Sand Silo"

            if machine_name == "PS":
                machine_name = "Primary Sedimentation"

            if machine_name == "QV":
                machine_name = "Quick Valve"

            if machine_name == "TV":
                machine_name = "Telescopic Valve"
                
            if machine_name == "TH":
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
        response['Content-Disposition'] = f'attachment; filename={project.name}_Calculation_report.docx'
        doc.save(response)
        return response

    except APP_Project.DoesNotExist:
        return HttpResponse("Project not found", status=404)





def generate_calculation_report_BBB(request, project_id):
    
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

        aCompany = UserCompany.objects.get(user=request.user)
        project = APP_Project.objects.get(id=project_id)
        machines = modelcalc.objects.filter(project=project)
        
        
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

        # Add machine details
        for index, machine in enumerate(machines, start=1):  # Add numbering
            machine_name = machine.oSec00Field03
            section_titles = []

            if machine_name == "NS":
                machine_name = "Manual Screen" 
                section_titles = ["General Data", "Design Data", "Material Data", "Channel Data", " ", " ", " ", " ", " ", " "]

            if machine_name == "MS":
                machine_name = "Mechanical Screen" 
                section_titles = ["General Data", "Design Data", "Gearmotor Data", "Control panel Data", "Material Data", "Other Data", " ", " ", " ", " "]

            if machine_name == "BC":
                machine_name = "Belt Conveyor"
                section_titles = ["General Data", "Design Data", "Gearbox Data", "Motor Data", "Material Data", " ", " ", " ", " ", " "]

            if machine_name == "CO":
                machine_name = "Container"
                section_titles = ["General Data", "Design Data", "Material Data", " ", " ", " ", " ", " ", " ", " "]

            if machine_name == "GR":
                machine_name = "Gritremoval"
                section_titles = ["General Data", "Design Data", "Walkway, Handrail, Wheel Data", "Scrapper Data", "Gearmotor Data", "Scrapper Data", "Drive unit", "Control panel Data", "Material Data ", " "]

            if machine_name == "SS":
                machine_name = "Sand Silo"

            if machine_name == "PS":
                machine_name = "Primary Sedimentation"

            if machine_name == "QV":
                machine_name = "Quick Valve"

            if machine_name == "TV":
                machine_name = "Telescopic Valve"
                
            if machine_name == "TH":
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
        response['Content-Disposition'] = f'attachment; filename={project.name}_Calculation_report.docx'
        doc.save(response)
        return response

    except APP_Project.DoesNotExist:
        return HttpResponse("Project not found", status=404)


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


def save_reports(request, project_id):
    try:
        #pdb.set_trace()
        # Log the action
        aLogEntry.objects.create(user=request.user, message=f"at {now()} {request.user} accessed Word Report")
        
        #pdb.set_trace()
        # Get the user’s company and project
        aCompany = UserCompany.objects.get(user=request.user)

        #pdb.set_trace()
        # Determine the company and generate the corresponding report
        if aCompany:
            save_submittal_report(request, project_id)
            save_pdf_report(request, project_id)
            save_calculation_report(request, project_id)
            return HttpResponse(status=204)

        else:
            return HttpResponse("Invalid company ID", status=400)
        
        

    except UserCompany.DoesNotExist:
        return HttpResponse("User does not belong to a company", status=403)

    except APP_Project.DoesNotExist:
        return HttpResponse("Project not found", status=404)
    
    



def save_submittal_report(request, project_id):
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
            return save_submittal_report_AAA(request, project_id)

        elif aCompany.company.nameCompanies == "BBBB":
            print("Company 2")
            return save_submittal_report_BBB(request, project_id)

        else:
            return HttpResponse("Invalid company ID", status=400)

    except UserCompany.DoesNotExist:
        return HttpResponse("User does not belong to a company", status=403)

    except APP_Project.DoesNotExist:
        return HttpResponse("Project not found", status=404)




def save_submittal_report_AAA(request, project_id):
    
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
    
    # Define a custom class for the PDF layout
    class PDF(FPDF):
        def __init__(self):
            super().__init__()
            self.set_auto_page_break(auto=True, margin=15)

            # Add the TrueType Unicode font (DejaVuSans)
            self.add_font('DejaVu', '', 'static/aFonts/DejaVuSans.ttf', uni=True)  # Regular
            self.add_font('DejaVu', 'B', 'static/aFonts/DejaVuSans-Bold.ttf', uni=True)  # Bold
            self.add_font('DejaVu', 'I', 'static/aFonts/DejaVuSerif-Italic.ttf', uni=True)  # Italic
            self.set_font('DejaVu', '', 12)

        def header_page(self, projectname, clientname, capacity):
            self.set_y(50)
            self.set_font("DejaVu", "B", 16)
            self.set_text_color(33, 66, 133)
            self.cell(0, 20, f"Project Report: {projectname}", ln=True,) 
            self.set_font("DejaVu", "B", 14)
            self.cell(0, 10, f"Project Details", ln=True,) 
            self.set_text_color(0, 0, 0)
            self.set_font("DejaVu", "", 12)
            self.cell(0, 10, f"Name:  {projectname}", ln=True,) 
            self.cell(0, 10, f"Client Name:  {clientname}", ln=True,) 
            self.cell(0, 10, f"Capacity: {capacity}", ln=True,) 

        def header(self):
            # Logo
            page_width = self.w - 2 * self.l_margin
            
            try:
                self.image("static/aLogo/LogoAAA.PNG", x=self.l_margin, y=10, w=page_width)  

                # Move cursor below image to avoid overlapping next content
                self.set_y(10 + 50)
            except Exception as e:
                print(f"Error loading logo: {e}")


        def footer(self):
            self.set_y(-15)  # Position 15 mm from bottom
            self.set_font("DejaVu", "I", 8)
            self.set_text_color(128)

            # Add "Page X of Y"
            self.cell(0, 10, f"Page {self.page_no()} of {{nb}}", align='C')

        def colored_header(self, number, name):
            self.set_font("DejaVu", "B", 16)
            self.set_text_color(33, 66, 133)
            self.cell(0, 10, f"{number}. {name}", ln=True)

        def section_title(self, title):
            self.set_font("DejaVu", "B", 12)
            self.set_text_color(33, 66, 133)
            self.ln(5)
            self.cell(0, 10, title, ln=True)

        def add_table(self, data):
            self.set_font("DejaVu", "B", 10)
            self.set_fill_color(255, 153, 0)
            self.set_text_color(0)
            self.cell(60, 8, "Field", border=1, fill=True)
            self.cell(130, 8, "Value", border=1, ln=True, fill=True)

            self.set_font("DejaVu", "", 10)
            for field, value in data:
                self.cell(60, 8, field, border=1)
                self.cell(130, 8, value, border=1, ln=True)
    
    
    try:
        
        ###LOG
        aLogEntry.objects.create(
                user=request.user,
                message=f"at {now()} {request.user} accessed Load  "
            )
        print(f"at {now()} {User} accessed Save Report")
        ###LOG

        aCompany = UserCompany.objects.get(user=request.user)
        company_id = aCompany.company
        project = APP_Project.objects.get(id=project_id)
        machines = Machine.objects.filter(project=project)

        print(aCompany.id)
        print(project.id)
    
        print("Company 1")
    
    
        # Create a Word document
        doc = Document()

        pdf = PDF()
        # Add header and footer with page numbers
        add_header_footer(doc)

        pdf.alias_nb_pages()  # Important for "of {nb}" to work
        pdf.add_page()
        
        # Add project title
        doc.add_heading(f'Project Report: {project.name}', level=1)

        pdf.header_page(project.name,  project.client_name, project.capacity)

        # Add project details
        doc.add_heading("Project Details", level=2)  
    

        doc.add_paragraph("\n")
        doc.add_paragraph("Name: " + project.name)
        doc.add_paragraph("Client Name: " + project.client_name)
        doc.add_paragraph("Capacity: " + project.capacity)
        doc.add_paragraph("\n")
        
        doc.add_page_break()     
        doc.add_paragraph("\n")

        

        # Add machine details
        for index, machine in enumerate(machines, start=1):  # Add numbering
            machine_name = machine.oSec00Field03
            machine_ID = machine.id
            sheet_key = AddMachine.objects.get(nameDB=machine_name, company=company_id).keyValue
            section_titles = []
            General_saved_DXF_ALL(request, machine_ID, sheet_key, project_id)
            SavedFullDrawing(request, machine_ID, sheet_key)
            if machine_name == "DataSheetNS":
                machine_name = "Manual Screen" 
                section_titles = ["General Data", "Design Data", "Material Data", "Channel Data", " ", " ", " ", " ", " ", " "]

            if machine_name == "DataSheetMS":
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
            
            pdf.alias_nb_pages()  # Important for "of {nb}" to work
            pdf.add_page()
            pdf.colored_header(index, machine_name)

            for i in range(1, 11):  # Loop from Sec01 to Sec10
                section_name = f"Sec{i:02d}"
                word_section_data = [("Field", "Value")]
                pdf_section_data = []

                for j in range(1, 21, 2):  # Step by 2 to avoid duplication
                    key = getattr(machine, f"o{section_name}Field{j:02d}", "").strip()
                    value = getattr(machine, f"o{section_name}Field{j+1:02d}", "").strip()

                    if key and value and key.lower() != "oooo" and value.lower() != "oooo":
                        word_section_data.append((key, value))
                        pdf_section_data.append((key, value))

                if len(word_section_data) > 1:  # If the section has valid data, create a table
                    section_title = section_titles[i-1] if i-1 < len(section_titles) else f"Section {i}"
                    doc.add_paragraph(f"{section_name}: {section_title}", style="Heading3")  # Only one title now

                    pdf.section_title(f"{section_name}: {section_title}")

                    add_table(doc, word_section_data)  # Removed redundant title

                    pdf.add_table(pdf_section_data)


            doc.add_page_break() 
        
        # Define the folder path
        company_slug = slugify(project.company.nameCompanies)
        project_slug = slugify(project.name)
        folder_name = slugify(f"{project_id}_{company_slug}_{project_slug}")

        project_folder = os.path.join(settings.BASE_DIR, 'static', 'aReports', company_slug, folder_name)
        os.makedirs(project_folder, exist_ok=True)  # Create folder if it doesn't exist

        # Save the file to that path
        word_file_path = os.path.join(project_folder, f"{project_slug}_report.docx")
        doc.save(word_file_path)
        
        pdf_file_path = os.path.join(project_folder, f"{project_slug}_report.pdf")
        pdf.output(pdf_file_path)

        return HttpResponse(status=204)
        

        

    except APP_Project.DoesNotExist:
        return HttpResponse("Project not found", status=404)





def save_submittal_report_BBB(request, project_id):
    
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
    
    
    # Define a custom class for the PDF layout
    class PDF(FPDF):
        def __init__(self):
            super().__init__()
            self.set_auto_page_break(auto=True, margin=15)

            # Add the TrueType Unicode font (DejaVuSans)
            self.add_font('DejaVu', '', 'static/aFonts/DejaVuSans.ttf', uni=True)  # Regular
            self.add_font('DejaVu', 'B', 'static/aFonts/DejaVuSans-Bold.ttf', uni=True)  # Bold
            self.add_font('DejaVu', 'I', 'static/aFonts/DejaVuSerif-Italic.ttf', uni=True)  # Italic
            self.set_font('DejaVu', '', 12)

        def header_footer(self, projectname, clientname, capacity):
            self.set_y(50)
            self.set_font("DejaVu", "B", 16)
            self.set_text_color(33, 66, 133)
            self.cell(0, 20, f"Project Report: {projectname}", ln=True,) 
            self.set_font("DejaVu", "B", 14)
            self.cell(0, 10, f"Project Details", ln=True,) 
            self.set_text_color(0, 0, 0)
            self.set_font("DejaVu", "", 12)
            self.cell(0, 10, f"Name:  {projectname}", ln=True,) 
            self.cell(0, 10, f"Client Name:  {clientname}", ln=True,) 
            self.cell(0, 10, f"Capacity: {capacity}", ln=True,) 

        def header(self):
            # Logo
            page_width = self.w - 2 * self.l_margin
            
            try:
                self.image("static/aLogo/LogoBBB.PNG", x=self.l_margin, y=10, w=page_width)  

                # Move cursor below image to avoid overlapping next content
                self.set_y(10 + 50)
            except Exception as e:
                print(f"Error loading logo: {e}")



        def footer(self):
            self.set_y(-15)  # Position 15 mm from bottom
            self.set_font("DejaVu", "I", 8)
            self.set_text_color(128)

            # Add "Page X of Y"
            self.cell(0, 10, f"Page {self.page_no()} of {{nb}}", align='C')

        def colored_header(self, number, name):
            self.set_font("DejaVu", "B", 16)
            self.set_text_color(33, 66, 133)
            self.cell(0, 10, f"{number}. {name}", ln=True)

        def section_title(self, title):
            self.set_font("DejaVu", "B", 12)
            self.set_text_color(33, 66, 133)
            self.ln(5)
            self.cell(0, 10, title, ln=True)

        def add_table(self, data):
            self.set_font("DejaVu", "B", 10)
            self.set_fill_color(255, 153, 0)
            self.set_text_color(0)
            self.cell(60, 8, "Field", border=1, fill=True)
            self.cell(130, 8, "Value", border=1, ln=True, fill=True)

            self.set_font("DejaVu", "", 10)
            for field, value in data:
                self.cell(60, 8, field, border=1)
                self.cell(130, 8, value, border=1, ln=True)
    
    
    try:
        
        ###LOG
        aLogEntry.objects.create(
                user=request.user,
                message=f"at {now()} {request.user} accessed Load  "
            )
        print(f"at {now()} {User} accessed Download Report")
        ###LOG

        aCompany = UserCompany.objects.get(user=request.user)
        company_id = aCompany.company
        project = APP_Project.objects.get(id=project_id)
        machines = Machine.objects.filter(project=project)
        
        
        print(aCompany.id)
        print(project.id)
    
        print("Company 2")
    
    
        # Create a Word document
        doc = Document()

        pdf = PDF()

        # Add header and footer with page numbers
        add_header_footer(doc)

        pdf.alias_nb_pages()  # Important for "of {nb}" to work
        pdf.add_page()

        # Add project title
        doc.add_heading(f'Project Report: {project.name}', level=1)

        pdf.header_footer(project.name,  project.client_name, project.capacity)

        # Add project details
        doc.add_heading("Project Details", level=2)     

        doc.add_paragraph("\n")
        doc.add_paragraph("Name: " + project.name)
        doc.add_paragraph("Client Name: " + project.client_name)
        doc.add_paragraph("Capacity: " + project.capacity)
        doc.add_paragraph("\n")
        
        doc.add_page_break()     
        doc.add_paragraph("\n")

        # Add machine details
        for index, machine in enumerate(machines, start=1):  # Add numbering
            machine_name = machine.oSec00Field03
            machine_ID = machine.id
            sheet_key = AddMachine.objects.get(nameDB=machine_name, company=company_id).keyValue
            section_titles = []
            General_saved_DXF_ALL(request, machine_ID, sheet_key, project_id)
            SavedFullDrawing(request, machine_ID, sheet_key)

            if machine_name == "DataSheetNS":
                machine_name = "Manual Screen" 
                section_titles = ["General Data", "Design Data", "Material Data", "Channel Data", " ", " ", " ", " ", " ", " "]

            if machine_name == "DataSheetMS":
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
            
            pdf.alias_nb_pages()  # Important for "of {nb}" to work
            pdf.add_page()
            pdf.colored_header(index, machine_name)

            for i in range(1, 11):  # Loop from Sec01 to Sec10
                section_name = f"Sec{i:02d}"
                section_data = [("Field", "Value")]
                pdf_section_data = []

                for j in range(1, 21, 2):  # Step by 2 to avoid duplication
                    key = getattr(machine, f"o{section_name}Field{j:02d}", "").strip()
                    value = getattr(machine, f"o{section_name}Field{j+1:02d}", "").strip()

                    if key and value and key.lower() != "oooo" and value.lower() != "oooo":
                        section_data.append((key, value))
                        pdf_section_data.append((key, value))

                if len(section_data) > 1:  # If the section has valid data, create a table
                    section_title = section_titles[i-1] if i-1 < len(section_titles) else f"Section {i}"
                    doc.add_paragraph(f"{section_name}: {section_title}", style="Heading3")  # Only one title now

                    pdf.section_title(f"{section_name}: {section_title}")

                    add_table(doc, section_data)  # Removed redundant title

                    pdf.add_table(pdf_section_data)

            doc.add_page_break()     

        # Define the folder path
        company_slug = slugify(project.company.nameCompanies)
        project_slug = slugify(project.name)
        folder_name = slugify(f"{project_id}_{company_slug}_{project_slug}")

        project_folder = os.path.join(settings.BASE_DIR, 'static', 'aReports', company_slug, folder_name)
        os.makedirs(project_folder, exist_ok=True)  # Create folder if it doesn't exist

        # Save the file to that path
        file_path = os.path.join(project_folder, f"{project_slug}_report.docx")
        doc.save(file_path)

        pdf_file_path = os.path.join(project_folder, f"{project_slug}_report.pdf")
        pdf.output(pdf_file_path)

        return HttpResponse(status=204)

        

    except APP_Project.DoesNotExist:
        return HttpResponse("Project not found", status=404)




def save_calculation_report(request, project_id):
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
            return save_calculation_report_AAA(request, project_id)

        elif aCompany.company.nameCompanies == "BBBB":
            print("Company 2")
            return save_calculation_report_BBB(request, project_id)

        else:
            return HttpResponse("Invalid company ID", status=400)

    except UserCompany.DoesNotExist:
        return HttpResponse("User does not belong to a company", status=403)

    except APP_Project.DoesNotExist:
        return HttpResponse("Project not found", status=404)




def save_calculation_report_AAA(request, project_id):
    
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
    
    # Define a custom class for the PDF layout
    class PDF(FPDF):
        def __init__(self):
            super().__init__()
            self.set_auto_page_break(auto=True, margin=15)

            # Add the TrueType Unicode font (DejaVuSans)
            self.add_font('DejaVu', '', 'static/aFonts/DejaVuSans.ttf', uni=True)  # Regular
            self.add_font('DejaVu', 'B', 'static/aFonts/DejaVuSans-Bold.ttf', uni=True)  # Bold
            self.add_font('DejaVu', 'I', 'static/aFonts/DejaVuSerif-Italic.ttf', uni=True)  # Italic
            self.set_font('DejaVu', '', 12)

        def header_footer(self, projectname, clientname, capacity):
            self.set_y(50)
            self.set_font("DejaVu", "B", 16)
            self.set_text_color(33, 66, 133)
            self.cell(0, 20, f"Project Report: {projectname}", ln=True,) 
            self.set_font("DejaVu", "B", 14)
            self.cell(0, 10, f"Project Details", ln=True,) 
            self.set_text_color(0, 0, 0)
            self.set_font("DejaVu", "", 12)
            self.cell(0, 10, f"Name:  {projectname}", ln=True,) 
            self.cell(0, 10, f"Client Name:  {clientname}", ln=True,) 
            self.cell(0, 10, f"Capacity: {capacity}", ln=True,) 

        def header(self):
            # Logo
            page_width = self.w - 2 * self.l_margin
            
            try:
                self.image("static/aLogo/LogoAAA.PNG", x=self.l_margin, y=10, w=page_width)  

                # Move cursor below image to avoid overlapping next content
                self.set_y(10 + 50)
            except Exception as e:
                print(f"Error loading logo: {e}")


        def footer(self):
            self.set_y(-15)  # Position 15 mm from bottom
            self.set_font("DejaVu", "I", 8)
            self.set_text_color(128)

            # Add "Page X of Y"
            self.cell(0, 10, f"Page {self.page_no()} of {{nb}}", align='C')

        def colored_header(self, number, name):
            self.set_font("DejaVu", "B", 16)
            self.set_text_color(33, 66, 133)
            self.cell(0, 10, f"{number}. {name}", ln=True)

        def section_title(self, title):
            self.set_font("DejaVu", "B", 12)
            self.set_text_color(33, 66, 133)
            self.ln(5)
            self.cell(0, 10, title, ln=True)

        def add_table(self, data):
            self.set_font("DejaVu", "B", 10)
            self.set_fill_color(255, 153, 0)
            self.set_text_color(0)
            self.cell(60, 8, "Field", border=1, fill=True)
            self.cell(130, 8, "Value", border=1, ln=True, fill=True)

            self.set_font("DejaVu", "", 10)
            for field, value in data:
                self.cell(60, 8, field, border=1)
                self.cell(130, 8, value, border=1, ln=True)
    
    
    
    try:
        
        ###LOG
        aLogEntry.objects.create(
                user=request.user,
                message=f"at {now()} {request.user} accessed Load  "
            )
        print(f"at {now()} {User} accessed Download Report")
        ###LOG

        aCompany = UserCompany.objects.get(user=request.user)
        companyname=aCompany.company.nameCompanies
        firstletter = companyname[0]
        project = APP_Project.objects.get(id=project_id)
        machines = modelcalc.objects.filter(project=project)
        
        
        print(aCompany.id)
        print(project.id)
    
        print("Company 1")
    
    
        # Create a Word document
        doc = Document()

        pdf = PDF()

        # Add header and footer with page numbers
        add_header_footer(doc)

        pdf.alias_nb_pages()  # Important for "of {nb}" to work
        pdf.add_page()

        # Add project title
        doc.add_heading(f'Project Report: {project.name}', level=1)

        pdf.header_footer(project.name,  project.client_name, project.capacity)

        # Add project details
        doc.add_heading("Project Details", level=2)     

        doc.add_paragraph("\n")
        doc.add_paragraph("Name: " + project.name)
        doc.add_paragraph("Client Name: " + project.client_name)
        doc.add_paragraph("Capacity: " + project.capacity)
        doc.add_paragraph("\n")
        
        doc.add_page_break()     
        doc.add_paragraph("\n")

        # Add machine details
        for index, machine in enumerate(machines, start=1):  # Add numbering
            machine_name = machine.oSec00Field03
            section_titles = []

            if machine_name == f"NS_{firstletter}":
                machine_name = "Manual Screen" 
                section_titles = ["General Data", "Design Data", "Material Data", "Channel Data", " ", " ", " ", " ", " ", " "]

            if machine_name == f"MS_{firstletter}":
                machine_name = "Mechanical Screen" 
                section_titles = ["General Data", "Design Data", "Gearmotor Data", "Control panel Data", "Material Data", "Other Data", " ", " ", " ", " "]

            if machine_name == f"BC_{firstletter}":
                machine_name = "Belt Conveyor"
                section_titles = ["General Data", "Design Data", "Gearbox Data", "Motor Data", "Material Data", " ", " ", " ", " ", " "]

            if machine_name == f"CO_{firstletter}":
                machine_name = "Container"
                section_titles = ["General Data", "Design Data", "Material Data", " ", " ", " ", " ", " ", " ", " "]

            if machine_name == f"GR_{firstletter}":
                machine_name = "Gritremoval"
                section_titles = ["General Data", "Design Data", "Walkway, Handrail, Wheel Data", "Scrapper Data", "Gearmotor Data", "Scrapper Data", "Drive unit", "Control panel Data", "Material Data ", " "]

            if machine_name == f"SS_{firstletter}":
                machine_name = "Sand Silo"

            if machine_name == f"PS_{firstletter}":
                machine_name = "Primary Sedimentation"

            if machine_name == f"QV_{firstletter}":
                machine_name = "Quick Valve"

            if machine_name == f"TV_{firstletter}":
                machine_name = "Telescopic Valve"
                
            if machine_name == f"TH_{firstletter}":
                machine_name = "Sludge Thickener"

            # Add machine title with font size 14 and numbering
            machine_title = doc.add_paragraph(f"{index}. {machine_name}", style="Heading3")
            machine_title.runs[0].font.size = Pt(14)
            
            pdf.alias_nb_pages()  # Important for "of {nb}" to work
            pdf.add_page()
            pdf.colored_header(index, machine_name)

            for i in range(1, 11):  # Loop from Sec01 to Sec10
                section_name = f"Sec{i:02d}"
                section_data = [("Field", "Value")]
                pdf_section_data = []

                for j in range(1, 21, 2):  # Step by 2 to avoid duplication
                    key = getattr(machine, f"o{section_name}Field{j:02d}", "").strip()
                    value = getattr(machine, f"o{section_name}Field{j+1:02d}", "").strip()

                    if key and value and key.lower() != "oooo" and value.lower() != "oooo":
                        section_data.append((key, value))
                        pdf_section_data.append((key, value))

                if len(section_data) > 1:  # If the section has valid data, create a table
                    section_title = section_titles[i-1] if i-1 < len(section_titles) else f"Section {i}"
                    doc.add_paragraph(f"{section_name}: {section_title}", style="Heading3")  # Only one title now

                    pdf.section_title(f"{section_name}: {section_title}")

                    add_table(doc, section_data)  # Removed redundant title

                    pdf.add_table(pdf_section_data)

            doc.add_page_break() 
        
        # Define the folder path
        company_slug = slugify(project.company.nameCompanies)
        project_slug = slugify(project.name)
        folder_name = slugify(f"{project_id}_{company_slug}_{project_slug}")

        project_folder = os.path.join(settings.BASE_DIR, 'static', 'aReports', company_slug, folder_name)
        os.makedirs(project_folder, exist_ok=True)  # Create folder if it doesn't exist

        # Save the file to that path
        file_path = os.path.join(project_folder, f"{project_slug}_Calculation_report.docx")
        doc.save(file_path)
        
        pdf_file_path = os.path.join(project_folder, f"{project_slug}_Calculation_report.pdf")
        pdf.output(pdf_file_path)

        return HttpResponse(status=204)

        

    except APP_Project.DoesNotExist:
        return HttpResponse("Project not found", status=404)





def save_calculation_report_BBB(request, project_id):
    
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
    
    
    # Define a custom class for the PDF layout
    class PDF(FPDF):
        def __init__(self):
            super().__init__()
            self.set_auto_page_break(auto=True, margin=15)

            # Add the TrueType Unicode font (DejaVuSans)
            self.add_font('DejaVu', '', 'static/aFonts/DejaVuSans.ttf', uni=True)  # Regular
            self.add_font('DejaVu', 'B', 'static/aFonts/DejaVuSans-Bold.ttf', uni=True)  # Bold
            self.add_font('DejaVu', 'I', 'static/aFonts/DejaVuSerif-Italic.ttf', uni=True)  # Italic
            self.set_font('DejaVu', '', 12)

        def header_footer(self, projectname, clientname, capacity):
            self.set_y(50)
            self.set_font("DejaVu", "B", 16)
            self.set_text_color(33, 66, 133)
            self.cell(0, 20, f"Project Report: {projectname}", ln=True,) 
            self.set_font("DejaVu", "B", 14)
            self.cell(0, 10, f"Project Details", ln=True,) 
            self.set_text_color(0, 0, 0)
            self.set_font("DejaVu", "", 12)
            self.cell(0, 10, f"Name:  {projectname}", ln=True,) 
            self.cell(0, 10, f"Client Name:  {clientname}", ln=True,) 
            self.cell(0, 10, f"Capacity: {capacity}", ln=True,) 

        def header(self):
            # Logo
            page_width = self.w - 2 * self.l_margin
            
            try:
                self.image("static/aLogo/LogoBBB.PNG", x=self.l_margin, y=10, w=page_width)  

                # Move cursor below image to avoid overlapping next content
                self.set_y(10 + 50)
            except Exception as e:
                print(f"Error loading logo: {e}")


        def footer(self):
            self.set_y(-15)  # Position 15 mm from bottom
            self.set_font("DejaVu", "I", 8)
            self.set_text_color(128)

            # Add "Page X of Y"
            self.cell(0, 10, f"Page {self.page_no()} of {{nb}}", align='C')

        def colored_header(self, number, name):
            self.set_font("DejaVu", "B", 16)
            self.set_text_color(33, 66, 133)
            self.cell(0, 10, f"{number}. {name}", ln=True)

        def section_title(self, title):
            self.set_font("DejaVu", "B", 12)
            self.set_text_color(33, 66, 133)
            self.ln(5)
            self.cell(0, 10, title, ln=True)

        def add_table(self, data):
            self.set_font("DejaVu", "B", 10)
            self.set_fill_color(255, 153, 0)
            self.set_text_color(0)
            self.cell(60, 8, "Field", border=1, fill=True)
            self.cell(130, 8, "Value", border=1, ln=True, fill=True)

            self.set_font("DejaVu", "", 10)
            for field, value in data:
                self.cell(60, 8, field, border=1)
                self.cell(130, 8, value, border=1, ln=True)
    
    
    try:
        
        ###LOG
        aLogEntry.objects.create(
                user=request.user,
                message=f"at {now()} {request.user} accessed Load  "
            )
        print(f"at {now()} {User} accessed Download Report")
        ###LOG

        aCompany = UserCompany.objects.get(user=request.user)
        companyname=aCompany.company.nameCompanies
        firstletter = companyname[0]
        project = APP_Project.objects.get(id=project_id)
        machines = modelcalc.objects.filter(project=project)
        
        
        print(aCompany.id)
        print(project.id)
    
        print("Company 2")
    
    
        # Create a Word document
        doc = Document()

        pdf = PDF()

        # Add header and footer with page numbers
        add_header_footer(doc)

        pdf.alias_nb_pages()  # Important for "of {nb}" to work
        pdf.add_page()

        # Add project title
        doc.add_heading(f'Project Report: {project.name}', level=1)

        pdf.header_footer(project.name,  project.client_name, project.capacity)

        # Add project details
        doc.add_heading("Project Details", level=2)     

        doc.add_paragraph("\n")
        doc.add_paragraph("Name: " + project.name)
        doc.add_paragraph("Client Name: " + project.client_name)
        doc.add_paragraph("Capacity: " + project.capacity)
        doc.add_paragraph("\n")
        
        doc.add_page_break()     
        doc.add_paragraph("\n")

        # Add machine details
        for index, machine in enumerate(machines, start=1):  # Add numbering
            machine_name = machine.oSec00Field03
            section_titles = []

            if machine_name == f"NS_{firstletter}":
                machine_name = "Manual Screen" 
                section_titles = ["General Data", "Design Data", "Material Data", "Channel Data", " ", " ", " ", " ", " ", " "]

            if machine_name == f"MS_{firstletter}":
                machine_name = "Mechanical Screen" 
                section_titles = ["General Data", "Design Data", "Gearmotor Data", "Control panel Data", "Material Data", "Other Data", " ", " ", " ", " "]

            if machine_name == f"BC_{firstletter}":
                machine_name = "Belt Conveyor"
                section_titles = ["General Data", "Design Data", "Gearbox Data", "Motor Data", "Material Data", " ", " ", " ", " ", " "]

            if machine_name == f"CO_{firstletter}":
                machine_name = "Container"
                section_titles = ["General Data", "Design Data", "Material Data", " ", " ", " ", " ", " ", " ", " "]

            if machine_name == f"GR_{firstletter}":
                machine_name = "Gritremoval"
                section_titles = ["General Data", "Design Data", "Walkway, Handrail, Wheel Data", "Scrapper Data", "Gearmotor Data", "Scrapper Data", "Drive unit", "Control panel Data", "Material Data ", " "]

            if machine_name == f"SS_{firstletter}":
                machine_name = "Sand Silo"

            if machine_name == f"PS_{firstletter}":
                machine_name = "Primary Sedimentation"

            if machine_name == f"QV_{firstletter}":
                machine_name = "Quick Valve"

            if machine_name == f"TV_{firstletter}":
                machine_name = "Telescopic Valve"
                
            if machine_name == f"TH_{firstletter}":
                machine_name = "Sludge Thickener"

            # Add machine title with font size 14 and numbering
            machine_title = doc.add_paragraph(f"{index}. {machine_name}", style="Heading3")
            machine_title.runs[0].font.size = Pt(14)
            
            pdf.alias_nb_pages()  # Important for "of {nb}" to work
            pdf.add_page()
            pdf.colored_header(index, machine_name)

            for i in range(1, 11):  # Loop from Sec01 to Sec10
                section_name = f"Sec{i:02d}"
                section_data = [("Field", "Value")]
                pdf_section_data = []

                for j in range(1, 21, 2):  # Step by 2 to avoid duplication
                    key = getattr(machine, f"o{section_name}Field{j:02d}", "").strip()
                    value = getattr(machine, f"o{section_name}Field{j+1:02d}", "").strip()

                    if key and value and key.lower() != "oooo" and value.lower() != "oooo":
                        section_data.append((key, value))
                        pdf_section_data.append((key, value))

                if len(section_data) > 1:  # If the section has valid data, create a table
                    section_title = section_titles[i-1] if i-1 < len(section_titles) else f"Section {i}"
                    doc.add_paragraph(f"{section_name}: {section_title}", style="Heading3")  # Only one title now

                    pdf.section_title(f"{section_name}: {section_title}")

                    add_table(doc, section_data)  # Removed redundant title

                    pdf.add_table(pdf_section_data)

            doc.add_page_break()     

        # Define the folder path
        company_slug = slugify(project.company.nameCompanies)
        project_slug = slugify(project.name)
        folder_name = slugify(f"{project_id}_{company_slug}_{project_slug}")

        project_folder = os.path.join(settings.BASE_DIR, 'static', 'aReports', company_slug, folder_name)
        os.makedirs(project_folder, exist_ok=True)  # Create folder if it doesn't exist

        # Save the file to that path
        file_path = os.path.join(project_folder, f"{project_slug}_Calculation_report.docx")
        doc.save(file_path)

        pdf_file_path = os.path.join(project_folder, f"{project_slug}_Calculation_report.pdf")
        pdf.output(pdf_file_path)

        return HttpResponse(status=204)

        

    except APP_Project.DoesNotExist:
        return HttpResponse("Project not found", status=404)




def convert_dxf_to_pdf_cloudconvert(input_path, output_path):
    cloudconvert.configure(api_key="eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJhdWQiOiIxIiwianRpIjoiZGViYWJiNGMzMjI3ZTA5YjgyYTUyZDI2NWY3ZTAxNmNhZjg2NWQ5MDRjYWIyMGEzMDYxN2I3MTlmYmYwMjZjYTZiODgxMmM5MDlkZmI4NzYiLCJpYXQiOjE3NDU2NzI2MTIuMjg2MTI2LCJuYmYiOjE3NDU2NzI2MTIuMjg2MTI3LCJleHAiOjQ5MDEzNDYyMTIuMjgxMjYxLCJzdWIiOiI3MTc0ODg5NyIsInNjb3BlcyI6WyJ1c2VyLnJlYWQiLCJ1c2VyLndyaXRlIiwidGFzay5yZWFkIiwidGFzay53cml0ZSIsIndlYmhvb2sucmVhZCIsIndlYmhvb2sud3JpdGUiLCJwcmVzZXQucmVhZCIsInByZXNldC53cml0ZSJdfQ.DGh70qP2W1ofilMBqzP_IkmqGvHpfiIn0jQou3w2gRpU2-gjz6CPlsxhhx6qLQ8EaYrQXHr_PCIwHR-m4sBbfNhKQ7N_gQ8j-dyZchk9GAj5I_uIHVLOwR-zQsmV-fNKVA55YG2n8Wy-PeV8rw7lP92a01vdgoK-sfyc-i4OjuhtlID7HuxB7p-yf6jya6EHY_gp_9NzeR_4RVRbIJkgejTXKVrTErs-6rTy-YruFzIkZev_w8ekryRzNv1Q0qm8rTAyTw-Pi3cmwFw4bbuLoiAxxOVG1K5JPqbPO2QVMn4-sgll3VIZwWvAQq-XhvMlf3AF5qMcDsCE-I1RcBcAg-Hr-_D-HjyHUB3Y63GYt2FRCw1OnwQ6ug4t9xrNcwiZOOdPrASpRlK0KN3S6pRG77lVM9rPCTu-khjG9B6b20ws8K0FmmiZBS7XxhPR94F1srD3K47LLPBW8OaAZFmiRdexa-cELxhPj1_VVYbNS5AazpjOCGkhiRbSO4KJEGr5fNFezUFqcLilyIM7TXBuwa5Oykoetx5McmCSJ8XgRwca1fCSmHXmY0VN8aczAwoKes4N8j5BMscJ1qq4v3FesXLP7hZunc08DFnYZAk3jZjddzfZPzzS84xQIVLsVGDw-Ig9T4LZdiJpDi5vaxv7m10nTan_IAOMhjGmIEw0FrQ", sandbox=False)

    job = cloudconvert.Job.create(payload={
        "tasks": {
            'import-my-file': {
                'operation': 'import/upload'
            },
            'convert-my-file': {
                'operation': 'convert',
                'input': 'import-my-file',
                'input_format': 'dxf',
                'output_format': 'pdf'
            },
            'export-my-file': {
                'operation': 'export/url',
                'input': 'convert-my-file'
            }
        }
    })

    job = cloudconvert.Job.find(id=job['id'])
    upload_task = [task for task in job['tasks'] if task['name'] == 'import-my-file'][0]
    upload_url = upload_task['result']['form']['url']
    parameters = upload_task['result']['form']['parameters']

    with open(input_path, 'rb') as file:
        response = requests.post(
            upload_url,
            data=parameters,
            files={'file': file}
        )

    if response.status_code not in [200, 201, 204]:
        raise Exception(f"Upload failed: {response.text}")

    while True:
        job = cloudconvert.Job.find(id=job['id'])
        if job['status'] == 'finished':
            break
        elif job['status'] == 'error':
            raise Exception("CloudConvert job failed.")
        time.sleep(2)

    export_task = [task for task in job['tasks'] if task['name'] == 'export-my-file'][0]
    file_url = export_task['result']['files'][0]['url']

    response = requests.get(file_url)
    with open(output_path, 'wb') as f:
        f.write(response.content)


# Helper function to define DXF paths
def get_saved_dxf_paths(user_company, category, project_id):
    # Get project info
    project = APP_Project.objects.get(id=project_id)
    company_slug = slugify(user_company.nameCompanies)
    project_slug = slugify(project.name)
    folder_name = f"{project_id}_{company_slug}_{project_slug}"

    # Load original path (base DXF)
    company_dxf_path = {
        1: os.path.join(settings.BASE_DIR, "static", "aDxfs", "AAA", f"AAA_{category}.dxf"),
        2: os.path.join(settings.BASE_DIR, "static", "aDxfs", "BBB", f"{category}.dxf"),
    }
    static_path = company_dxf_path.get(user_company.id)
    if not static_path or not os.path.exists(static_path):
        raise FileNotFoundError(f"DXF not found: {static_path}")

    # Target output path for modified DXF
    target_dir = os.path.join(
        settings.BASE_DIR,
        "static",
        "aReports",
        company_slug.upper(),
        folder_name
    )
    os.makedirs(target_dir, exist_ok=True)

    modified_path = os.path.join(target_dir, f"{category}_new.dxf")

    return static_path, modified_path
    

# Helper function to modify DXF files
def modify_saved_dxf_file(static_path, modified_path, modifications):
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
def process_saved_dxf(request, aMachine_ID, category, project_id, modifications, output_filename):
    # Log the request
    aLogEntry.objects.create(
        user=request.user,
        message=f"at {now()} {request.user} Download DXF {category} {aMachine_ID}"
    )

    user_company = get_user_company(request)
    if not user_company:
        return HttpResponse("Unauthorized", status=403)

    static_path, modified_path = get_saved_dxf_paths(user_company, category, project_id)
    if not os.path.exists(static_path):
        return HttpResponse("File not found", status=404)

    machine = Machine.objects.get(id=aMachine_ID)

    
    modify_saved_dxf_file(static_path, modified_path, modifications(machine))


    # Define PDF output path
    pdf_output_path = modified_path.replace(".dxf", ".pdf")

    try:
        convert_dxf_to_pdf_cloudconvert(modified_path, pdf_output_path)
        print(f"PDF saved to {pdf_output_path}")
    except Exception as e:
        print("DXF to PDF conversion failed:", e)
        return HttpResponse("DXF to PDF conversion failed", status=500)

    return FileResponse(open(pdf_output_path, 'rb'), as_attachment=True, filename=os.path.basename(pdf_output_path))

    

    

# DXF Download Views


def General_saved_DXF_ALL(request, aMachine_ID, aType, project_id):
    
    print(aType)
    
    # Redirect unauthenticated users
    if not request.user.is_authenticated:
        return redirect("login")  
    
    
    ###LOG
    aLogEntry.objects.create(
            user=request.user,
            message=f"at {now()} {request.user} DXF download {aType} "
        )
    
    
    # Get the company of the logged-in user    
    user_company = None
    firstletter = None
    if request.user.is_authenticated:
        try:
            user_company = UserCompany.objects.get(user=request.user).company
            firstletter = user_company.nameCompanies[0]
        except UserCompany.DoesNotExist:
            user_company = None

    
    if aType == f"NS_{firstletter}":
        return process_saved_dxf(
            request,
            aMachine_ID,
            "NS",
            project_id,
            lambda machine: {
                "ScreenLength": machine.oSec02Field06,
                "BarLength": "500",
                "ScreenWidth": machine.oSec02Field04,
                "BarTh": "10",
                "BarSpacing": machine.oSec02Field10,
            },
            f"new_NS_{user_company}.dxf"
        )
        
    
    if aType == f"MS_{firstletter}":
        return process_saved_dxf(
            request,
            aMachine_ID,
            "MS",
            project_id,
            lambda machine: {
                "ChannelHeight": "0000",
                "WaterLevel": "000",
                "Width": machine.oSec02Field08,
                "Length": machine.oSec02Field10,
                "Angle": machine.oSec02Field20,
            },
            f"new_MS_{user_company}.dxf"
        )
        
    if aType == f"BC_{firstletter}":
        return process_saved_dxf(
            request,
            aMachine_ID,
            "BC",
            project_id,
            lambda machine: {
                "Length": machine.oSec02Field04,
                "Width": machine.oSec02Field02,
                "WidB": "000",
                "BarTh": "10",
                "BarSpacing": "25",
            },
            f"new_BC_{user_company}.dxf"
        )
        
    if aType == f"CO_{firstletter}":
        return process_saved_dxf(
            request,
            aMachine_ID,
            "CO",
            project_id,
            lambda machine: {
                "ScreenLength": "1000",
                "BarLength": "500",
                "ScreenWidth": "600",
                "BarTh": "10",
                "BarSpacing": "25",
            },
            f"new_CO_{user_company}.dxf"
        )
        
    if aType == f"GR_{firstletter}":
        return process_saved_dxf(
            request,
            aMachine_ID,
            "GR",
            project_id,
            lambda machine: {
                "ScreenLength": "1000",
                "BarLength": "500",
                "ScreenWidth": "600",
                "BarTh": "10",
                "BarSpacing": "25",
            },
            f"new_GR_{user_company}.dxf"
        )
        
    if aType == f"SS_{firstletter}":
        return process_saved_dxf(
            request,
            aMachine_ID,
            "SS",
            project_id,
            lambda machine: {
                "ScreenLength": "1000",
                "BarLength": "500",
                "ScreenWidth": "600",
                "BarTh": "10",
                "BarSpacing": "25",
            },
            f"new_SS_{user_company}.dxf"
        )
        
    if aType == f"PS_{firstletter}":
        return process_saved_dxf(
            request,
            aMachine_ID,
            "PS",
            project_id,
            lambda machine: {
                "ScreenLength": "1000",
                "BarLength": "500",
                "ScreenWidth": "600",
                "BarTh": "10",
                "BarSpacing": "25",
            },
            f"new_PS_{user_company}.dxf"
        )
        
    if aType == f"QV_{firstletter}":
        return process_saved_dxf(
            request,
            aMachine_ID,
            "QV",
            project_id,
            lambda machine: {
                "ScreenLength": "1000",
                "BarLength": "500",
                "ScreenWidth": "600",
                "BarTh": "10",
                "BarSpacing": "25",
            },
            f"new_QV_{user_company}.dxf"
        )
        
    if aType == f"TV_{firstletter}":
        return process_saved_dxf(
            request,
            aMachine_ID,
            "TV",
            project_id,
            lambda machine: {
                "ScreenLength": "1000",
                "BarLength": "500",
                "ScreenWidth": "600",
                "BarTh": "10",
                "BarSpacing": "25",
            },
            f"new_TV_{user_company}.dxf"
        )
        
    if aType == f"TH_{firstletter}":
        return process_saved_dxf(
            request,
            aMachine_ID,
            "TH",
            project_id,
            lambda machine: {
                "ScreenLength": "1000",
                "BarLength": "500",
                "ScreenWidth": "600",
                "BarTh": "10",
                "BarSpacing": "25",
            },
            f"new_TH_{user_company}.dxf"
        )
        
    
    
# DXF Download Views
def SavedFullDrawing(request, aMachine_ID, aType):
    
    # Helper function to modify DXF files
    def SavedFullDrawing_modify_dxf_file(static_path, modified_path, modifications):
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
    def SavedFullDrawing_process_dxf(request, aMachine_ID, category, modifications, output_filename):

        user_company = get_user_company(request)
        if not user_company:
            return HttpResponse("Unauthorized", status=403)

        # Get machine and project
        machine = Machine.objects.get(id=aMachine_ID)
        project = machine.project  # Assumes FK from Machine to Project
        company_slug = slugify(user_company.nameCompanies)
        project_slug = slugify(project.name)
        folder_name = f"{project.id}_{company_slug}_{project_slug}"


        static_path  = os.path.join(settings.BASE_DIR, "static", "aDxfs", "AAA", "FullDrawing", f"Full Drawing {category}.dxf")
        
        
        if not os.path.exists(static_path):
            return HttpResponse("File not found", status=404)

        # Destination path
        target_dir = os.path.join(
            settings.BASE_DIR, "static", "aReports", company_slug.upper(), folder_name
        )
        os.makedirs(target_dir, exist_ok=True)
        modified_path = os.path.join(target_dir, f"{category}_newFullDrawing.dxf")

        machine = Machine.objects.get(id=aMachine_ID)
        
        SavedFullDrawing_modify_dxf_file(static_path, modified_path, modifications(machine))
        

        

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
        
    ###LOG
    aLogEntry.objects.create(
            user=request.user,
            message=f"at {now()} {request.user} DXF download {aType} "
        )

    
    if aType == f"NS_{firstletter}":
        return SavedFullDrawing_process_dxf(
            request,
            aMachine_ID,
            "NS",
            lambda machine: {
                "ScreenLength": machine.oSec02Field06,
                "BarLength": "500",
                "ScreenWidth": machine.oSec02Field04,
                "BarTh": "10",
                "BarSpacing": machine.oSec02Field10,
            },
            f"newFullDrawing_ManualScreen_{user_company}.dxf"
        )
        
    
    if aType == f"MS_{firstletter}":
        return SavedFullDrawing_process_dxf(
            request,
            aMachine_ID,
            "MS",
            lambda machine: {
                "ChannelHeight": "0000",
                "WaterLevel": "000",
                "Width": machine.oSec02Field08,
                "Length": machine.oSec02Field10,
                "Angle": machine.oSec02Field20,
            },
            f"newFullDrawing_MechanicalScreen_{user_company}.dxf"
        )
        
    if aType == f"BC_{firstletter}":
        return SavedFullDrawing_process_dxf(
            request,
            aMachine_ID,
            "BC",
            lambda machine: {
                "Length": machine.oSec02Field04,
                "Width": machine.oSec02Field02,
                "WidB": "000",
                "BarTh": "10",
                "BarSpacing": "25",
            },
            f"newFullDrawing_BeltConveyor_{user_company}.dxf"
        )
        
    if aType == f"CO_{firstletter}":
        return SavedFullDrawing_process_dxf(
            request,
            aMachine_ID,
            "CO",
            lambda machine: {
                "ScreenLength": "1000",
                "BarLength": "500",
                "ScreenWidth": "600",
                "BarTh": "10",
                "BarSpacing": "25",
            },
            f"newFullDrawing_Container_{user_company}.dxf"
        )
        
    if aType == f"GR_{firstletter}":
        return SavedFullDrawing_process_dxf(
            request,
            aMachine_ID,
            "GR",
            lambda machine: {
                "ScreenLength": "1000",
                "BarLength": "500",
                "ScreenWidth": "600",
                "BarTh": "10",
                "BarSpacing": "25",
            },
            f"newFullDrawing_Gritremoval_{user_company}.dxf"
        )
        
    if aType == f"SS_{firstletter}":
        return SavedFullDrawing_process_dxf(
            request,
            aMachine_ID,
            "SS",
            lambda machine: {
                "ScreenLength": "1000",
                "BarLength": "500",
                "ScreenWidth": "600",
                "BarTh": "10",
                "BarSpacing": "25",
            },
            f"newFullDrawing_SandSilo_{user_company}.dxf"
        )
        
    if aType == f"PS_{firstletter}":
        return SavedFullDrawing_process_dxf(
            request,
            aMachine_ID,
            "PS",
            lambda machine: {
                "ScreenLength": "1000",
                "BarLength": "500",
                "ScreenWidth": "600",
                "BarTh": "10",
                "BarSpacing": "25",
            },
            f"newFullDrawing_PrimarySedimentation_{user_company}.dxf"
        )
        
    if aType == f"QV_{firstletter}":
        return SavedFullDrawing_process_dxf(
            request,
            aMachine_ID,
            "QV",
            lambda machine: {
                "ScreenLength": "1000",
                "BarLength": "500",
                "ScreenWidth": "600",
                "BarTh": "10",
                "BarSpacing": "25",
            },
            f"newFullDrawing_QuickValve_{user_company}.dxf"
        )
        
    if aType == f"TV_{firstletter}":
        return SavedFullDrawing_process_dxf(
            request,
            aMachine_ID,
            "TV",
            lambda machine: {
                "ScreenLength": "1000",
                "BarLength": "500",
                "ScreenWidth": "600",
                "BarTh": "10",
                "BarSpacing": "25",
            },
            f"newFullDrawing_TelescopicValve_{user_company}.dxf"
        )
        
    if aType == f"TH_{firstletter}":
        return SavedFullDrawing_process_dxf(
            request,
            aMachine_ID,
            "TH",
            lambda machine: {
                "ScreenLength": "1000",
                "BarLength": "500",
                "ScreenWidth": "600",
                "BarTh": "10",
                "BarSpacing": "25",
            },
            f"newFullDrawing_SludgeThickener_{user_company}.dxf"
        )
        




def save_pdf_report(request, project_id):
    try:
        #pdb.set_trace()
        # Log the action
        aLogEntry.objects.create(user=request.user, message=f"at {now()} {request.user} accessed Pdf Report")
        
        #pdb.set_trace()
        # Get the user’s company and project
        aCompany = UserCompany.objects.get(user=request.user)

        #pdb.set_trace()
        # Determine the company and generate the corresponding report
        if aCompany.company.nameCompanies == "AAAA":
            print("Company 1")
            return save_pdf_report_AAA(request, project_id)

        elif aCompany.company.nameCompanies == "BBBB":
            print("Company 2")
            return save_pdf_report_BBB(request, project_id)

        else:
            return HttpResponse("Invalid company ID", status=400)

    except UserCompany.DoesNotExist:
        return HttpResponse("User does not belong to a company", status=403)

    except APP_Project.DoesNotExist:
        return HttpResponse("Project not found", status=404)




def save_pdf_report_AAA(request, project_id):
    
    # Define a custom class for the PDF layout
    class PDF(FPDF):
        def __init__(self):
            super().__init__()
            self.set_auto_page_break(auto=True, margin=15)

            # Add the TrueType Unicode font (DejaVuSans)
            self.add_font('DejaVu', '', 'static/aFonts/DejaVuSans.ttf', uni=True)  # Regular
            self.add_font('DejaVu', 'B', 'static/aFonts/DejaVuSans-Bold.ttf', uni=True)  # Bold
            self.add_font('DejaVu', 'I', 'static/aFonts/DejaVuSerif-Italic.ttf', uni=True)  # Italic
            self.set_font('DejaVu', '', 12)

        def header_page(self, projectname, clientname, capacity):
            self.set_y(50)
            self.set_font("DejaVu", "B", 16)
            self.set_text_color(33, 66, 133)
            self.cell(0, 20, f"Project Report: {projectname}", ln=True,) 
            self.set_font("DejaVu", "B", 14)
            self.cell(0, 10, f"Project Details", ln=True,) 
            self.set_text_color(0, 0, 0)
            self.set_font("DejaVu", "", 12)
            self.cell(0, 10, f"Name:  {projectname}", ln=True,) 
            self.cell(0, 10, f"Client Name:  {clientname}", ln=True,) 
            self.cell(0, 10, f"Capacity: {capacity}", ln=True,) 

        def header(self):
            # Logo
            page_width = self.w - 2 * self.l_margin
            
            try:
                self.image("static/aLogo/LogoAAA.PNG", x=self.l_margin, y=10, w=page_width)  

                # Move cursor below image to avoid overlapping next content
                self.set_y(10 + 50)
            except Exception as e:
                print(f"Error loading logo: {e}")


        def footer(self):
            self.set_y(-15)  # Position 15 mm from bottom
            self.set_font("DejaVu", "I", 8)
            self.set_text_color(128)

            # Add "Page X of Y"
            self.cell(0, 10, f"Page {self.page_no()} of {{nb}}", align='C')

        def colored_header(self, number, name):
            self.set_font("DejaVu", "B", 16)
            self.set_text_color(33, 66, 133)
            
            text = f"{number}. {name}"
            text_width = self.get_string_width(text) + 2  # Optional padding
            text_height = 10  # Height for one line of text

            # Page dimensions
            page_width = self.w
            page_height = self.h

            # Center position
            x = (page_width - text_width) / 2
            y = (page_height - text_height) / 2

            self.set_xy(x, y)
            self.cell(text_width, text_height, text, border=0, align='C')

        def section_title(self, title):
            self.set_font("DejaVu", "B", 12)
            self.set_text_color(33, 66, 133)
            self.ln(5)
            self.cell(0, 10, title, ln=True)

        def add_table(self, data):
            self.set_font("DejaVu", "B", 10)
            self.set_fill_color(255, 153, 0)
            self.set_text_color(0)
            self.cell(60, 8, "Field", border=1, fill=True)
            self.cell(130, 8, "Value", border=1, ln=True, fill=True)

            self.set_font("DejaVu", "", 10)
            for field, value in data:
                self.cell(60, 8, field, border=1)
                self.cell(130, 8, value, border=1, ln=True)
    
    
    try:
        
        ###LOG
        aLogEntry.objects.create(
                user=request.user,
                message=f"at {now()} {request.user} accessed Load  "
            )
        print(f"at {now()} {User} accessed Save Report")
        ###LOG

        aCompany = UserCompany.objects.get(user=request.user)
        company_id = aCompany.company
        project = APP_Project.objects.get(id=project_id)
        machines = Machine.objects.filter(project=project)
        # Define the folder path
        company_slug = slugify(project.company.nameCompanies)
        project_slug = slugify(project.name)
        folder_name = slugify(f"{project_id}_{company_slug}_{project_slug}")

        project_folder = os.path.join(settings.BASE_DIR, 'static', 'aReports', company_slug, folder_name)
        os.makedirs(project_folder, exist_ok=True)  # Create folder if it doesn't exist

        
        pdf_file_path = os.path.join(project_folder, f"all_{project_slug}_report.pdf")

        print(aCompany.id)
        print(project.id)
    
        print("Company 1")
    

        
        output = PdfWriter()

        # Create a Pdf document
        pdf = PDF()

        pdf.alias_nb_pages()  # Important for "of {nb}" to work
        pdf.add_page()
        
        
        pdf.header_page(project.name,  project.client_name, project.capacity)
        pdf.output(pdf_file_path)

        mainreader = PdfReader(pdf_file_path)

        for page in mainreader.pages:
            output.add_page(page)
        
        # clean up
        os.remove(pdf_file_path)

        # Add machine details
        for index, machine in enumerate(machines, start=1):  # Add numbering
            machine_name = machine.oSec00Field03
            section_titles = []
            if machine_name == "DataSheetNS":
                machine_name = "Manual Screen" 
                sheet_key = "NS"
                section_titles = ["General Data", "Design Data", "Material Data", "Channel Data", " ", " ", " ", " ", " ", " "]

            if machine_name == "DataSheetMS":
                machine_name = "Mechanical Screen"
                sheet_key = "MS" 
                section_titles = ["General Data", "Design Data", "Gearmotor Data", "Control panel Data", "Material Data", "Other Data", " ", " ", " ", " "]

            if machine_name == "DataSheetBC":
                machine_name = "Belt Conveyor"
                sheet_key = "BC"
                section_titles = ["General Data", "Design Data", "Gearbox Data", "Motor Data", "Material Data", " ", " ", " ", " ", " "]

            if machine_name == "DataSheetCO":
                machine_name = "Container"
                sheet_key = "CO"
                section_titles = ["General Data", "Design Data", "Material Data", " ", " ", " ", " ", " ", " ", " "]

            if machine_name == "DataSheetGR":
                machine_name = "Gritremoval"
                sheet_key = "GR"
                section_titles = ["General Data", "Design Data", "Walkway, Handrail, Wheel Data", "Scrapper Data", "Gearmotor Data", "Scrapper Data", "Drive unit", "Control panel Data", "Material Data ", " "]

            if machine_name == "DataSheetSS":
                machine_name = "Sand Silo"
                sheet_key = "SS"

            if machine_name == "DataSheetPS":
                machine_name = "Primary Sedimentation"
                sheet_key = "PS"

            if machine_name == "DataSheetQV":
                machine_name = "Quick Valve"
                sheet_key = "QV"

            if machine_name == "DataSheetTV":
                machine_name = "Telescopic Valve"
                sheet_key = "TV"
                
            if machine_name == "DataSheetTH":
                machine_name = "Sludge Thickener"
                sheet_key = "TH"


            # Add machine name 
            pdf = PDF()
            pdf.alias_nb_pages()  
            pdf.add_page()
            pdf.colored_header(index, machine_name)

            
            pdf.alias_nb_pages()  
            pdf.add_page()

            for i in range(1, 11):  # Loop from Sec01 to Sec10
                section_name = f"Sec{i:02d}"
                pdf_section_data = []

                for j in range(1, 21, 2):  # Step by 2 to avoid duplication
                    key = getattr(machine, f"o{section_name}Field{j:02d}", "").strip()
                    value = getattr(machine, f"o{section_name}Field{j+1:02d}", "").strip()

                    if key and value and key.lower() != "oooo" and value.lower() != "oooo":
                        pdf_section_data.append((key, value))

                if len(pdf_section_data) > 1:  # If the section has valid data, create a table
                    section_title = section_titles[i-1] if i-1 < len(section_titles) else f"Section {i}"
                    pdf.section_title(f"{section_name}: {section_title}")
                    pdf.add_table(pdf_section_data)

            
            pdf.output(pdf_file_path)

            mainreader = PdfReader(pdf_file_path)

            for page in mainreader.pages:
                output.add_page(page)

            # clean up
            os.remove(pdf_file_path)
            

            appendix = PdfReader(f"static/aReports/{company_slug.upper()}/{folder_name}/{sheet_key}_new.pdf")

            
            for page in appendix.pages:
                output.add_page(page)

        # Save the new PDF
        with open(pdf_file_path, "wb") as f:
            output.write(f)

        return HttpResponse(status=204)
        

        

    except APP_Project.DoesNotExist:
        return HttpResponse("Project not found", status=404)


def save_pdf_report_BBB(request, project_id):
    
    # Define a custom class for the PDF layout
    class PDF(FPDF):
        def __init__(self):
            super().__init__()
            self.set_auto_page_break(auto=True, margin=15)

            # Add the TrueType Unicode font (DejaVuSans)
            self.add_font('DejaVu', '', 'static/aFonts/DejaVuSans.ttf', uni=True)  # Regular
            self.add_font('DejaVu', 'B', 'static/aFonts/DejaVuSans-Bold.ttf', uni=True)  # Bold
            self.add_font('DejaVu', 'I', 'static/aFonts/DejaVuSerif-Italic.ttf', uni=True)  # Italic
            self.set_font('DejaVu', '', 12)

        def header_page(self, projectname, clientname, capacity):
            self.set_y(50)
            self.set_font("DejaVu", "B", 16)
            self.set_text_color(33, 66, 133)
            self.cell(0, 20, f"Project Report: {projectname}", ln=True,) 
            self.set_font("DejaVu", "B", 14)
            self.cell(0, 10, f"Project Details", ln=True,) 
            self.set_text_color(0, 0, 0)
            self.set_font("DejaVu", "", 12)
            self.cell(0, 10, f"Name:  {projectname}", ln=True,) 
            self.cell(0, 10, f"Client Name:  {clientname}", ln=True,) 
            self.cell(0, 10, f"Capacity: {capacity}", ln=True,) 

        def header(self):
            # Logo
            page_width = self.w - 2 * self.l_margin
            
            try:
                self.image("static/aLogo/LogoBBB.PNG", x=self.l_margin, y=10, w=page_width)  

                # Move cursor below image to avoid overlapping next content
                self.set_y(10 + 50)
            except Exception as e:
                print(f"Error loading logo: {e}")


        def footer(self):
            self.set_y(-15)  # Position 15 mm from bottom
            self.set_font("DejaVu", "I", 8)
            self.set_text_color(128)

            # Add "Page X of Y"
            self.cell(0, 10, f"Page {self.page_no()} of {{nb}}", align='C')

        def colored_header(self, number, name):
            self.set_font("DejaVu", "B", 16)
            self.set_text_color(33, 66, 133)
            
            text = f"{number}. {name}"
            text_width = self.get_string_width(text) + 2  # Optional padding
            text_height = 10  # Height for one line of text

            # Page dimensions
            page_width = self.w
            page_height = self.h

            # Center position
            x = (page_width - text_width) / 2
            y = (page_height - text_height) / 2

            self.set_xy(x, y)
            self.cell(text_width, text_height, text, border=0, align='C')

        def section_title(self, title):
            self.set_font("DejaVu", "B", 12)
            self.set_text_color(33, 66, 133)
            self.ln(5)
            self.cell(0, 10, title, ln=True)

        def add_table(self, data):
            self.set_font("DejaVu", "B", 10)
            self.set_fill_color(255, 153, 0)
            self.set_text_color(0)
            self.cell(60, 8, "Field", border=1, fill=True)
            self.cell(130, 8, "Value", border=1, ln=True, fill=True)

            self.set_font("DejaVu", "", 10)
            for field, value in data:
                self.cell(60, 8, field, border=1)
                self.cell(130, 8, value, border=1, ln=True)
    
    
    try:
        
        ###LOG
        aLogEntry.objects.create(
                user=request.user,
                message=f"at {now()} {request.user} accessed Load  "
            )
        print(f"at {now()} {User} accessed Save Report")
        ###LOG

        aCompany = UserCompany.objects.get(user=request.user)
        company_id = aCompany.company
        project = APP_Project.objects.get(id=project_id)
        machines = Machine.objects.filter(project=project)
        # Define the folder path
        company_slug = slugify(project.company.nameCompanies)
        project_slug = slugify(project.name)
        folder_name = slugify(f"{project_id}_{company_slug}_{project_slug}")

        project_folder = os.path.join(settings.BASE_DIR, 'static', 'aReports', company_slug, folder_name)
        os.makedirs(project_folder, exist_ok=True)  # Create folder if it doesn't exist

        
        pdf_file_path = os.path.join(project_folder, f"all_{project_slug}_report.pdf")

        print(aCompany.id)
        print(project.id)
    
        print("Company 2")
    

        
        output = PdfWriter()

        # Create a Pdf document
        pdf = PDF()

        pdf.alias_nb_pages()  # Important for "of {nb}" to work
        pdf.add_page()
        
        
        pdf.header_page(project.name,  project.client_name, project.capacity)
        pdf.output(pdf_file_path)

        mainreader = PdfReader(pdf_file_path)

        for page in mainreader.pages:
            output.add_page(page)
        
        # clean up
        os.remove(pdf_file_path)

        # Add machine details
        for index, machine in enumerate(machines, start=1):  # Add numbering
            machine_name = machine.oSec00Field03
            section_titles = []
            if machine_name == "DataSheetNS":
                machine_name = "Manual Screen" 
                sheet_key = "NS"
                section_titles = ["General Data", "Design Data", "Material Data", "Channel Data", " ", " ", " ", " ", " ", " "]

            if machine_name == "DataSheetMS":
                machine_name = "Mechanical Screen"
                sheet_key = "MS" 
                section_titles = ["General Data", "Design Data", "Gearmotor Data", "Control panel Data", "Material Data", "Other Data", " ", " ", " ", " "]

            if machine_name == "DataSheetBC":
                machine_name = "Belt Conveyor"
                sheet_key = "BC"
                section_titles = ["General Data", "Design Data", "Gearbox Data", "Motor Data", "Material Data", " ", " ", " ", " ", " "]

            if machine_name == "DataSheetCO":
                machine_name = "Container"
                sheet_key = "CO"
                section_titles = ["General Data", "Design Data", "Material Data", " ", " ", " ", " ", " ", " ", " "]

            if machine_name == "DataSheetGR":
                machine_name = "Gritremoval"
                sheet_key = "GR"
                section_titles = ["General Data", "Design Data", "Walkway, Handrail, Wheel Data", "Scrapper Data", "Gearmotor Data", "Scrapper Data", "Drive unit", "Control panel Data", "Material Data ", " "]

            if machine_name == "DataSheetSS":
                machine_name = "Sand Silo"
                sheet_key = "SS"

            if machine_name == "DataSheetPS":
                machine_name = "Primary Sedimentation"
                sheet_key = "PS"

            if machine_name == "DataSheetQV":
                machine_name = "Quick Valve"
                sheet_key = "QV"

            if machine_name == "DataSheetTV":
                machine_name = "Telescopic Valve"
                sheet_key = "TV"
                
            if machine_name == "DataSheetTH":
                machine_name = "Sludge Thickener"
                sheet_key = "TH"


            # Add machine name 
            pdf = PDF()
            pdf.alias_nb_pages()  
            pdf.add_page()
            pdf.colored_header(index, machine_name)

            
            pdf.alias_nb_pages()  
            pdf.add_page()

            for i in range(1, 11):  # Loop from Sec01 to Sec10
                section_name = f"Sec{i:02d}"
                pdf_section_data = []

                for j in range(1, 21, 2):  # Step by 2 to avoid duplication
                    key = getattr(machine, f"o{section_name}Field{j:02d}", "").strip()
                    value = getattr(machine, f"o{section_name}Field{j+1:02d}", "").strip()

                    if key and value and key.lower() != "oooo" and value.lower() != "oooo":
                        pdf_section_data.append((key, value))

                if len(pdf_section_data) > 1:  # If the section has valid data, create a table
                    section_title = section_titles[i-1] if i-1 < len(section_titles) else f"Section {i}"
                    pdf.section_title(f"{section_name}: {section_title}")
                    pdf.add_table(pdf_section_data)

            
            pdf.output(pdf_file_path)

            mainreader = PdfReader(pdf_file_path)

            for page in mainreader.pages:
                output.add_page(page)

            # clean up
            os.remove(pdf_file_path)


            appendix = PdfReader(f"static/aReports/{company_slug.upper()}/{folder_name}/{sheet_key}_new.pdf")

            
            for page in appendix.pages:
                output.add_page(page)

        # Save the new PDF
        with open(pdf_file_path, "wb") as f:
            output.write(f)

        return HttpResponse(status=204)
        

        

    except APP_Project.DoesNotExist:
        return HttpResponse("Project not found", status=404)

