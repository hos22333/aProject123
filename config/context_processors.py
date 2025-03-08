from aApp1.models import RoleAutho

def user_permissions(request):
    permissions = {}
    if request.user.is_authenticated:
        for autho_name in ["MS", "BC", "GR", "PS", "TH", "MX", "RT", "AthRol", "Hist", "Settings", "Users"]:
            permissions[autho_name] = RoleAutho.objects.filter(
                role__userrole__user=request.user, autho__name=autho_name
            ).exists()

    return {'permissions': permissions}
