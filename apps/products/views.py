from django.shortcuts import render
from ..logs.utils.helper import Logger
from ..inventory.utils import adjust_inventory_stock
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
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        """
        Optional: Filter Products by type via URL query params
        Example: /api/Products/?type=Vaccine
        """
        queryset = Product.objects.all()
        rt_name = self.request.query_params.get('type')
        if rt_name:
            # Fixed: changed Product_type to product_type to match model field
            queryset = queryset.filter(product_type__name__iexact=rt_name)
        return queryset

    def perform_create(self, serializer):
        instance = serializer.save()
        animal_info = f" for Animal: {instance.animal.tag_id}" if instance.animal else ""
        Logger.write(
            user=self.request.user,
            title="Product Created",
            description=f"Added {instance.product_type.name}: {instance.description}{animal_info}",
            module="Products"
        )

        if getattr(serializer, '_add_to_inventory', False):
            try:
                qty = float(instance.quantity)
            except (TypeError, ValueError):
                qty = 0

            adjust_inventory_stock(
                user=self.request.user,
                model_name="product",
                object_id=instance.id,
                category=instance.product_type.name,
                item_name=instance.description,
                quantity=qty,
                unit=instance.unit,
                action="add",
            )

    def perform_update(self, serializer):
        instance = serializer.save()
        Logger.write(
            user=self.request.user,
            title="Product Updated",
            description=f"Updated product details: {instance.description}",
            module="Products"
        )

        if getattr(serializer, '_add_to_inventory', False):
            try:
                qty = float(instance.quantity)
            except (TypeError, ValueError):
                qty = 0

            adjust_inventory_stock(
                user=self.request.user,
                model_name="product",
                object_id=instance.id,
                category=instance.product_type.name,
                item_name=instance.description,
                quantity=qty,
                unit="Units",
                action="add",
            )

    def perform_destroy(self, instance):
        desc = instance.description
        instance.is_deleted = True
        instance.is_active = False 
        instance.save()

        add_inv = self.request.query_params.get("add_to_inventory")
        if str(add_inv).lower() in ("1", "true", "yes", "on"):
            try:
                qty = float(instance.quantity)
            except (TypeError, ValueError):
                qty = 0

            adjust_inventory_stock(
                user=self.request.user,
                model_name="product",
                object_id=instance.id,
                category=instance.product_type.name,
                item_name=instance.description,
                quantity=qty,
                unit="Units",
                action="remove",
            )

        Logger.write(
            user=self.request.user,
            title="Product Deleted",
            description=f"Removed product: {desc}",
            module="Products"
        )
