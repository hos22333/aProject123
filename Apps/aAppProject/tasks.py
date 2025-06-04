import time
from django.core.mail import send_mail
from django.utils.timezone import now
from django_q.models import Task
from django.contrib.auth.models import User
from .models import APP_Project
from .models import ReportProgress
from Apps.aAppMechanical.models import UserCompany
from .reports import save_word_pdf_submittal_report, save_word_pdf_calculation_report, save_all_pdf_report


def update_progress(user, project_id, percent, status):
    ReportProgress.objects.update_or_create(
        user=user,
        project_id=project_id,
        status=status,
        percent=percent,
        
    )



def save_reports_task(project_id, user_id):
    user = User.objects.get(id=user_id)
    ReportProgress.objects.filter(user=user, project_id=project_id).delete()
    time.sleep(2)
    
    try:
        user = User.objects.get(id=user_id)
        project = APP_Project.objects.get(pk=project_id)
        aCompany = UserCompany.objects.get(user=user)

        update_progress(user, project_id, 10, f"{project.name}_starting")
        time.sleep(2)

        if aCompany:
            if aCompany.company.nameCompanies == "AAAA":
                update_progress(user, project_id, 20, f"{project.name}_submittal report")
                save_word_pdf_submittal_report(user, project_id, "LogoAAA", "FFA500")
                time.sleep(2)

                update_progress(user, project_id, 80, f"{project.name}_calculation report")
                save_word_pdf_calculation_report(user, project_id, "LogoAAA", "FFA500")
                time.sleep(2)

                update_progress(user, project_id, 90, f"{project.name}_final report")
                save_all_pdf_report(user, project_id, "LogoAAA")
                time.sleep(2)

            elif aCompany.company.nameCompanies == "BBBB":
                update_progress(user, project_id, 20, f"{project.name}_submittal report")
                save_word_pdf_submittal_report(user, project_id, "LogoBBB", "ffffff")
                time.sleep(2)

                update_progress(user, project_id, 80, f"{project.name}_calculation report")
                save_word_pdf_calculation_report(user, project_id, "LogoBBB", "ffffff")
                time.sleep(2)

                update_progress(user, project_id, 90, f"{project.name}_final report")
                save_all_pdf_report(user, project_id, "LogoBBB")
                time.sleep(2)

            project.last_saved_time = now()
            project.save()

            update_progress(user, project_id, 100, f"{project.name}_done")

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
    except Exception as e:
        print("Handled task error:", e)
        try:
            update_progress(user, project_id, -1, f"{project.name}_error: {str(e)[:480]}")
        except Exception as update_error:
            print("Could not update progress due to DB failure:", update_error)
        return None
    