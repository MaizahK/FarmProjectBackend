from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .serializers import AnimalSerializer, AnimalPurposeSerializer, AnimalHistorySerializer
from .models import Animal, AnimalPurpose, AnimalHistory
from ..logs.utils.helper import Logger
from ..inventory.utils import adjust_inventory_stock
from ..finances.utils import process_inventory_purchase


class AnimalViewSet(viewsets.ModelViewSet):
    queryset = Animal.objects.filter(is_deleted=False)
    permission_classes = [IsAuthenticated]
    serializer_class = AnimalSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        species = self.request.query_params.get("species")
        status = self.request.query_params.get("status")
        if species:
            queryset = queryset.filter(species__iexact=species)
        if status:
            queryset = queryset.filter(status__iexact=status)
        return queryset

    def perform_create(self, serializer):
        instance = serializer.save(owner=self.request.user)
        if self.request.data.get('add_to_inventory'):
            process_inventory_purchase(
                user=self.request.user,
                model_name='animal',
                object_id=instance.id,
                qty=1,
                amount=self.request.data.get('purchase_price', 0),
                category=instance.species,
                item_name=instance.tag_id,
                unit="Units"
            )

    def perform_update(self, serializer):
        instance = serializer.save()
        Logger.write(self.request.user, "Animal Updated", f"Updated: {instance.tag_id}", "Livestock")
        if getattr(serializer, '_add_to_inventory', False):
            self._adjust_inventory(instance, "add")

    def perform_destroy(self, instance):
        instance.is_deleted = True
        instance.is_active = False
        instance.save()
        Logger.write(self.request.user, "Animal Archived", f"Soft-deleted: {instance.tag_id}", "Livestock")

    def _adjust_inventory(self, instance, action):
        adjust_inventory_stock(
            user=self.request.user, model_name="animal", object_id=instance.id,
            category=instance.species, item_name=instance.tag_id,
            quantity=1, unit="Units", action=action
        )

class AnimalHistoryViewSet(viewsets.ModelViewSet):
    queryset = AnimalHistory.objects.all()
    serializer_class = AnimalHistorySerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        instance = serializer.save()
        Logger.write(self.request.user, "History Added", f"New {instance.record_type} for {instance.animal.tag_id}", "Livestock")

class AnimalPurposeViewSet(viewsets.ModelViewSet):
    queryset = AnimalPurpose.objects.all()
    serializer_class = AnimalPurposeSerializer
    permission_classes = [IsAuthenticated]