from rest_framework import permissions

class IsAdminUser(permissions.BasePermission):
    """Allows access only to users in the 'Admin' group."""
    def has_permission(self, request, view):
        return request.user.groups.filter(name='Admin').exists()
    
class IsManagerUser(permissions.BasePermission):
    """Allows access to Managers and Admins."""
    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False
        return request.user.groups.filter(name__in=['Admin', 'Manager']).exists()

class IsReadOnly(permissions.BasePermission):
    """Allows safe methods for everyone, but write access only to Managers."""
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user.groups.filter(name='User').exists()