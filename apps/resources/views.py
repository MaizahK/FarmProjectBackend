from ..logs.utils.helper import Logger
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .models import Resource, ResourceType
from .serializers import ResourceSerializer, ResourceTypeSerializer

class ResourceTypeViewSet(viewsets.ModelViewSet):
    queryset = ResourceType.objects.all()
    serializer_class = ResourceTypeSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        instance = serializer.save()
        Logger.write(
            user=self.request.user,
            title="Resource Type Created",
            description=f"Created resource category: {instance.name}",
            module="Resources"
        )

    def perform_update(self, serializer):
        instance = serializer.save()
        Logger.write(
            user=self.request.user,
            title="Resource Type Updated",
            description=f"Updated resource category: {instance.name}",
            module="Resources"
        )

    def perform_destroy(self, instance):
        name = instance.name
        instance.delete()
        Logger.write(
            user=self.request.user,
            title="Resource Type Deleted",
            description=f"Deleted resource category: {name}",
            module="Resources"
        )

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

    def perform_create(self, serializer):
        instance = serializer.save()
        Logger.write(
            user=self.request.user,
            title="Resource Created",
            description=f"Added resource: {instance.name} ({instance.resource_type.name})",
            module="Resources"
        )

    def perform_update(self, serializer):
        instance = serializer.save()
        Logger.write(
            user=self.request.user,
            title="Resource Updated",
            description=f"Updated resource: {instance.name}",
            module="Resources"
        )

    def perform_destroy(self, instance):
        name = instance.name
        instance.delete()
        Logger.write(
            user=self.request.user,
            title="Resource Deleted",
            description=f"Removed resource: {name}",
            module="Resources"
        )