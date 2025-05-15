from django.shortcuts import render

from config import settings
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
from django.shortcuts import render, redirect
from django.utils.timezone import now 
from django.contrib.auth.models import User




from django.utils.text import slugify
from io import BytesIO


import os
import ezdxf

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

from ezdxf import recover
from ezdxf.addons.drawing import Frontend, RenderContext
from ezdxf.addons.drawing import matplotlib as ezdxf_matplotlib


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







def word_submittal_report(request, project_id, logo, color):
    
    def add_table(doc, data, title=None):
        """Creates a borderless table and applies a background color to the header."""
        if title:
            doc.add_heading(title, level=3)

        table = doc.add_table(rows=len(data), cols=2)

        if logo == "LogoBBB": 
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
        elif logo == "LogoAAA":
            table.style = "Table Grid"

        for i, row in enumerate(data):
            for j, text in enumerate(row):
                cell = table.cell(i, j)
                cell.text = text

                # Apply background color only to the header row (first row)
                if i == 0:
                    shading_elm = OxmlElement("w:shd")
                    shading_elm.set(ns.qn("w:val"), "clear")  # Set shading value
                    shading_elm.set(ns.qn("w:fill"), color)  # Light blue color
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
            run_logo.add_picture(f"static/aLogo/{logo}.PNG", width=Inches(7.0))  # Adjust width as needed
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
        company_id = aCompany.company
        project = APP_Project.objects.get(id=project_id)
        machines = Machine.objects.filter(project=project)
        
        
        print(aCompany.id)
        print(project.id)
    
        print("Company 2")
    
    
        # Create a Word document
        doc = Document()

        # Add header and footer with page numbers
        add_header_footer(doc)

        for _ in range(3):  # Adjust this number based on how centered you want it
            para = doc.add_paragraph()
            para.alignment = WD_ALIGN_PARAGRAPH.CENTER

        # Centered content
        lines = [
            "Project Name: ",
            project.name,
            "Client Name: ",
            project.client_name,
            "Capacity: ",
            project.capacity,
        ]

        for line in lines:
            para = doc.add_paragraph()
            run = para.add_run(line)
            run.font.size = Pt(25) 
            para.alignment = WD_ALIGN_PARAGRAPH.CENTER

        # Add spacing after if needed
        para = doc.add_paragraph("\n")
        para.alignment = WD_ALIGN_PARAGRAPH.CENTER
        
        doc.add_page_break()     
        doc.add_paragraph("\n")

        # Add machine details
        for index, machine in enumerate(machines, start=1):  # Add numbering
            machine_name = machine.oSec00Field03
            machine_DB = machine.oSec00Field03
            
            try:
                themachines = AddMachine.objects.get(nameDB=machine_DB, company=company_id)
            except AddMachine.DoesNotExist:
                print(f"Skipping machine '{machine_DB}' for company ID {company_id}: not found in AddMachine.")
                continue  # Skip this machine and continue with the rest
            
            themachinename = themachines.nameMachine
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
            machine_title = doc.add_paragraph(f"{index}. {themachinename}", style="Heading3")
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


