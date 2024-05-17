from django.contrib import admin

from .models import User, Plan, Role, UserRole

admin.site.register(User)
admin.site.register(Plan)
admin.site.register(Role)
admin.site.register(UserRole)
