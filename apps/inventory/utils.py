from django.contrib.contenttypes.models import ContentType
from rest_framework import status
from rest_framework.response import Response
from .models import Inventory
from ..logs.utils.helper import Logger

def adjust_inventory_stock(user, model_name, object_id, category, item_name, quantity, unit, action="add"):
    """
    Core logic to update the running balance in the Inventory table.
    """
    model_name = (model_name or "").lower()
    try:
        content_type = ContentType.objects.get(model=model_name)
    except ContentType.DoesNotExist:
        return None # Handle error in view

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
    else:
        # Prevent negative inventory
        if inventory_item.quantity < quantity:
            return False 
        inventory_item.quantity -= quantity

    if inventory_item.quantity <= 0:
        inventory_item.delete()
    else:
        inventory_item.save()
    
    return True