def word_calculation_report(request, project_id, logo, color):
    
    def add_table(doc, data, title=None):
        """Creates a borderless table and applies a background color to the header."""
        if title:
            doc.add_heading(title, level=3)

        table = doc.add_table(rows=len(data), cols=2)

        if logo == "LogoBBB": 
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
        elif logo == "LogoAAA":
            table.style = "Table Grid"

        for i, row in enumerate(data):
            for j, text in enumerate(row):
                cell = table.cell(i, j)
                cell.text = text

                # Apply background color only to the header row (first row)
                if i == 0:
                    shading_elm = OxmlElement("w:shd")
                    shading_elm.set(ns.qn("w:val"), "clear")  # Set shading value
                    shading_elm.set(ns.qn("w:fill"), color)  # Light blue color
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
            run_logo.add_picture(f"static/aLogo/{logo}.PNG", width=Inches(7.0))  # Adjust width as needed
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
        companyname=aCompany.company.nameCompanies
        firstletter = companyname[0]
        project = APP_Project.objects.get(id=project_id)
        machines = modelcalc.objects.filter(project=project)
        
        
        print(aCompany.id)
        print(project.id)
    
        print("Company 2")
    
    
        # Create a Word document
        doc = Document()

        # Add header and footer with page numbers
        add_header_footer(doc)

        for _ in range(4):  # Adjust this number based on how centered you want it
            para = doc.add_paragraph()
            para.alignment = WD_ALIGN_PARAGRAPH.CENTER

        # Centered content
        lines = [
            "Project Name: ",
            project.name,
            "Client Name: ",
            project.client_name,
            "Capacity: ",
            project.capacity,
        ]

        for line in lines:
            para = doc.add_paragraph()
            run = para.add_run(line)
            run.font.size = Pt(25) 
            para.alignment = WD_ALIGN_PARAGRAPH.CENTER

        # Add spacing after if needed
        para = doc.add_paragraph("\n")
        para.alignment = WD_ALIGN_PARAGRAPH.CENTER
        
        doc.add_page_break()     
        doc.add_paragraph("\n")

        # Add machine details
        for index, machine in enumerate(machines, start=1):  # Add numbering
            machine_name = machine.oSec00Field03
            section_titles = []

            if machine_name == f"NS_{firstletter}":
                machine_name = "Manual Screen" 
                section_titles = ["Inputs", "Outputs"]

            if machine_name == f"MS_{firstletter}":
                machine_name = "Mechanical Screen" 
                section_titles = ["Inputs", "Outputs"]

            if machine_name == f"BC_{firstletter}":
                machine_name = "Belt Conveyor"
                section_titles = ["Inputs", "Outputs"]

            if machine_name == f"CT_{firstletter}":
                machine_name = "Circular Tanks	"
                section_titles = ["Inputs", "Outputs"]

            if machine_name == f"GR_{firstletter}":
                machine_name = "Gritremoval"
                section_titles = ["Inputs", "Outputs"]

            if machine_name == f"SC_{firstletter}":
                machine_name = "Screw Conveyor"
                section_titles = ["Inputs", "Outputs"]

            if machine_name == f"PS_{firstletter}":
                machine_name = "Primary Sedimentation"
                section_titles = ["Inputs", "Outputs"]

            if machine_name == f"MX_{firstletter}":
                machine_name = "Rectangular Mixers"
                section_titles = ["Inputs", "Outputs"]

            if machine_name == f"RT_{firstletter}":
                machine_name = "Rectangular Tanks"
                section_titles = ["Inputs", "Outputs"]
                
            if machine_name == f"TH_{firstletter}":
                machine_name = "Sludge Thickener"
                section_titles = ["Inputs", "Outputs"]
                
            if machine_name == f"BS_{firstletter}":
                machine_name = "Basket screens"
                section_titles = ["Inputs", "Outputs"]
                
            if machine_name == f"PNch_{firstletter}":
                machine_name = "Channel Penstocks"
                section_titles = ["Inputs", "Outputs"]
                
            if machine_name == f"PNwa_{firstletter}":
                machine_name = "Wall Penstocks"
                section_titles = ["Inputs", "Outputs"]

            # Add machine title with font size 14 and numbering
            machine_title = doc.add_paragraph(f"{index}. {machine_name}", style="Heading3")
            machine_title.runs[0].font.size = Pt(14)

            for i in range(1, 3):  # Loop from Sec01 to Sec02
                section_name = f"Sec{i:02d}"
                section_data = [("Field", "Value")]

                for j in range(1, 31, 2):  # Step by 2 to avoid duplication
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




