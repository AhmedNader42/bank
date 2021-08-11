from rest_framework import permissions
from .models import User


class IsBankerOrAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        print(request.method)
        return request.user.is_superuser or (request.user.user_type == User.BANKER)
