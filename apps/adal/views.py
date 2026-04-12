from rest_framework import viewsets
from .models import AdalRecord
from .serializers import AdalRecordSerializer
from apps.logs.utils.helper import Logger # Adjust path based on your structure

class AdalRecordViewSet(viewsets.ModelViewSet):
    queryset = AdalRecord.objects.all().order_by('-date_sent')
    serializer_class = AdalRecordSerializer

    def perform_create(self, serializer):
        # 1. Save the record
        instance = serializer.save()

        # 2. Log the creation
        Logger.write(
            user=self.request.user,
            title="Breeding Record Created",
            description=f"Sent animal {instance.animal.tag_id} for breeding. Price before: {instance.price_before}",
            module="Adal"
        )

    def perform_update(self, serializer):
        # 1. Save the updates
        instance = serializer.save()

        # 2. Log the update
        Logger.write(
            user=self.request.user,
            title="Breeding Record Updated",
            description=f"Updated breeding info for {instance.animal.tag_id}. Current status: {'Received' if instance.date_received else 'Sent'}",
            module="Adal"
        )

    def perform_destroy(self, instance):
        # 1. Capture details before deletion
        tag_id = instance.animal.tag_id
        
        # 2. Delete the record
        instance.delete()

        # 3. Log the deletion
        Logger.write(
            user=self.request.user,
            title="Breeding Record Deleted",
            description=f"Removed breeding record for animal: {tag_id}",
            module="Adal"
        )