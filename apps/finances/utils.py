from django.db import transaction
from django.contrib.contenttypes.models import ContentType
from .models import FinancialTransaction, Expense, Sale
from ..inventory.models import InventoryTransaction
from ..inventory.utils import adjust_inventory_stock
from ..logs.utils.helper import Logger
from ..animals.models import Animal # Assuming this path

@transaction.atomic
def process_inventory_purchase(user, model_name, object_id, qty, amount, category, item_name, unit="Units"):
    try:
        model_name = model_name.lower()
        ctype = ContentType.objects.get(model=model_name)
        
        # 1. Expense Record
        expense = Expense.objects.create(
            content_type=ctype,
            object_id=object_id,
            category_name=category,
            amount=amount,
            is_paid=True,
            description=f"Purchase of {item_name}"
        )

        # 2. Financial Ledger
        FinancialTransaction.objects.create(
            type='EXPENSE',
            amount=amount,
            category=category,
            reference_type=ContentType.objects.get_for_model(expense),
            reference_id=expense.id
        )

        # 3. Movement Log (Always individual for history)
        InventoryTransaction.objects.create(
            content_type=ctype,
            object_id=object_id,
            transaction_type='PURCHASE',
            quantity=qty,
            description=f"Buying {item_name}",
            reference_type=ContentType.objects.get_for_model(expense),
            reference_id=expense.id
        )

        # 4. Inventory Balance (Hybrid Logic)
        adjust_inventory_stock(
            user=user,
            model_name=model_name,
            object_id=object_id, # Passed to util which decides whether to use it or 0
            category=category,
            item_name=item_name,
            quantity=qty,
            unit=unit,
            action="add"
        )
        
        return True
    except Exception as e:
        print(f"Purchase Flow Error: {e}")
        return False

@transaction.atomic
def process_inventory_production(user, model_name, object_id, qty, category, item_name, unit="Units"):
    """
    Handles internal production/harvesting (e.g., Milk collection).
    Records an Inventory Transaction and updates the Stock Balance.
    """
    try:
        model_name = model_name.lower()
        ctype = ContentType.objects.get(model=model_name)

        # 1. Record Inventory Transaction (The Movement Log)
        InventoryTransaction.objects.create(
            content_type=ctype,
            object_id=object_id,
            transaction_type='PRODUCTION', # Or 'HARVEST' depending on your choices
            quantity=qty,
            description=f"Produced/Collected {qty} {unit} of {item_name}",
        )

        # 2. Adjust Inventory Stock (The Current Balance)
        success = adjust_inventory_stock(
            user=user,
            model_name=model_name,
            object_id=object_id,
            category=category,
            item_name=item_name,
            quantity=qty,
            unit=unit,
            action="add"
        )
        
        return success
    except Exception as e:
        print(f"Production Flow Error: {e}")
        return False

@transaction.atomic
def process_full_sale(user, sale_instance):
    # 1. Financial Ledger (Income)
    FinancialTransaction.objects.create(
        type='INCOME',
        amount=sale_instance.total_amount,
        category="Sales",
        reference_type=ContentType.objects.get_for_model(sale_instance),
        reference_id=sale_instance.id
    )

    # 2. Inventory Transaction Log
    InventoryTransaction.objects.create(
        content_type=sale_instance.content_type,
        object_id=sale_instance.object_id,
        transaction_type='SALE',
        quantity=sale_instance.quantity,
        description=f"Sold {sale_instance.item}"
    )

    # 3. Hybrid Reduction
    model_name = sale_instance.content_type.model
    
    # Determine item details for logic
    if model_name == 'animal':
        category = getattr(sale_instance.item, 'species', 'Livestock')
        item_name = getattr(sale_instance.item, 'tag_id', 'Unknown')
        # Mark animal as sold in the actual Animal model
        Animal.objects.filter(id=sale_instance.object_id).update(status='sold', is_active=False)
    else:
        category = getattr(sale_instance.item, 'category', 'General')
        item_name = getattr(sale_instance.item, 'name', 'Product')

    adjust_inventory_stock(
        user=user,
        model_name=model_name,
        object_id=sale_instance.object_id,
        category=category,
        item_name=item_name,
        quantity=sale_instance.quantity,
        unit="Units",
        action="remove"
    )
    
    Logger.write(user, "Sale Completed", f"Processed sale for {item_name}", "Finance")