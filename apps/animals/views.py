from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .serializers import *    
from .models import *

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

class AnimalPurposeViewSet(viewsets.ModelViewSet):
    queryset = AnimalPurpose.objects.all()
    serializer_class = AnimalPurposeSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        queryset = AnimalPurpose.objects.all()
        species = self.request.query_params.get("species")

        if species:
            queryset = queryset.filter(species__iexact=species)

        return queryset