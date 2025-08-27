from django.db import transaction
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from core.listings.repository.supplier_repository import SupplierProductRepository
from core.listings.serializer.supplier_serializer import SupplierProductSerializer
from teseapi.models import ListingImage, SupplierProduct

class SupplierProductService:
    
    @staticmethod
    def create(user, validated_data, files=None):
        files = files or []
        with transaction.atomic():
            supplier_product = SupplierProduct.objects.create(user=user, **validated_data)
            for image_file in files:
                ListingImage.objects.create(content_object=supplier_product, image_url=image_file.url if hasattr(image_file, 'url') else None)
            
            # Broadcast creation
            channel_layer = get_channel_layer()
            async_to_sync(channel_layer.group_send)(
                "supplier_products",
                {"type": "supplier_product_update", "data": SupplierProductSerializer(supplier_product).data}
            )
            return supplier_product

    @staticmethod
    def update(instance, validated_data, files=None):
        files = files or []
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        for image_file in files:
            ListingImage.objects.create(content_object=instance, image_url=image_file.url if hasattr(image_file, 'url') else None)
        
        # Broadcast update
        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            "supplier_products",
            {"type": "supplier_product_update", "data": SupplierProductSerializer(instance).data}
        )
        return instance

    @staticmethod
    def delete(instance):
        instance_id = instance.id
        instance.delete()
        # Broadcast deletion
        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            "supplier_products",
            {"type": "supplier_product_delete", "data": {"id": str(instance_id)}}
        )
