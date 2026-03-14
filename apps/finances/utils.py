from django.db import transaction
from django.contrib.contenttypes.models import ContentType
from .models import FinancialTransaction, Expense, Sale
from ..inventory.models import InventoryTransaction
from ..inventory.utils import adjust_inventory_stock
from ..logs.utils.helper import Logger

@transaction.atomic
def process_inventory_purchase(user, model_name, object_id, amount, category, item_name, unit="Units"):
    """
    Full Purchase Flow using Collective Inventory
    """
    try:
        ctype = ContentType.objects.get(model=model_name.lower())
        qty = 1 # Purchase usually adds 1 unit/animal
        
        # 1. Expense Record
        expense = Expense.objects.create(
            content_type=ctype,
            object_id=object_id,
            category_name=category,
            amount=amount,
            is_paid=True,
            description=f"Purchase of {item_name} ({category})"
        )
        Logger.write(user, "Expense Created", f"Spent {amount} on {item_name}", "Finance")

        # 2. Financial Ledger
        FinancialTransaction.objects.create(
            type='EXPENSE',
            amount=amount,
            category=category,
            reference_type=ContentType.objects.get_for_model(expense),
            reference_id=expense.id
        )
        Logger.write(user, "Financial Ledger Updated", f"Recorded expense for {category}", "Finance")

        # 3. Inventory Transaction (Movement Log)
        InventoryTransaction.objects.create(
            content_type=ctype,
            object_id=object_id, # Link to specific animal/resource
            transaction_type='PURCHASE',
            quantity=qty,
            description=f"Collective stock entry for {item_name}",
            reference_type=ContentType.objects.get_for_model(expense),
            reference_id=expense.id
        )

        # 4. Use Utils to update Collective Inventory
        adjust_inventory_stock(
            user=user,
            model_name=model_name,
            category=category,
            item_name=item_name,
            quantity=qty,
            unit=unit,
            action="add"
        )
        
        return True
    except Exception as e:
        print(f"Error: {e}")
        return False

@transaction.atomic
def process_full_sale(user, sale_instance):
    """
    Full Sale Flow using Collective Inventory
    """
    # 1. Financial Ledger (Income)
    FinancialTransaction.objects.create(
        type='INCOME',
        amount=sale_instance.total_amount,
        category="Sales",
        reference_type=ContentType.objects.get_for_model(sale_instance),
        reference_id=sale_instance.id
    )
    Logger.write(user, "Income Recorded", f"Earned {sale_instance.total_amount}", "Finance")

    # 2. Inventory Transaction Log
    InventoryTransaction.objects.create(
        content_type=sale_instance.content_type,
        object_id=sale_instance.object_id,
        transaction_type='SALE',
        quantity=sale_instance.quantity,
        description=f"Sale of {sale_instance.quantity} units"
    )

    # 3. Reduce Collective Inventory
    adjust_inventory_stock(
        user=user,
        model_name=sale_instance.content_type.model,
        category=getattr(sale_instance.item, 'species', 'General'),
        item_name=getattr(sale_instance.item, 'breed', 'Product'),
        quantity=sale_instance.quantity,
        unit="Units",
        action="remove"
    )