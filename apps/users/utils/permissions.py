from rest_framework import permissions

class HasRole(permissions.BasePermission):
    def __init__(self, allowed_roles):
        self.allowed_roles = allowed_roles

    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role.name in self.allowed_roles