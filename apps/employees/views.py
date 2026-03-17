from rest_framework import viewsets, status
from django.db import transaction as db_transaction
from .models import Employee, EmployeeType
from .serializers import EmployeeSerializer, EmployeeTypeSerializer
from ..finances.models import RecurringExpense, FinancialTransaction
from ..finances.utils import process_employee_salary_recurring
from ..logs.utils.helper import Logger

class EmployeeTypeViewSet(viewsets.ModelViewSet):
    queryset = EmployeeType.objects.all()
    serializer_class = EmployeeTypeSerializer

class EmployeeViewSet(viewsets.ModelViewSet):
    serializer_class = EmployeeSerializer

    def get_queryset(self):
        # Only return employees who are not soft-deleted
        return Employee.objects.filter(is_deleted=False)

    def perform_create(self, serializer):
        with db_transaction.atomic():
            is_recurring = serializer.validated_data.pop('is_recurring', False)
            employee = serializer.save()
            
            process_employee_salary_recurring(
                user=self.request.user,
                employee_id=employee.id,
                amount=employee.salary,
                employee_name=f"{employee.first_name} {employee.last_name}",
                is_recurring=is_recurring
            )
            Logger.write(self.request.user, "Employee", f"Created employee {employee.id}", "Employee")

    def perform_update(self, serializer):
        with db_transaction.atomic():
            old_salary = self.get_object().salary
            employee = serializer.save()

            print(old_salary, employee.salary)
            
            if old_salary != employee.salary:
                RecurringExpense.objects.filter(user_id=employee.id).update(amount=employee.salary)
                FinancialTransaction.objects.create(
                    type='EXPENSE',
                    amount=employee.salary,
                    category="Salary",
                    reference_type=ContentType.objects.get_for_model(expense),
                    reference_id=expense.id,
                    notes=f"Updated salary for employee ID: {employee_id}"
                )
                Logger.write(self.request.user, "Employee", f"Updated salary for {employee.id}", "Finance")

    def perform_destroy(self, instance):
        """
        Custom Soft Delete Logic
        """
        with db_transaction.atomic():
            # 1. Set the flag instead of deleting
            instance.is_deleted = True
            instance.save()

            # 2. Cleanup recurring expense templates (Stop future payments)
            RecurringExpense.objects.filter(user_id=instance.id).delete()

            # 3. Log the action
            Logger.write(
                self.request.user, 
                "Employee", 
                f"Soft-deleted employee {instance.id} and removed recurring salary template", 
                "Employee"
            )