from rest_framework import viewsets, views, status
from rest_framework.permissions import IsAuthenticated
from .models import User, Role, Permission, RolePermissionMapping
from rest_framework.response import Response
from .serializers.roles import RoleSerializer
from .serializers.users import UserSerializer
from .serializers.permissions import PermissionSerializer

class RoleViewSet(viewsets.ModelViewSet):
    queryset = Role.objects.all()
    serializer_class = RoleSerializer
    # Only Admins should manage roles
    permission_classes = [IsAuthenticated]


class PermissionViewSet(viewsets.ModelViewSet):
    queryset = Permission.objects.all()
    serializer_class = PermissionSerializer
    permission_classes = [IsAuthenticated] 

class AssignPermissionView(views.APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        role_id = request.data.get('role_id')
        permission_id = request.data.get('permission_id')
        
        mapping, created = RolePermissionMapping.objects.get_or_create(
            role_id=role_id, 
            permission_id=permission_id
        )
        return Response({"detail": "Permission assigned to role."}, status=status.HTTP_201_CREATED)

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all().select_related('role')
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]