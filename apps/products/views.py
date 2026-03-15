from django.shortcuts import render
from ..logs.utils.helper import Logger
from ..finances.utils import process_inventory_production
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .models import Product, ProductType
from .serializers import ProductSerializer, ProductTypeSerializer


class ProductTypeViewSet(viewsets.ModelViewSet):
    queryset = ProductType.objects.all()
    serializer_class = ProductTypeSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        instance = serializer.save()
        Logger.write(
            user=self.request.user,
            title="Product Type Created",
            description=f"Created product category: {instance.name}",
            module="Products"
        )

    def perform_update(self, serializer):
        instance = serializer.save()
        Logger.write(
            user=self.request.user,
            title="Product Type Updated",
            description=f"Updated product category: {instance.name}",
            module="Products"
        )

    def perform_destroy(self, instance):
        name = instance.name
        instance.delete()
        Logger.write(
            user=self.request.user,
            title="Product Type Deleted",
            description=f"Deleted product category: {name}",
            module="Products"
        )


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.filter(is_deleted=False)
    serializer_class = ProductSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        queryset = Product.objects.filter(is_deleted=False)
        rt_name = self.request.query_params.get('type')
        if rt_name:
            queryset = queryset.filter(product_type__name__iexact=rt_name)
        return queryset

    def perform_create(self, serializer):
        # 1. Save the model instance
        instance = serializer.save()
        
        # 2. Basic Activity Log
        animal_info = f" from Animal: {instance.animal.tag_id}" if instance.animal else ""
        Logger.write(
            user=self.request.user,
            title="Product Recorded",
            description=f"Recorded {instance.product_type.name}: {instance.description}{animal_info}",
            module="Products"
        )

        # 3. Handle Production Inventory Flow
        if getattr(serializer, '_add_to_inventory', False):
            # This handles both the Transaction Log and the Stock Balance
            process_inventory_production(
                user=self.request.user,
                model_name="product",
                object_id=instance.id,
                qty=instance.quantity,
                category=instance.product_type.name,
                item_name=instance.description,
                unit=instance.unit
            )
    def perform_update(self, serializer):
        instance = serializer.save()
        
        Logger.write(
            user=self.request.user,
            title="Product Updated",
            description=f"Updated product details: {instance.description}",
            module="Products"
        )

        # if getattr(serializer, '_add_to_inventory', False):
        #     try:
        #         qty = float(instance.quantity)
        #     except (TypeError, ValueError):
        #         qty = 0

        #     # Usually used for stock corrections during update
        #     adjust_inventory_stock(
        #         user=self.request.user,
        #         model_name="product",
        #         object_id=instance.id,
        #         category=instance.product_type.name,
        #         item_name=instance.description,
        #         quantity=qty,
        #         unit=instance.unit,
        #         action="add",
        #     )

    def perform_destroy(self, instance):
        desc = instance.description
        instance.is_deleted = True
        # Assuming your model has 'is_active', otherwise omit this line
        if hasattr(instance, 'is_active'):
            instance.is_active = False 
        instance.save()

        # Optional: Remove from inventory on delete if query param is passed
        # remove_inv = self.request.query_params.get("remove_from_inventory")
        # if str(remove_inv).lower() in ("1", "true", "yes"):
        #     try:
        #         qty = float(instance.quantity)
        #     except (TypeError, ValueError):
        #         qty = 0

        #     adjust_inventory_stock(
        #         user=self.request.user,
        #         model_name="product",
        #         object_id=instance.id,
        #         category=instance.product_type.name,
        #         item_name=instance.description,
        #         quantity=qty,
        #         unit=instance.unit,
        #         action="remove",
        #     )

        Logger.write(
            user=self.request.user,
            title="Product Deleted",
            description=f"Removed product: {desc}",
            module="Products"
        )