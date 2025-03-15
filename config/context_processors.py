from Apps.aApp1.models import RoleAutho
from Apps.aAppMechanical.models import UserCompany  # Import your UserCompany model

def user_permissions(request):
    permissions = {}
    if request.user.is_authenticated:
        for autho_name in ["MS", "BC", "GR", "PS", "TH", "MX", "RT", "AthRol", "Hist", "Settings", "Users"]:
            permissions[autho_name] = RoleAutho.objects.filter(
                role__userrole__user=request.user, autho__name=autho_name
            ).exists()

    # Get the company of the logged-in user
    user_company = None
    if request.user.is_authenticated:
        try:
            user_company = UserCompany.objects.select_related('company').get(user=request.user)
        except UserCompany.DoesNotExist:
            user_company = None

    return {
        'permissions': permissions,
        'user_company': user_company  # Add company to context
    }
