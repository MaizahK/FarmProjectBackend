from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.contrib.contenttypes.models import ContentType
from .models import Inventory
from .serializers import InventorySerializer
from ..logs.utils.helper import Logger

class InventoryViewSet(viewsets.ModelViewSet):
    queryset = Inventory.objects.all()
    serializer_class = InventorySerializer
    permission_classes = [IsAuthenticated]

    @action(detail=False, methods=['post'])
    def adjust_stock(self, request):
        """
        Payload example:
        {
            "model_name": "resource",  # or "product" or "animal"
            "object_id": 1,
            "category": "Vaccine",
            "item_name": "Booster",
            "quantity": 10,
            "unit": "Units",
            "action": "add" # or "remove"
        }
        """
        model_name = request.data.get('model_name').lower()
        obj_id = request.data.get('object_id')
        category = request.data.get('category')
        item_name = request.data.get('item_name')
        qty = float(request.data.get('quantity', 0))
        mode = request.data.get('action')
        unit = request.data.get('unit')

        try:
            # Dynamically get the ContentType for Resource, Product, or Animal
            content_type = ContentType.objects.get(model=model_name)
            
            # Get or create the inventory record for this specific object
            inventory_item, created = Inventory.objects.get_or_create(
                content_type=content_type,
                object_id=obj_id,
                defaults={
                    'category_name': category,
                    'item_name': item_name,
                    'unit': unit,
                    'quantity': 0
                }
            )

            if mode == 'add':
                inventory_item.quantity += qty
                verb = "Added to"
            else:
                if inventory_item.quantity < qty:
                    return Response({"error": "Insufficient stock"}, status=status.HTTP_400_BAD_REQUEST)
                inventory_item.quantity -= qty
                verb = "Removed from"

            # If item is fully consumed, we delete the inventory record
            if inventory_item.quantity <= 0:
                inventory_item.delete()
                Logger.write(request.user, "Stock Depleted", f"{item_name} removed from inventory", "Inventory")
                return Response({"detail": f"{item_name} is now out of stock."}, status=status.HTTP_204_NO_CONTENT)

            inventory_item.save()

            Logger.write(
                user=request.user,
                title="Stock Adjusted",
                description=f"{verb} {category}: {item_name}. New quantity: {inventory_item.quantity} {unit}",
                module="Inventory"
            )

            return Response(InventorySerializer(inventory_item).data)

        except ContentType.DoesNotExist:
            return Response({"error": "Invalid model type"}, status=status.HTTP_400_BAD_REQUEST)