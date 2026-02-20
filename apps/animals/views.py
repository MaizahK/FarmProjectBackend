from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .models.animals import Animal
from .serializers import AnimalSerializer    
from .models.vaccination_records import VaccinationRecord
from .serializers import VaccinationRecordSerializer
from .utils.permissions import IsManagerUser # Using the RBAC class from earlier

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

    def get_permissions(self):
        """
        RBAC Logic: 
        - Anyone authenticated can view or create records.
        - Only Managers/Admins can delete records.
        """
        if self.action == 'destroy':
            return [IsManagerUser()]
        return [super().get_permissions()[0]]

    def create(self, request, *args, **kwargs):
        # Optional: Add logic here to deduct the 'vaccine_resource' 
        # quantity from your Resource inventory when a vaccine is used.
        return super().create(request, *args, **kwargs)