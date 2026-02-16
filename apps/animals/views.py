from rest_framework import viewsets
from .models.animals import Animal
# from .serializers import AnimalSerializer
from .utils.permissions import HasRole

class AnimalViewSet(viewsets.ModelViewSet):
    queryset = Animal.objects.all()
    # serializer_class = AnimalSerializer
    
    def get_permissions(self):
        if self.action in ['destroy', 'update']:
            return [HasRole(['Admin'])]
        return [HasRole(['Admin', 'Farmer', 'Vet'])]