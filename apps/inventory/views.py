from rest_framework import serializers
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Inventory, InventoryTransaction
from .serializers import InventorySerializer, InventoryTransactionSerializer
from .utils import adjust_inventory_stock
from ..logs.utils.helper import Logger
from django.db import transaction as db_transaction

class InventoryViewSet(viewsets.ModelViewSet):
    queryset = Inventory.objects.all()
    serializer_class = InventorySerializer
    permission_classes = [IsAuthenticated]

    def perform_update(self, serializer):
        with db_transaction.atomic():
            old_quantity = self.get_object().quantity
            item = serializer.save()

            # Record manual stock corrections in the movement log so history stays complete
            if item.quantity != old_quantity:
                InventoryTransaction.objects.create(
                    content_type=item.content_type,
                    object_id=item.object_id,
                    transaction_type='ADJUSTMENT',
                    quantity=item.quantity - old_quantity,
                    unit=item.unit,
                    description=f"Manual adjustment {old_quantity} → {item.quantity} of {item.item_name}",
                )
            Logger.write(self.request.user, "Inventory Edited", f"Edited {item.item_name}", "Inventory")

    def perform_destroy(self, instance):
        Logger.write(self.request.user, "Stock Removed", f"Deleted {instance.item_name} from inventory", "Inventory")
        instance.delete()

    @action(detail=True, methods=['get'])
    def history(self, request, pk=None):
        item = self.get_object()
        transactions = InventoryTransaction.objects.filter(content_type=item.content_type)
        if item.content_type.model == 'animal':
            transactions = transactions.filter(object_id=item.object_id)
        else:
            # Collective rows (object_id 0) aren't linked to transactions by id;
            # every movement description ends with the item name ("Bought X", "Sold X", ...)
            if not item.item_name:
                transactions = transactions.none()
            else:
                transactions = transactions.filter(description__iendswith=item.item_name)
        serializer = InventoryTransactionSerializer(transactions.order_by('-created_at')[:100], many=True)
        return Response(serializer.data)

class InventoryTransactionViewSet(viewsets.ModelViewSet):
    queryset = InventoryTransaction.objects.all()
    serializer_class = InventoryTransactionSerializer
    permission_classes = [IsAuthenticated]

    queryset = InventoryTransaction.objects.all()
    serializer_class = InventoryTransactionSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        with db_transaction.atomic():
            # 1. This now works because the extra fields were popped in the serializer
            inv_trans = serializer.save()
            if not inv_trans.description:
                # Keeps the item name in the log so InventoryViewSet.history can find it
                inv_trans.description = f"{inv_trans.get_transaction_type_display()} of {getattr(serializer, '_item_name', 'Unknown')}"
                inv_trans.save(update_fields=['description'])

            # 2. Logic to determine Add/Remove
            add_types = ['PRODUCTION', 'PURCHASE']
            action = "add" if inv_trans.transaction_type in add_types else "remove"
            
            # 3. Access the popped values stored on the serializer instance
            success = adjust_inventory_stock(
                user=self.request.user,
                model_name=inv_trans.content_type.model,
                object_id=inv_trans.object_id,
                category=getattr(serializer, '_category_name', 'General'),
                item_name=getattr(serializer, '_item_name', 'Unknown'),
                quantity=inv_trans.quantity,
                unit=inv_trans.unit,
                action=action
            )

            if not success:
                raise serializers.ValidationError({
                    "error": "Insufficient stock to complete this transaction."
                })