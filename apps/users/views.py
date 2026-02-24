from ..logs.utils.helper import Logger
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

    def perform_create(self, serializer):
        instance = serializer.save()
        Logger.write(
            user=self.request.user,
            title="Role Created",
            description=f"Created new role: {instance.name}",
            module="Users"
        )

    def perform_update(self, serializer):
        instance = serializer.save()
        Logger.write(
            user=self.request.user,
            title="Role Updated",
            description=f"Updated role: {instance.name}",
            module="Users"
        )

    def perform_destroy(self, instance):
        role_name = instance.name
        instance.delete()
        Logger.write(
            user=self.request.user,
            title="Role Deleted",
            description=f"Deleted role: {role_name}",
            module="Users"
        )


class PermissionViewSet(viewsets.ModelViewSet):
    queryset = Permission.objects.all()
    serializer_class = PermissionSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        instance = serializer.save()
        Logger.write(
            user=self.request.user,
            title="Permission Created",
            description=f"Created permission: {instance.name}",
            module="Users"
        )

    def perform_update(self, serializer):
        instance = serializer.save()
        Logger.write(
            user=self.request.user,
            title="Permission Updated",
            description=f"Updated permission: {instance.name}",
            module="Users"
        )

    def perform_destroy(self, instance):
        perm_name = instance.name
        instance.delete()
        Logger.write(
            user=self.request.user,
            title="Permission Deleted",
            description=f"Deleted permission: {perm_name}",
            module="Users"
        )

class AssignPermissionView(views.APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        role_id = request.data.get('role_id')
        permission_id = request.data.get('permission_id')
        
        mapping, created = RolePermissionMapping.objects.get_or_create(
            role_id=role_id, 
            permission_id=permission_id
        )

        Logger.write(
            user=self.request.user,
            title="Permission Assigned",
            description=f"Assigned permission ID {permission_id} to role ID {role_id}",
            module="Users"
        )

        return Response({"detail": "Permission assigned to role."}, status=status.HTTP_201_CREATED)

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all().select_related('role')
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        instance = serializer.save()
        Logger.write(
            user=self.request.user,
            title="User Registered",
            description=f"Created user account: {instance.username}",
            module="Users"
        )

    def perform_update(self, serializer):
        instance = serializer.save()
        Logger.write(
            user=self.request.user,
            title="User Updated",
            description=f"Updated user profile: {instance.username}",
            module="Users"
        )

    def perform_destroy(self, instance):
        username = instance.username
        instance.delete()
        Logger.write(
            user=self.request.user,
            title="User Deleted",
            description=f"Removed user account: {username}",
            module="Users"
        )