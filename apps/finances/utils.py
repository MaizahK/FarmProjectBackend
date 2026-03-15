from django.db import transaction
from django.contrib.contenttypes.models import ContentType
from rest_framework.exceptions import ValidationError
from .models import FinancialTransaction, Expense, Sale, RecurringExpense, RecurringExpenseType
from ..inventory.models import Inventory, InventoryTransaction
from ..inventory.utils import adjust_inventory_stock
from ..logs.utils.helper import Logger
from ..animals.models import Animal

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
            unit=unit,
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
            unit=unit,
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
def process_financial_flow(user, tx_type, amount, category, item_name, ref_model, ref_data, is_standalone=False, is_recurring=False, recurring_type_id=None):
    """
    Main entry point for Financial Transactions.
    Bridges Finance, Inventory, and Recurring templates.
    """
    ctype = ContentType.objects.get(model=ref_model)
    item_id = ref_data.get('object_id', 0)
    qty = ref_data.get('quantity', 0)
    unit = ref_data.get('unit', 'Units')
    description = ref_data.get('description', f"{tx_type} for {category}")

    # --- 1. INCOME (SALE) LOGIC ---
    if tx_type == 'INCOME':
        if not is_standalone:
            # Inventory Validation: Must exist and have enough stock
            # Products usually use object_id 0 in hybrid inventory systems
            target_inv_id = item_id if ref_model == 'animal' else 0
            
            inv_item = Inventory.objects.filter(
                content_type=ctype, 
                object_id=target_inv_id,
                category_name=category
            ).first()

            if not inv_item:
                raise ValidationError(f"Item '{category}' not found in inventory.")
            
            if inv_item.quantity < qty:
                raise ValidationError(f"Insufficient stock. Available: {inv_item.quantity}, Requested: {qty}")

        # Create Sale Record with new fields
        reference_obj = Sale.objects.create(
            content_type=ctype,
            object_id=item_id,
            category_name=category,
            quantity=qty,
            price_per_item=amount / qty if qty > 0 else amount,
            is_paid=ref_data.get('is_paid', True),
            description=description,
            notes=ref_data.get('notes', '')
        )

    # --- 2. EXPENSE LOGIC ---
    else: 
        reference_obj = Expense.objects.create(
            content_type=ctype,
            object_id=item_id,
            category_name=category,
            amount=amount,
            is_paid=ref_data.get('is_paid', True),
            description=description
        )

        # RECURRING LOGIC (Only for Expenses in this context)
        if is_recurring and recurring_type_id:
            try:
                r_type = RecurringExpenseType.objects.get(id=recurring_type_id)
                RecurringExpense.objects.get_or_create(
                    expense_type=r_type,
                    name=category,
                    user=user,
                    defaults={'amount': amount}
                )
            except RecurringExpenseType.DoesNotExist:
                pass

    # --- 3. FINANCIAL LEDGER ---
    FinancialTransaction.objects.create(
        type=tx_type,
        amount=amount,
        category=category,
        reference_type=ContentType.objects.get_for_model(reference_obj),
        reference_id=reference_obj.id,
        payment_method=ref_data.get('payment_method', 'Cash'),
        notes=ref_data.get('notes', '')
    )

    # --- 4. INVENTORY IMPACT ---
    if not is_standalone:
        action = "remove" if tx_type == 'INCOME' else "add"
        
        # Log Movement
        InventoryTransaction.objects.create(
            content_type=ctype,
            object_id=item_id,
            transaction_type='SALE' if tx_type == 'INCOME' else 'PURCHASE',
            quantity=qty,
            unit=unit,
            description=description
        )

        # Adjust Balance (Utility handles decrement/deletion or increment)
        adjust_inventory_stock(
            user=user,
            model_name=ref_model,
            object_id=item_id,
            category=category,
            item_name=item_name, # Using category as item name
            quantity=qty,
            unit=unit,
            action=action
        )

        # Special Animal Handling: If animal is sold, mark as inactive
        if tx_type == 'INCOME' and ref_model == 'animal':
            Animal.objects.filter(id=item_id).update(status='sold', is_active=False)

    Logger.write(user, f"Finance: {tx_type}", f"Processed {category} (Standalone: {is_standalone})", "Finance")
    return True
