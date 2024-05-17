from rest_framework.permissions import BasePermission
from apps.core.models import UserRole


class IsBetaPlayer(BasePermission):
    def has_permission(self, request, view):
        return bool(UserRole.objects.filter(user=request.user, role__name='beta players').count())
