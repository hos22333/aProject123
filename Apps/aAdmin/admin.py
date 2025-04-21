from django.contrib import admin
from .models import Role, Autho, UserRole, RoleAutho

admin.site.register(Role)
admin.site.register(Autho)
admin.site.register(UserRole)
admin.site.register(RoleAutho)