def save_word_pdf_submittal_report(request, project_id, logo, color):
    
    def add_table(doc, data, title=None):
        """Creates a borderless table and applies a background color to the header."""
        if title:
            doc.add_heading(title, level=3)

        table = doc.add_table(rows=len(data), cols=2)

        if logo == "LogoBBB": 
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
        elif logo == "LogoAAA":
            table.style = "Table Grid"

        for i, row in enumerate(data):
            for j, text in enumerate(row):
                cell = table.cell(i, j)
                cell.text = text

                # Apply background color only to the header row (first row)
                if i == 0:
                    shading_elm = OxmlElement("w:shd")
                    shading_elm.set(ns.qn("w:val"), "clear")  # Set shading value
                    shading_elm.set(ns.qn("w:fill"), color)  # Light blue color
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
            run_logo.add_picture(f"static/aLogo/{logo}.PNG", width=Inches(7.0))  # Adjust width as needed
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
            self.add_font('DejaVu', '', 'static/aApp1/fonts/DejaVu/DejaVuSans.ttf', uni=True)  # Regular
            self.add_font('DejaVu', 'B', 'static/aApp1/fonts/DejaVu/DejaVuSans-Bold.ttf', uni=True)  # Bold
            self.add_font('DejaVu', 'I', 'static/aApp1/fonts/DejaVu/DejaVuSerif-Italic.ttf', uni=True)  # Italic
            self.set_font('DejaVu', '', 12)

        def header_footer(self, projectname, clientname, capacity):
            self.set_y(50)
            
            
            page_height = self.h
            top_margin = self.t_margin
            bottom_margin = self.b_margin

            
            lines = [
                ("Project Name: ", "", 14, (0, 0, 0)),
                (projectname, "", 14, (0, 0, 0)),
                ("Client Name: ", "", 14, (0, 0, 0)),
                (clientname, "", 14, (0, 0, 0)),
                ("Capacity: ", "", 14, (0, 0, 0)),
                (capacity, "", 14, (0, 0, 0)),
            ]

            
            line_height = 16
            total_content_height = line_height * len(lines)

            
            y_position = (page_height - total_content_height) / 2
            self.set_y(y_position)

            
            for text, style, size, color in lines:
                self.set_font("DejaVu", style, size)
                self.set_text_color(*color)
                self.cell(0, line_height, text, ln=True, align="C")

        def header(self):
            # Logo
            page_width = self.w - 2 * self.l_margin
            
            try:
                self.image(f"static/aLogo/{logo}.PNG", x=self.l_margin, y=10, w=page_width)  

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
            if logo == "LogoAAA":
                self.set_fill_color(255, 153, 0)
                tableborder = 1
            elif logo == "LogoBBB": 
                self.set_fill_color(173, 216, 230)
                tableborder = 0
            self.set_text_color(0)
            self.cell(80, 8, "Field", border=tableborder, fill=True)
            self.cell(110, 8, "Value", border=tableborder, ln=True, fill=True)

            self.set_font("DejaVu", "", 10)
            for field, value in data:
                self.cell(80, 8, field, border=tableborder)
                self.cell(110, 8, value, border=tableborder, ln=True)
    
    
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

        pdf.header_footer(project.name,  project.client_name, project.capacity) 

        for _ in range(4):  # Adjust this number based on how centered you want it
            para = doc.add_paragraph()
            para.alignment = WD_ALIGN_PARAGRAPH.CENTER

        # Centered content
        lines = [
            "Project Name: ",
            project.name,
            "Client Name: ",
            project.client_name,
            "Capacity: ",
            project.capacity,
        ]

        for line in lines:
            para = doc.add_paragraph()
            run = para.add_run(line)
            run.font.size = Pt(25) 
            para.alignment = WD_ALIGN_PARAGRAPH.CENTER

        # Add spacing after if needed
        para = doc.add_paragraph("\n")
        para.alignment = WD_ALIGN_PARAGRAPH.CENTER
        
        doc.add_page_break()     
        doc.add_paragraph("\n")

        # Add machine details
        for index, machine in enumerate(machines, start=1):  # Add numbering
            machine_name = machine.oSec00Field03
            machine_DB = machine.oSec00Field03
            machine_ID = machine.id
            
            try:
                themachines = AddMachine.objects.get(nameDB=machine_DB, company=company_id)
            except AddMachine.DoesNotExist:
                print(f"Skipping machine '{machine_DB}' for company ID {company_id}: not found in AddMachine.")
                continue  # Skip this machine and continue with the rest
            
            sheet_key = themachines.keyValue
            themachinename = themachines.nameMachine
            General_saved_DXF_ALL(request, machine_ID, sheet_key, project_id)
            SavedFullDrawing(request, machine_ID, sheet_key)


            
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
            machine_title = doc.add_paragraph(f"{index}. {themachinename}", style="Heading3")
            machine_title.runs[0].font.size = Pt(14)
            
            pdf.alias_nb_pages()  # Important for "of {nb}" to work
            pdf.add_page()
            pdf.colored_header(index, themachinename)

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


