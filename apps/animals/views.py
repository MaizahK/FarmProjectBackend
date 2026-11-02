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
        
        Logger.write(
            user=self.request.user,
            title="Animal Created",
            description=f"Added animal: {instance.tag_id}",
            module="Animals"
        )
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
        # Only touch stock when the client explicitly sends the flag; the serializer
        # defaults it to False, which used to remove the animal from inventory on every edit.
        flag = self.request.data.get('add_to_inventory')
        if flag is not None:
            if str(flag).lower() in ('true', '1'):
                self._adjust_inventory(instance, "add")
            else:
                self._adjust_inventory(instance, "remove")

    def perform_destroy(self, instance):
        instance.is_deleted = True
        instance.is_active = False
        instance.save()
        self._adjust_inventory(instance, "remove")
        Logger.write(self.request.user, "Animal Archived", f"Soft-deleted: {instance.tag_id}", "Livestock")

    def _adjust_inventory(self, instance, action):
        adjust_inventory_stock(
            user=self.request.user, model_name="animal", object_id=instance.id,
            category=instance.species, item_name=instance.tag_id,
            quantity=1, unit="Units", action=action
        )
        Logger.write(self.request.user, f"Inventory Updated ({action} animal)", f"Inventory updated: {instance.tag_id}", "Livestock")


class AnimalHistoryViewSet(viewsets.ModelViewSet):
    queryset = AnimalHistory.objects.all()
    serializer_class = AnimalHistorySerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        queryset = super().get_queryset()
        animal = self.request.query_params.get("animal")
        if animal:
            queryset = queryset.filter(animal_id=animal)
        return queryset

    def perform_create(self, serializer):
        event_date = serializer.validated_data.get('event_date')
        instance = serializer.save()
        # auto_now_add overwrites event_date on insert, so apply the chosen date afterwards
        if event_date and instance.event_date != event_date:
            AnimalHistory.objects.filter(pk=instance.pk).update(event_date=event_date)
            instance.event_date = event_date
        Logger.write(self.request.user, "History Added", f"New {instance.record_type} for {instance.animal.tag_id}", "Livestock")

    def perform_update(self, serializer):
        instance = serializer.save()
        Logger.write(self.request.user, "History Updated", f"Updated {instance.record_type} for {instance.animal.tag_id}", "Livestock")

    def perform_destroy(self, instance):
        Logger.write(self.request.user, "History Deleted", f"Removed {instance.record_type} for {instance.animal.tag_id}", "Livestock")
        instance.delete()

class AnimalPurposeViewSet(viewsets.ModelViewSet):
    queryset = AnimalPurpose.objects.all()
    serializer_class = AnimalPurposeSerializer
    permission_classes = [IsAuthenticated]