from ..logs.utils.helper import Logger
from ..finances.utils import process_inventory_purchase
from ..inventory.utils import adjust_inventory_stock
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
    queryset = Resource.objects.filter(is_deleted=False)
    serializer_class = ResourceSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        # 1. Save the Resource instance
        instance = serializer.save()
        
        # Extract transient data from serializer
        amount = getattr(serializer, '_amount', 0)
        add_to_inv = getattr(serializer, '_add_to_inventory', False)

        # 2. Standard Activity Log
        Logger.write(
            user=self.request.user,
            title="Resource Created",
            description=f"Added resource: {instance.name}",
            module="Resources"
        )

        # 3. Trigger the Unified Purchase Flow
        # This handles: Expense, Financial Transaction, Inventory Log, and Stock Adjustment
        if add_to_inv:
            process_inventory_purchase(
                user=self.request.user,
                model_name="resource",
                object_id=instance.id,
                qty=instance.quantity,
                amount=amount,
                category=instance.resource_type.name,
                item_name=instance.name,
                unit=instance.unit
            )

    def perform_update(self, serializer):
        instance = serializer.save()
        Logger.write(
            user=self.request.user,
            title="Resource Updated",
            description=f"Updated details for {instance.name}",
            module="Resources"
        )

    def perform_destroy(self, instance):
        # Soft Delete Logic
        instance.is_deleted = True
        instance.save()

        # Check if we should also remove this from active inventory stock
        # Triggered via query param: DELETE /api/resources/1/?remove_from_inventory=true
        remove_inv = self.request.query_params.get("remove_from_inventory")
        if str(remove_inv).lower() in ("1", "true", "yes"):
            adjust_inventory_stock(
                user=self.request.user,
                model_name="resource",
                object_id=instance.id,
                category=instance.resource_type.name,
                item_name=instance.name,
                quantity=instance.quantity,
                unit=instance.unit,
                action="remove"
            )

        Logger.write(
            user=self.request.user,
            title="Resource Deleted",
            description=f"Soft deleted resource: {instance.name}",
            module="Resources"
        )