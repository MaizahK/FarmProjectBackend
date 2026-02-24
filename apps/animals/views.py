from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .serializers import *
from .models import *
from ..logs.utils.helper import Logger

class AnimalViewSet(viewsets.ModelViewSet):
    queryset = Animal.objects.all()
    permission_classes = [IsAuthenticated]
    serializer_class = AnimalSerializer

    def get_queryset(self):
        queryset = Animal.objects.all()
        species = self.request.query_params.get("species")

        if species:
            queryset = queryset.filter(species__iexact=species)

        return queryset

    def perform_create(self, serializer):
        # Automatically set the owner to the user making the request (from JWT)
        instance = serializer.save(owner=self.request.user)
        Logger.write(
            user=self.request.user,
            title="Animal Registered",
            description=f"Registered new animal: {instance.tag_id} ({instance.species})",
            module="Livestock"
        )

    def perform_update(self, serializer):
        instance = serializer.save()
        Logger.write(
            user=self.request.user,
            title="Animal Updated",
            description=f"Updated details for animal: {instance.tag_id}",
            module="Livestock"
        )

    def perform_destroy(self, instance):
        tag_id = instance.tag_id
        instance.delete()
        Logger.write(
            user=self.request.user,
            title="Animal Deleted",
            description=f"Removed animal record: {tag_id}",
            module="Livestock"
        )

class VaccinationRecordViewSet(viewsets.ModelViewSet):
    queryset = VaccinationRecord.objects.all()
    serializer_class = VaccinationRecordSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        instance = serializer.save()
        Logger.write(
            user=self.request.user,
            title="Vaccination Added",
            description=f"Administered {instance.vaccine_resource.name} to {instance.animal.tag_id}",
            module="Livestock"
        )

    def perform_update(self, serializer):
        instance = serializer.save()
        Logger.write(
            user=self.request.user,
            title="Vaccination Updated",
            description=f"Updated vaccination record for {instance.animal.tag_id}",
            module="Livestock"
        )

    def perform_destroy(self, instance):
        info = f"{instance.vaccine_resource.name} for {instance.animal.tag_id}"
        instance.delete()
        Logger.write(
            user=self.request.user,
            title="Vaccination Deleted",
            description=f"Deleted record: {info}",
            module="Livestock"
        )
    
class HealthRecordViewSet(viewsets.ModelViewSet):
    queryset = HealthRecord.objects.all()
    serializer_class = HealthRecordSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        instance = serializer.save()
        Logger.write(
            user=self.request.user,
            title="Health Checkup Added",
            description=f"Recorded checkup for {instance.animal.tag_id}",
            module="Livestock"
        )

    def perform_update(self, serializer):
        instance = serializer.save()
        Logger.write(
            user=self.request.user,
            title="Health Checkup Updated",
            description=f"Updated health record for {instance.animal.tag_id}",
            module="Livestock"
        )

    def perform_destroy(self, instance):
        animal_tag = instance.animal.tag_id
        instance.delete()
        Logger.write(
            user=self.request.user,
            title="Health Checkup Deleted",
            description=f"Deleted health record for {animal_tag}",
            module="Livestock"
        )

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

    def perform_create(self, serializer):
        instance = serializer.save()
        Logger.write(
            user=self.request.user,
            title="Animal Purpose Created",
            description=f"Created purpose: {instance.name} for {instance.species}",
            module="Livestock"
        )

    def perform_update(self, serializer):
        instance = serializer.save()
        Logger.write(
            user=self.request.user,
            title="Animal Purpose Updated",
            description=f"Updated purpose: {instance.name}",
            module="Livestock"
        )

    def perform_destroy(self, instance):
        name = instance.name
        instance.delete()
        Logger.write(
            user=self.request.user,
            title="Animal Purpose Deleted",
            description=f"Deleted purpose: {name}",
            module="Livestock"
        )