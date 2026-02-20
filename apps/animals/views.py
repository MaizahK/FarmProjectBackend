from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .models.animals import Animal
from .serializers import AnimalSerializer    
from .models.vaccination_records import VaccinationRecord
from .serializers import VaccinationRecordSerializer

class AnimalViewSet(viewsets.ModelViewSet):
    queryset = Animal.objects.all()
    permission_classes = [IsAuthenticated]
    serializer_class = AnimalSerializer

    def perform_create(self, serializer):
        # Automatically set the owner to the user making the request (from JWT)
        serializer.save(owner=self.request.user)

class VaccinationRecordViewSet(viewsets.ModelViewSet):
    queryset = VaccinationRecord.objects.all()
    serializer_class = VaccinationRecordSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        # Optional: Add logic here to deduct the 'vaccine_resource' 
        # quantity from your Resource inventory when a vaccine is used.
        return super().create(request, *args, **kwargs)