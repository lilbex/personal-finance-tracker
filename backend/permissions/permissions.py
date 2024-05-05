from rest_framework import permissions
from rest_framework import permissions, status

# Still not sure what to do
class IsOwner(permissions.BasePermission):
    def has_permission(self, request, view):
        if not request.user:
            return False