def convert_dxf_to_pdf_ezdxf(input_path, output_path):
    try:
        doc = ezdxf.recover.readfile(input_path)[0]
        ezdxf_matplotlib.qsave(
            doc.modelspace(),
            output_path,
            dpi=300,
            size_inches=(36, 24),  # Custom paper size
            bg='#FFFFFF'
        )

        print(f"PDF successfully saved to {output_path}")

    except Exception as e:
        print(f"Error converting DXF to PDF: {e}")
        raise


# Helper function to define DXF paths
def get_saved_dxf_paths(user_company, category, project_id, output_filename):
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
        #raise FileNotFoundError(f"DXF not found: {static_path}")
        print(f"DXF not found: {static_path}")

    # Target output path for modified DXF
    target_dir = os.path.join(
        settings.BASE_DIR,
        "static",
        "aReports",
        company_slug.upper(),
        folder_name
    )
    os.makedirs(target_dir, exist_ok=True)

    
    modified_path = os.path.join(target_dir, output_filename)

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

    static_path, modified_path = get_saved_dxf_paths(user_company, category, project_id, output_filename)
    if not os.path.exists(static_path):
        return HttpResponse("File not found", status=404)

    machine = Machine.objects.get(id=aMachine_ID)

    
    modify_saved_dxf_file(static_path, modified_path, modifications(machine))


    # Define PDF output path
    pdf_output_path = modified_path.replace(".dxf", ".pdf")

    try:
        convert_dxf_to_pdf_ezdxf(modified_path, pdf_output_path)
        print(f"PDF saved to {pdf_output_path}")
    except Exception as e:
        print("DXF to PDF conversion failed:", e)
        return HttpResponse("DXF to PDF conversion failed", status=500)


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
    
    machine = AddMachine.objects.get(keyValue = aType)
    file_model_name = machine.nameDXF
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
            f"{file_name}.dxf"
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
            f"{file_name}.dxf"
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
            f"{file_name}.dxf"
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
            f"{file_name}.dxf"
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
            f"{file_name}.dxf"
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
            f"{file_name}.dxf"
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
            f"{file_name}.dxf"
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
            f"{file_name}.dxf"
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
            f"{file_name}.dxf"
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
            f"{file_name}.dxf"
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
        if output_filename != "None.dxf" :
            modified_path = os.path.join(target_dir, output_filename)
        else :
            modified_path = os.path.join(target_dir, f"{category}_newFullDrawing.dxf")

        machine = Machine.objects.get(id=aMachine_ID)
        
        SavedFullDrawing_modify_dxf_file(static_path, modified_path, modifications(machine))
        

        

        return HttpResponse("Invalid request", status=400)
        

    
    # Redirect unauthenticated users
    if not request.user.is_authenticated:
        return redirect("login") 
    
    
    machine = AddMachine.objects.get(keyValue = aType)
    file_model_name = machine.nameFullDrawing
    sheetkey = aType[0:-2]

    if file_model_name not in ["", None] :
        file_name = file_model_name
    else :
        file_name = f"{sheetkey}_newFullDrawing"

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
            f"{file_name}.dxf"
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
            f"{file_name}.dxf"
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
            f"{file_name}.dxf"
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
            f"{file_name}.dxf"
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
            f"{file_name}.dxf"
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
            f"{file_name}.dxf"
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
            f"{file_name}.dxf"
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
            f"{file_name}.dxf"
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
            f"{file_name}.dxf"
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
            f"{file_name}.dxf"
        )

