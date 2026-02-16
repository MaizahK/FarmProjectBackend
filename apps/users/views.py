from rest_framework import viewsets
from .models import User, Role
from .serializers.roles import RoleSerializer
from .serializers.users import UserSerializer
from .utils.permissions import HasRole

class RoleViewSet(viewsets.ModelViewSet):
    queryset = Role.objects.all()
    serializer_class = RoleSerializer
    # Only Admins should manage roles
    permission_classes = [HasRole(['Admin'])]

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all().select_related('role')
    serializer_class = UserSerializer
    
    def get_permissions(self):
        # Allow anyone logged in to see users, but only Admin to create/delete
        if self.action in ['create', 'destroy']:
            return [HasRole(['Admin'])]
        return [HasRole(['Admin', 'Farmer', 'Vet'])]