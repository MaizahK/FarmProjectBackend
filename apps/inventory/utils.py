from .models import Inventory
from ..logs.utils.helper import Logger
from django.contrib.contenttypes.models import ContentType

def adjust_inventory_stock(user, model_name, object_id, category, item_name, quantity, unit, action="add"):
    try:
        model_name = (model_name or "").lower()
        try:
            content_type = ContentType.objects.get(model=model_name)
        except ContentType.DoesNotExist:
            return False

        # Logic: Animals use their real ID. Resources/Products use ID 0 to stay collective.
        target_id = object_id if model_name == 'animal' else 0

        search_criteria = {
            "content_type": content_type,
            "category_name": category,
            "item_name": item_name,
            "object_id": target_id, # Always include this in the filter
        }

        # Get or Create the record
        inventory_item, created = Inventory.objects.get_or_create(
            **search_criteria,
            defaults={
                "unit": unit,
                "quantity": 0,
            },
        )

        if action == "add":
            inventory_item.quantity += quantity
            verb = "Added"
        else:
            if inventory_item.quantity < quantity:
                return False 
            inventory_item.quantity -= quantity
            verb = "Removed"

        if inventory_item.quantity <= 0:
            inventory_item.delete()
            Logger.write(user, "Stock Removed", f"{item_name} cleared", "Inventory")
        else:
            inventory_item.save()
            Logger.write(
                user=user,
                title="Inventory Updated",
                description=f"{verb} {quantity} {unit} of {item_name}",
                module="Inventory"
            )
        
        return True
    except Exception as e:
        print(f"Inventory Error: {e}")
        return False