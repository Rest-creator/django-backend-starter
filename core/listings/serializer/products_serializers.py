from rest_framework import serializers
from ..service.product_service import ProductService
from ..entities.product_entity import ProductEntity

class ProductImageReadSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    image_url = serializers.URLField()

class ProductReadSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    user_id = serializers.IntegerField()
    name = serializers.CharField()
    quantity = serializers.CharField()
    unit = serializers.CharField()
    price = serializers.CharField()
    category = serializers.CharField()
    description = serializers.CharField()
    organic = serializers.BooleanField()
    location = serializers.CharField()
    status = serializers.CharField()
    inquiries = serializers.IntegerField()
    views = serializers.IntegerField()
    images = ProductImageReadSerializer(many=True)

    @staticmethod
    def from_entity(entity: ProductEntity) -> dict:
        return {
            "id": entity.id,
            "user_id": entity.user_id,
            "name": entity.name,
            "quantity": entity.quantity,
            "unit": entity.unit,
            "price": entity.price,
            "category": entity.category,
            "description": entity.description,
            "organic": entity.organic,
            "location": entity.location,
            "status": entity.status,
            "inquiries": entity.inquiries,
            "views": entity.views,
            "images": [{"id": i.id, "image_url": i.image_url} for i in entity.images],
        }

class ProductWriteSerializer(serializers.Serializer):
    name = serializers.CharField()
    quantity = serializers.CharField()
    unit = serializers.CharField()
    price = serializers.DecimalField(max_digits=10, decimal_places=2)
    category = serializers.CharField()
    description = serializers.CharField()
    organic = serializers.BooleanField(required=False, default=False)
    location = serializers.CharField()
    status = serializers.CharField(required=False, default="active")

    # For uploads: images[] in multipart/form-data
    images = serializers.ListField(
        child=serializers.ImageField(),
        required=False,
        allow_empty=True
    )

    def create(self, validated_data):
        images = validated_data.pop("images", [])
        user = self.context["request"].user
        entity = ProductService.create_product(user_id=user.id, payload=validated_data, images_files=images)
        return ProductReadSerializer.from_entity(entity)

    def update(self, instance, validated_data):  # instance unused (we pass id through view)
        # not used by DRF directly; handled in view with service
        return validated_data  # not called
