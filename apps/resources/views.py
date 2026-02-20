from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .models import Resource, ResourceType
from .serializers import ResourceSerializer, ResourceTypeSerializer

class ResourceTypeViewSet(viewsets.ModelViewSet):
    queryset = ResourceType.objects.all()
    serializer_class = ResourceTypeSerializer
    permission_classes = [IsAuthenticated]

class ResourceViewSet(viewsets.ModelViewSet):
    queryset = Resource.objects.all()
    serializer_class = ResourceSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        """
        Optional: Filter resources by type via URL query params
        Example: /api/resources/?type=Vaccine
        """
        queryset = Resource.objects.all()
        rt_name = self.request.query_params.get('type')
        if rt_name:
            queryset = queryset.filter(resource_type__name__iexact=rt_name)
        return queryset