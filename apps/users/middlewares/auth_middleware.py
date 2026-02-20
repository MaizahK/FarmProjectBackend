import re
from django.http import JsonResponse
from ..models import RolePermissionMapping

class DynamicRBACMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # 1. Skip check for admin site or auth endpoints
        exempt_urls = [r'^/admin/', r'^/api/token/']
        if any(re.match(url, request.path) for url in exempt_urls):
            return self.get_response(request)

        # 2. Ensure user is authenticated (JWT handles request.user)
        if not request.user.is_authenticated:
            return JsonResponse({'detail': 'Authentication required'}, status=401)

        # 3. Superusers bypass all checks
        if request.user.is_superuser or request.user.role == 'Admin':
            print(f'Role {user_role} has permission for {current_method} {current_path}')
            return self.get_response(request)

        # 4. Check Database for Role-Path-Method match
        current_path = request.path
        current_method = request.method
        user_role = request.user.role # Assuming user.role returns the string name

        has_permission = RolePermissionMapping.objects.filter(
            role__name=user_role,
            permission__path__iexact=current_path,
            permission__method__iexact=current_method
        ).exists()

        if not has_permission:
            return JsonResponse({
                'detail': f'Role {user_role} does not have permission for {current_method} {current_path}'
            }, status=403)

        print(f'Role {user_role} has permission for {current_method} {current_path}')
        return self.get_response(request)