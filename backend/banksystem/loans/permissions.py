from rest_framework import permissions
from users.models import User
from rest_framework.permissions import SAFE_METHODS



class IsBankerOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True
        return request.user.user_type == User.BANKER
