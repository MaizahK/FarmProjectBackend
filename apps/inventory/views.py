from rest_framework import serializers
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Inventory, InventoryTransaction
from .serializers import InventorySerializer, InventoryTransactionSerializer
from .utils import adjust_inventory_stock
from django.db import transaction as db_transaction

class InventoryViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Inventory.objects.all()
    serializer_class = InventorySerializer
    permission_classes = [IsAuthenticated]

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
                unit=getattr(serializer, '_unit', 'Units'),
                action=action
            )

            if not success:
                raise serializers.ValidationError({
                    "error": "Insufficient stock to complete this transaction."
                })