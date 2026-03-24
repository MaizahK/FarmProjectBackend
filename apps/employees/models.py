from django.db import models

class EmployeeType(models.Model):
    name = models.CharField(max_length=100) # e.g., Farmer, Driver
    description = models.TextField(blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

class Employee(models.Model):
    employee_type = models.ForeignKey(EmployeeType, on_delete=models.PROTECT, related_name='employees')
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    salary = models.DecimalField(max_digits=12, decimal_places=2)
    position = models.CharField(max_length=100) # specific title
    hire_date = models.DateField(auto_now_add=True)
    is_deleted = models.BooleanField(default=False)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.employee_type.name})"