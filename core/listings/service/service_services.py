from rest_framework import serializers
from django.db import transaction
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer

from ..repository.service_repository import ServiceRepository
from ...utils.bytescale_client import BytescaleClient
from ..serializer.service_serializer import ServiceSerializer


class ServiceService:

    @staticmethod
    def create_service(user, validated_data, images):
        uploaded_image_urls = []

        with transaction.atomic():
            service = ServiceRepository.create(user, validated_data)

            for img in images:
                img.seek(0)
                upload_result = BytescaleClient.upload_file(img)

                if "files" in upload_result and upload_result["files"]:
                    image_url = upload_result["files"][0].get("fileUrl")
                    if not image_url:
                        raise serializers.ValidationError(
                            {"images": f"FileUrl missing for {img.name}"}
                        )
                    uploaded_image_urls.append(image_url)
                else:
                    raise serializers.ValidationError(
                        {"images": f"Upload failed for {img.name}"}
                    )

            ServiceRepository.attach_images(service, uploaded_image_urls)

            serialized_service = ServiceSerializer(service).data
            ServiceService._broadcast("service_update", serialized_service)

            return serialized_service

    @staticmethod
    def update_service(service, validated_data):
        for attr, value in validated_data.items():
            setattr(service, attr, value)
        service.save()

        ServiceService._broadcast("service_update", ServiceSerializer(service).data)
        return service

    @staticmethod
    def delete_service(service):
        service_id = service.id
        service.delete()

        ServiceService._broadcast("service_delete", {"id": str(service_id)})

    @staticmethod
    def _broadcast(event_type, data):
        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            "services", {"type": event_type, "data": data}
        )
