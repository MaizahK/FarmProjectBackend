# from django.db import transaction
# from django.contrib.contenttypes.models import ContentType
# from .models import FinancialTransaction
# from ..inventory.models import InventoryTransaction

# @transaction.atomic
# def record_sale_flow(user, sale_instance):
#     """
#     Handles the 4-step process for a sale: 
#     1. Inventory reduction 2. Inventory Transaction 3. Financial Transaction
#     """
#     # 1. Create Inventory Transaction (Internal update is handled by InventoryTransaction View/Logic)
#     InventoryTransaction.objects.create(
#         content_type=sale_instance.content_type,
#         object_id=sale_instance.object_id,
#         transaction_type='SALE',
#         quantity=sale_instance.quantity,
#         description=f"Sale ID: {sale_instance.id}",
#         reference_type=ContentType.objects.get_for_model(sale_instance),
#         reference_id=sale_instance.id
#     )

#     # 2. Create Financial Transaction (Income)
#     FinancialTransaction.objects.create(
#         type='INCOME',
#         amount=sale_instance.total_amount,
#         category='Sales',
#         reference_type=ContentType.objects.get_for_model(sale_instance),
#         reference_id=sale_instance.id,
#         notes=f"Revenue from sale of {sale_instance.item}"
#     )

# @transaction.atomic
# def record_expense_flow(user, expense_instance):
#     """Handles expense financial records and inventory purchase if applicable"""
#     if expense_instance.content_type: # If it's a purchase (Feed/Med)
#         InventoryTransaction.objects.create(
#             content_type=expense_instance.content_type,
#             object_id=expense_instance.object_id,
#             transaction_type='PURCHASE',
#             quantity=1, # Logic depends on unit
#             description=f"Purchase via Expense ID: {expense_instance.id}",
#             reference_type=ContentType.objects.get_for_model(expense_instance),
#             reference_id=expense_instance.id
#         )

#     FinancialTransaction.objects.create(
#         type='EXPENSE',
#         amount=expense_instance.amount,
#         category=expense_instance.category_name,
#         reference_type=ContentType.objects.get_for_model(expense_instance),
#         reference_id=expense_instance.id,
#     )


from django.db import transaction
from django.contrib.contenttypes.models import ContentType
from .models import FinancialTransaction, Sale, Expense
from ..inventory.models import Inventory, InventoryTransaction
from ..animals.models import Animal

@transaction.atomic
def process_inventory_purchase(user, model_name, object_id, amount, category, item_name, unit):
    """
    Called when adding a new animal/resource with 'add_to_inventory=true'.
    Creates: 1. Expense, 2. Financial Transaction, 3. Inventory Transaction.
    """
    try:
        ctype = ContentType.objects.get(model=model_name.lower())
        
        # 1. Create Expense Record
        expense = Expense.objects.create(
            content_type=ctype,
            object_id=object_id,
            category_name=category,
            amount=amount,
            is_paid=True,
            description=f"Initial purchase of {item_name}"
        )

        # 2. Financial Ledger
        FinancialTransaction.objects.create(
            type='EXPENSE',
            amount=amount,
            category=category,
            reference_type=ContentType.objects.get_for_model(expense),
            reference_id=expense.id
        )

        # 3. Inventory Ledger
        InventoryTransaction.objects.create(
            content_type=ctype,
            object_id=object_id,
            transaction_type='PURCHASE',
            quantity=1 if model_name == 'animal' else 0, # Quantity logic
            description=f"Stock entry for {item_name}"
        )
    except Exception as e:
        print(e)

@transaction.atomic
def process_full_sale(user, sale_instance):
    """
    Handles Sale -> Finance -> Inventory -> Animal Status
    """
    # 1. Financial Ledger (Income)
    FinancialTransaction.objects.create(
        type='INCOME',
        amount=sale_instance.total_amount,
        category="Sales",
        reference_type=ContentType.objects.get_for_model(sale_instance),
        reference_id=sale_instance.id
    )

    # 2. Inventory Ledger (Reduction)
    InventoryTransaction.objects.create(
        content_type=sale_instance.content_type,
        object_id=sale_instance.object_id,
        transaction_type='SALE',
        quantity=sale_instance.quantity,
        description=f"Sale transaction #{sale_instance.id}"
    )

    # 3. Special Case: Animals
    if sale_instance.content_type.model == 'animal':
        Animal.objects.filter(id=sale_instance.object_id).update(
            status='sold', 
            is_active=False
        )