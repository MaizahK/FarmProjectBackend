from ..logs.utils.helper import Logger
from rest_framework.decorators import action
from rest_framework import viewsets, views, status
from rest_framework.permissions import IsAuthenticated
from .models import User, Role, Permission, RolePermissionMapping
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from .serializers import *

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

class AssignPermissionViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]
    queryset = RolePermissionMapping.objects.all()

    @action(detail=False, methods=["post"])
    def assign(self, request):
        role_id = request.data.get("role_id")
        permission_id = request.data.get("permission_id")

        mapping, created = RolePermissionMapping.objects.get_or_create(
            role_id=role_id,
            permission_id=permission_id
        )

        Logger.write(
            user=request.user,
            title="Permission Assigned",
            description=f"Assigned permission ID {permission_id} to role ID {role_id}",
            module="Users"
        )

        return Response(
            {"detail": "Permission assigned to role."},
            status=status.HTTP_201_CREATED
        )
    
    @action(detail=False, methods=["post"])
    def remove(self, request):
        role_id = request.data.get("role_id")
        permission_id = request.data.get("permission_id")
        
        deleted, _ = RolePermissionMapping.objects.filter(
            role_id=role_id, 
            permission_id=permission_id
        ).delete()

        if deleted:
            Logger.write(
                user=request.user,
                title="Permission Removed",
                description=f"Removed permission {permission_id} from role {role_id}",
                module="Users"
            )
            return Response({"detail": "Permission removed."}, status=status.HTTP_200_OK)
        return Response({"detail": "Mapping not found."}, status=status.HTTP_404_NOT_FOUND)

    @action(detail=False, methods=["post"])
    def assign_many(self, request):
        role_id = request.data.get("role_id")
        assign_all = request.data.get("assign_all", False)
        permission_ids = request.data.get("permission_ids", [])

        role = get_object_or_404(Role, id=role_id)
        
        if assign_all:
            # You can now use the manager directly!
            perms = Permission.objects.all()
            role.permissions.add(*perms) 
        else:
            perms = Permission.objects.filter(id__in=permission_ids)
            role.permissions.add(*perms)

        return Response({"detail": "Permissions assigned."}, status=status.HTTP_201_CREATED)

    @action(detail=False, methods=["post"])
    def remove_many(self, request):
        role_id = request.data.get("role_id")
        remove_all = request.data.get("remove_all", False)
        permission_ids = request.data.get("permission_ids", [])

        role = get_object_or_404(Role, id=role_id)
        
        if remove_all:
            role.permissions.clear() # Removes all mappings for this role
        else:
            role.permissions.remove(*permission_ids)

        return Response({"detail": "Permissions removed."}, status=status.HTTP_200_OK)
    
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