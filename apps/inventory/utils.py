from django.contrib.contenttypes.models import ContentType
from rest_framework import status
from rest_framework.response import Response

from .models import Inventory
from .serializers import InventorySerializer
from ..logs.utils.helper import Logger


def adjust_inventory_stock(user, model_name, object_id, category, item_name, quantity, unit, action="add"):
    """Adjust the inventory stock for a specific object.

    This encapsulates the shared logic used by the Inventory API and other app-level
    endpoints that want to update inventory without re-implementing the business rules.

    Args:
        user: The user performing the change (for logging purposes).
        model_name: The lowercase model name (e.g., "resource", "product", "animal").
        object_id: The id of the object to associate with the inventory record.
        category: The category name (e.g., "Vaccine", "Feed", "Cow").
        item_name: The item name (e.g., "Booster").
        quantity: The amount to add/remove.
        unit: The unit string (e.g. "Units").
        action: "add" or "remove".

    Returns:
        rest_framework.response.Response - mimics the InventoryViewSet.adjust_stock response.
    """

    model_name = (model_name or "").lower()
    try:
        content_type = ContentType.objects.get(model=model_name)
    except ContentType.DoesNotExist:
        return Response({"error": "Invalid model type"}, status=status.HTTP_400_BAD_REQUEST)

    inventory_item, created = Inventory.objects.get_or_create(
        content_type=content_type,
        object_id=object_id,
        defaults={
            "category_name": category,
            "item_name": item_name,
            "unit": unit,
            "quantity": 0,
        },
    )

    if action == "add":
        inventory_item.quantity += quantity
        verb = "Added to"
    else:
        if inventory_item.quantity < quantity:
            return Response({"error": "Insufficient stock"}, status=status.HTTP_400_BAD_REQUEST)
        inventory_item.quantity -= quantity
        verb = "Removed from"

    # If item is fully consumed, we delete the inventory record
    if inventory_item.quantity <= 0:
        inventory_item.delete()
        Logger.write(user, "Stock Depleted", f"{item_name} removed from inventory", "Inventory")
        return Response({"detail": f"{item_name} is now out of stock."}, status=status.HTTP_204_NO_CONTENT)

    inventory_item.save()

    Logger.write(
        user=user,
        title="Stock Adjusted",
        description=f"{verb} {category}: {item_name}. New quantity: {inventory_item.quantity} {unit}",
        module="Inventory",
    )

    return Response(InventorySerializer(inventory_item).data)
