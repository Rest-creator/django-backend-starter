from rest_framework import serializers
from teseapi.models import Service, ListingImage


class ListingImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ListingImage
        fields = ["id", "image_url"]


class ServiceSerializer(serializers.ModelSerializer):
    images = serializers.SerializerMethodField()
    user = serializers.ReadOnlyField(source="user.id")

    class Meta:
        model = Service
        fields = [
            "id",
            "user",
            "name",
            "description",
            "status",
            "created_at",
            "updated_at",
            "images",
        ]
        read_only_fields = ["id", "created_at", "updated_at", "user"]

    def get_images(self, obj):
        return ListingImageSerializer(obj.images.all(), many=True).data
