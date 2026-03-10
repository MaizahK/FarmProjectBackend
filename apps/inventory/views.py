from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated

from .models import Inventory
from .serializers import InventorySerializer
from .utils import adjust_inventory_stock
from ..logs.utils.helper import Logger


class InventoryViewSet(viewsets.ModelViewSet):
    queryset = Inventory.objects.all()
    serializer_class = InventorySerializer
    permission_classes = [IsAuthenticated]

    @action(detail=False, methods=["post"])
    def adjust_stock(self, request):
        """Adjust inventory for a given object.

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
        model_name = request.data.get('model_name')
        obj_id = request.data.get('object_id')
        category = request.data.get('category')
        item_name = request.data.get('item_name')
        qty = float(request.data.get('quantity', 0))
        mode = request.data.get('action')
        unit = request.data.get('unit')

        return adjust_inventory_stock(
            user=request.user,
            model_name=model_name,
            object_id=obj_id,
            category=category,
            item_name=item_name,
            quantity=qty,
            unit=unit,
            action=mode,
        )
