from rest_framework import serializers
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Inventory, InventoryTransaction
from .serializers import InventorySerializer, InventoryTransactionSerializer
from .utils import adjust_inventory_stock

class InventoryViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Inventory.objects.all()
    serializer_class = InventorySerializer
    permission_classes = [IsAuthenticated]

class InventoryTransactionViewSet(viewsets.ModelViewSet):
    queryset = InventoryTransaction.objects.all()
    serializer_class = InventoryTransactionSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        # 1. Save the transaction record
        transaction = serializer.save()
        
        # 2. Determine if we are adding or removing based on type
        # Production, Purchase, Adjustment (pos), Transfer (in) = ADD
        # Consumption, Sale, Adjustment (neg), Transfer (out) = REMOVE
        
        add_types = ['PRODUCTION', 'PURCHASE']
        remove_types = ['CONSUMPTION', 'SALE']
        
        # Defaulting logic for this example
        action = "add" if transaction.transaction_type in add_types else "remove"
        
        # 3. Call utility to update the actual Inventory balance
        success = adjust_inventory_stock(
            user=self.request.user,
            model_name=transaction.content_type.model,
            object_id=transaction.object_id,
            category="General", # You can pass more specific logic here
            item_name=f"Item-{transaction.object_id}",
            quantity=transaction.quantity,
            unit="Units",
            action=action
        )

        if not success:
            # Note: In a production app, you'd use a database transaction.atomic() 
            # to roll back the Transaction record if stock adjustment fails.
            transaction.delete()
            raise serializers.ValidationError({"error": "Insufficient stock for this transaction."})