from teseapi.models import Service, ListingImage
from django.contrib.contenttypes.models import ContentType


class ServiceRepository:

    @staticmethod
    def create(user, validated_data):
        return Service.objects.create(user=user, **validated_data)

    @staticmethod
    def get_by_id(service_id):
        return Service.objects.filter(id=service_id).first()

    @staticmethod
    def get_all():
        return Service.objects.all().order_by('-created_at')

    @staticmethod
    def get_by_user(user):
        return Service.objects.filter(user=user).order_by('-created_at')

    @staticmethod
    def get_active():
        return Service.objects.filter(status="active").select_related("user")

    @staticmethod
    def delete(service):
        service.delete()

    @staticmethod
    def attach_images(service, image_urls):
        service_ct = ContentType.objects.get_for_model(Service)
        for url in image_urls:
            ListingImage.objects.create(
                content_type=service_ct,
                object_id=service.id,
                image_url=url
            )