def save_word_pdf_calculation_report(request, project_id, logo, color):
    
    def add_table(doc, data, title=None):
        """Creates a borderless table and applies a background color to the header."""
        if title:
            doc.add_heading(title, level=3)

        table = doc.add_table(rows=len(data), cols=2)

        if logo == "LogoBBB": 
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
        elif logo == "LogoAAA":
            table.style = "Table Grid"

        for i, row in enumerate(data):
            for j, text in enumerate(row):
                cell = table.cell(i, j)
                cell.text = text

                # Apply background color only to the header row (first row)
                if i == 0:
                    shading_elm = OxmlElement("w:shd")
                    shading_elm.set(ns.qn("w:val"), "clear")  # Set shading value
                    shading_elm.set(ns.qn("w:fill"), color)  # Light blue color
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
            run_logo.add_picture(f"static/aLogo/{logo}.PNG", width=Inches(7.0))  # Adjust width as needed
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
            self.add_font('DejaVu', '', 'static/aApp1/fonts/DejaVu/DejaVuSans.ttf', uni=True)  # Regular
            self.add_font('DejaVu', 'B', 'static/aApp1/fonts/DejaVu/DejaVuSans-Bold.ttf', uni=True)  # Bold
            self.add_font('DejaVu', 'I', 'static/aApp1/fonts/DejaVu/DejaVuSerif-Italic.ttf', uni=True)  # Italic
            self.set_font('DejaVu', '', 12)

        def header_footer(self, projectname, clientname, capacity):
            self.set_y(50)
            
            page_height = self.h
            top_margin = self.t_margin
            bottom_margin = self.b_margin

            
            lines = [
                ("Project Name: ", "", 14, (0, 0, 0)),
                (projectname, "", 14, (0, 0, 0)),
                ("Client Name: ", "", 14, (0, 0, 0)),
                (clientname, "", 14, (0, 0, 0)),
                ("Capacity: ", "", 14, (0, 0, 0)),
                (capacity, "", 14, (0, 0, 0)),
            ]

            
            line_height = 16
            total_content_height = line_height * len(lines)

            
            y_position = (page_height - total_content_height) / 2
            self.set_y(y_position)

            
            for text, style, size, color in lines:
                self.set_font("DejaVu", style, size)
                self.set_text_color(*color)
                self.cell(0, line_height, text, ln=True, align="C")

        def header(self):
            # Logo
            page_width = self.w - 2 * self.l_margin
            
            try:
                self.image(f"static/aLogo/{logo}.PNG", x=self.l_margin, y=10, w=page_width)  

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
            if logo == "LogoAAA":
                self.set_fill_color(255, 153, 0)
                tableborder = 1
            elif logo == "LogoBBB": 
                self.set_fill_color(173, 216, 230)
                tableborder = 0
            self.set_text_color(0)
            self.cell(80, 8, "Field", border=tableborder, fill=True)
            self.cell(110, 8, "Value", border=tableborder, ln=True, fill=True)

            self.set_font("DejaVu", "", 10)
            for field, value in data:
                self.cell(80, 8, field, border=tableborder)
                self.cell(110, 8, value, border=tableborder, ln=True)
    
    
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

        pdf.header_footer(project.name,  project.client_name, project.capacity)

        for _ in range(4):  # Adjust this number based on how centered you want it
            para = doc.add_paragraph()
            para.alignment = WD_ALIGN_PARAGRAPH.CENTER

        # Centered content
        lines = [
            "Project Name: ",
            project.name,
            "Client Name: ",
            project.client_name,
            "Capacity: ",
            project.capacity,
        ]

        for line in lines:
            para = doc.add_paragraph()
            run = para.add_run(line)
            run.font.size = Pt(25) 
            para.alignment = WD_ALIGN_PARAGRAPH.CENTER

        # Add spacing after if needed
        para = doc.add_paragraph("\n")
        para.alignment = WD_ALIGN_PARAGRAPH.CENTER
        
        doc.add_page_break()     
        doc.add_paragraph("\n")

        # Add machine details
        for index, machine in enumerate(machines, start=1):  # Add numbering
            machine_name = machine.oSec00Field03
            section_titles = []

            if machine_name == f"NS_{firstletter}":
                machine_name = "Manual Screen" 
                section_titles = ["Inputs", "Outputs"]

            if machine_name == f"MS_{firstletter}":
                machine_name = "Mechanical Screen" 
                section_titles = ["Inputs", "Outputs"]

            if machine_name == f"BC_{firstletter}":
                machine_name = "Belt Conveyor"
                section_titles = ["Inputs", "Outputs"]

            if machine_name == f"CT_{firstletter}":
                machine_name = "Circular Tanks	"
                section_titles = ["Inputs", "Outputs"]

            if machine_name == f"GR_{firstletter}":
                machine_name = "Gritremoval"
                section_titles = ["Inputs", "Outputs"]

            if machine_name == f"SC_{firstletter}":
                machine_name = "Screw Conveyor"
                section_titles = ["Inputs", "Outputs"]

            if machine_name == f"PS_{firstletter}":
                machine_name = "Primary Sedimentation"
                section_titles = ["Inputs", "Outputs"]

            if machine_name == f"MX_{firstletter}":
                machine_name = "Rectangular Mixers"
                section_titles = ["Inputs", "Outputs"]

            if machine_name == f"RT_{firstletter}":
                machine_name = "Rectangular Tanks"
                section_titles = ["Inputs", "Outputs"]
                
            if machine_name == f"TH_{firstletter}":
                machine_name = "Sludge Thickener"
                section_titles = ["Inputs", "Outputs"]
                
            if machine_name == f"BS_{firstletter}":
                machine_name = "Basket screens"
                section_titles = ["Inputs", "Outputs"]
                
            if machine_name == f"PNch_{firstletter}":
                machine_name = "Channel Penstocks"
                section_titles = ["Inputs", "Outputs"]
                
            if machine_name == f"PNwa_{firstletter}":
                machine_name = "Wall Penstocks"
                section_titles = ["Inputs", "Outputs"]
            
            # Add machine title with font size 14 and numbering
            machine_title = doc.add_paragraph(f"{index}. {machine_name}", style="Heading3")
            machine_title.runs[0].font.size = Pt(14)
            
            pdf.alias_nb_pages()  # Important for "of {nb}" to work
            pdf.add_page()
            pdf.colored_header(index, machine_name)

            for i in range(1, 3):  # Loop from Sec01 to Sec02
                section_name = f"Sec{i:02d}"
                section_data = [("Field", "Value")]
                pdf_section_data = []

                for j in range(1, 31, 2):  # Step by 2 to avoid duplication
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

        
def save_all_pdf_report(request, project_id, logo):
    
    # Define a custom class for the PDF layout
    class PDF(FPDF):
        def __init__(self):
            super().__init__()
            self.set_auto_page_break(auto=True, margin=15)

            # Add the TrueType Unicode font (DejaVuSans)
            self.add_font('DejaVu', '', 'static/aApp1/fonts/DejaVu/DejaVuSans.ttf', uni=True)  # Regular
            self.add_font('DejaVu', 'B', 'static/aApp1/fonts/DejaVu/DejaVuSans-Bold.ttf', uni=True)  # Bold
            self.add_font('DejaVu', 'I', 'static/aApp1/fonts/DejaVu/DejaVuSerif-Italic.ttf', uni=True)  # Italic
            self.set_font('DejaVu', '', 12)

        def header_page(self, projectname, clientname, capacity):
            self.set_y(50)
            
            page_height = self.h
            top_margin = self.t_margin
            bottom_margin = self.b_margin

            
            lines = [
                ("Project Name: ", "", 14, (0, 0, 0)),
                (projectname, "", 14, (0, 0, 0)),
                ("Client Name: ", "", 14, (0, 0, 0)),
                (clientname, "", 14, (0, 0, 0)),
                ("Capacity: ", "", 14, (0, 0, 0)),
                (capacity, "", 14, (0, 0, 0)),
            ]

            
            line_height = 16
            total_content_height = line_height * len(lines)

            
            y_position = (page_height - total_content_height) / 2
            self.set_y(y_position)

            
            for text, style, size, color in lines:
                self.set_font("DejaVu", style, size)
                self.set_text_color(*color)
                self.cell(0, line_height, text, ln=True, align="C")

        def header(self):
            # Logo
            page_width = self.w - 2 * self.l_margin
            
            try:
                self.image(f"static/aLogo/{logo}.PNG", x=self.l_margin, y=10, w=page_width)  

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
            if logo == "LogoAAA":
                self.set_fill_color(255, 153, 0)
                tableborder = 1
            elif logo == "LogoBBB": 
                self.set_fill_color(173, 216, 230)
                tableborder = 0
            self.set_text_color(0)
            self.cell(80, 8, "Field", border=tableborder, fill=True)
            self.cell(110, 8, "Value", border=tableborder, ln=True, fill=True)

            self.set_font("DejaVu", "", 10)
            for field, value in data:
                self.cell(80, 8, field, border=tableborder)
                self.cell(110, 8, value, border=tableborder, ln=True)
    
    
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
        paragraph_text = project.cover_page_text or "No description provided."

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

        pdf.alias_nb_pages()  # Important for "of {nb}" to work
        pdf.add_page()
        pdf.set_font("DejaVu", "", 12)
        pdf.set_text_color(0)
        pdf.multi_cell(0, 10, paragraph_text, align='L')

        pdf.output(pdf_file_path)

        mainreader = PdfReader(pdf_file_path)

        for page in mainreader.pages:
            output.add_page(page)
        
        # clean up
        os.remove(pdf_file_path)

        # Add machine details
        for index, machine in enumerate(machines, start=1):  # Add numbering
            machine_name = machine.oSec00Field03
            machine_DB = machine.oSec00Field03
            
            try:
                themachines = AddMachine.objects.get(nameDB=machine_DB, company=company_id)
                
            except AddMachine.DoesNotExist:
                print(f"Skipping machine '{machine_name}' for company ID {company_id}: not found in AddMachine.")
                continue  # Skip this machine and continue with the rest
            
            themachinename = themachines.nameMachine
            file_name = themachines.nameDXF

            section_titles = [" ", " ", " ", " ", " ", " ", " ", " ", " ", " "]
            if machine_name == "DataSheetNS":
                machine_name = "Manual Screen" 
                sheet_key = "NS"
                section_titles = ["General Data", "Design Data", "Material Data", "Channel Data", " ", " ", " ", " ", " ", " "]

            elif machine_name == "DataSheetMS":
                machine_name = "Mechanical Screen"
                sheet_key = "MS" 
                section_titles = ["General Data", "Design Data", "Gearmotor Data", "Control panel Data", "Material Data", "Other Data", " ", " ", " ", " "]

            elif machine_name == "DataSheetBC":
                machine_name = "Belt Conveyor"
                sheet_key = "BC"
                section_titles = ["General Data", "Design Data", "Gearbox Data", "Motor Data", "Material Data", " ", " ", " ", " ", " "]

            elif machine_name == "DataSheetCO":
                machine_name = "Container"
                sheet_key = "CO"
                section_titles = ["General Data", "Design Data", "Material Data", " ", " ", " ", " ", " ", " ", " "]

            elif machine_name == "DataSheetGR":
                machine_name = "Gritremoval"
                sheet_key = "GR"
                section_titles = ["General Data", "Design Data", "Walkway, Handrail, Wheel Data", "Scrapper Data", "Gearmotor Data", "Scrapper Data", "Drive unit", "Control panel Data", "Material Data ", " "]

            elif machine_name == "DataSheetSS":
                machine_name = "Sand Silo"
                sheet_key = "SS"

            elif machine_name == "DataSheetPS":
                machine_name = "Primary Sedimentation"
                sheet_key = "PS"

            elif machine_name == "DataSheetQV":
                machine_name = "Quick Valve"
                sheet_key = "QV"

            elif machine_name == "DataSheetTV":
                machine_name = "Telescopic Valve"
                sheet_key = "TV"
                
            elif machine_name == "DataSheetTH":
                machine_name = "Sludge Thickener"
                sheet_key = "TH"


            sheet_key = themachines.keyValue[0:-2]
            # Add machine name 
            pdf = PDF()
            pdf.alias_nb_pages()  
            pdf.add_page()
            pdf.colored_header(index, themachinename)

            
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

            appendix = None
            if os.path.exists(f"static/aReports/{company_slug.upper()}/{folder_name}/{file_name}.pdf") :
                appendix = PdfReader(f"static/aReports/{company_slug.upper()}/{folder_name}/{file_name}.pdf")
            elif os.path.exists(f"static/aReports/{company_slug.upper()}/{folder_name}/{sheet_key}_new.pdf") :
                appendix = PdfReader(f"static/aReports/{company_slug.upper()}/{folder_name}/{sheet_key}_new.pdf")

            if appendix != None:
                for page in appendix.pages:
                    output.add_page(page)

        for i in range(1 , 6):
            emptyappendix = None
            cost_file_name = f"cost{i}_pdf.pdf"
            if os.path.exists(f"static/aReports/{company_slug.upper()}/{folder_name}/{cost_file_name}") :
                emptyappendix = PdfReader(f"static/aReports/{company_slug.upper()}/{folder_name}/{cost_file_name}")

            if emptyappendix != None:
                for page in emptyappendix.pages:
                    output.add_page(page)

        # Save the new PDF
        with open(pdf_file_path, "wb") as f:
            output.write(f)

        return HttpResponse(status=204)
        

        

    except APP_Project.DoesNotExist:
        return HttpResponse("Project not found", status=404)

