from rest_framework import viewsets
from .models.resources import Resource
# from serializers import ResourceSerializer, ResourceTypeSerializer
from ..utils.permissions import HasRole

class ResourceViewSet(viewsets.ModelViewSet):
    queryset = Resource.objects.all()
    # serializer_class = ResourceSerializer
    permission_classes = [HasRole(['Admin', 'Farmer'])]