from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    SaleViewSet, ExpenseViewSet, 
    RecurringExpenseTypeViewSet, RecurringExpenseViewSet, FinancialTransactionViewSet
)

router = DefaultRouter()
router.register(r'financial-transactions', FinancialTransactionViewSet)
router.register(r'sales', SaleViewSet)
router.register(r'expenses', ExpenseViewSet)
router.register(r'recurring-types', RecurringExpenseTypeViewSet)
router.register(r'recurring-expenses', RecurringExpenseViewSet)

urlpatterns = [
    path('api/', include(router.urls)),
]