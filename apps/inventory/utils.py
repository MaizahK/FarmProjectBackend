from .models import Inventory
from ..logs.utils.helper import Logger

def adjust_inventory_stock(user, model_name, category, item_name, quantity, unit, action="add"):
    """
    Collective Inventory Logic:
    Finds an item by category and name. If it exists, update quantity.
    Otherwise, create a new record.
    """
    from django.contrib.contenttypes.models import ContentType
    
    model_name = (model_name or "").lower()
    try:
        content_type = ContentType.objects.get(model=model_name)
    except ContentType.DoesNotExist:
        return None

    # Find the collective record (e.g., all Angus Cows)
    inventory_item, created = Inventory.objects.get_or_create(
        content_type=content_type,
        category_name=category,
        item_name=item_name,
        defaults={
            "unit": unit,
            "quantity": 0,
        },
    )

    if action == "add":
        inventory_item.quantity += quantity
        verb = "Added to"
    else:
        if inventory_item.quantity < quantity:
            return False 
        inventory_item.quantity -= quantity
        verb = "Removed from"

    # Save logic
    if inventory_item.quantity <= 0:
        inventory_item.delete()
        Logger.write(user, "Stock Depleted", f"{item_name} removed from inventory", "Inventory")
    else:
        inventory_item.save()
        Logger.write(
            user=user,
            title="Stock Adjusted",
            description=f"{verb} {category}: {item_name}. New balance: {inventory_item.quantity} {unit}",
            module="Inventory",
        )
    
    return True