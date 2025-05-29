from django.core.mail import send_mail
from django.utils.timezone import now
from .models import APP_Project
from Apps.aAppMechanical.models import UserCompany
from .reports import save_word_pdf_submittal_report, save_word_pdf_calculation_report, save_all_pdf_report

def save_reports_task(project_id, user_id):
    from django.contrib.auth.models import User
    user = User.objects.get(id=user_id)
    project = APP_Project.objects.get(pk=project_id)
    aCompany = UserCompany.objects.get(user=user)

    if aCompany:
        if aCompany.company.nameCompanies == "AAAA":
            save_word_pdf_submittal_report(user, project_id, "LogoAAA", "FFA500")
            save_word_pdf_calculation_report(user, project_id, "LogoAAA", "FFA500")
            save_all_pdf_report(user, project_id, "LogoAAA")
        elif aCompany.company.nameCompanies == "BBBB":
            save_word_pdf_submittal_report(user, project_id, "LogoBBB", "ADD8E6")
            save_word_pdf_calculation_report(user, project_id, "LogoBBB", "ADD8E6")
            save_all_pdf_report(user, project_id, "LogoBBB")
        project.last_saved_time = now()
        project.save()

        # ✅ Send email after saving reports
        send_mail(
            subject=f"✅ Reports Saved: {project.name}",
            message=f"The reports for project '{project.name}' were generated and saved successfully.",
            from_email=None,  # uses DEFAULT_FROM_EMAIL
            recipient_list=[user.email],
            fail_silently=False
        )
        
        print(f"the User's Email is :  {user.email}")
        print(f"the files saved complete for project {project_id}")