from rest_framework import viewsets
from models.resource_types import ResourceType
from ..utils.permissions import HasRole

class ResourceTypeViewSet(viewsets.ModelViewSet):
    queryset = ResourceType.objects.all()
    # serializer_class = ResourceTypeSerializer
    permission_classes = [HasRole(['Admin'])]
