from rest_framework import serializers
from teseapi.models import Product, Service, SupplierProduct
from serializer.products_serializers import ProductReadSerializer
from serializer.service_serializer import ServiceSerializer
from serializer.supplier_serializer import SupplierProductSerializer

class UserListingSerializer(serializers.Serializer):
    """
    Generic wrapper serializer for user listings.
    Dynamically uses the correct serializer based on the listing type.
    """

    listing_type = serializers.CharField(read_only=True)
    data = serializers.SerializerMethodField()

    def get_data(self, obj):
        """
        Returns the serialized data based on the object's model type.
        """
        if isinstance(obj, Product):
            serializer = ProductReadSerializer(obj, context=self.context)
            listing_type = 'product'
        elif isinstance(obj, Service):
            serializer = ServiceSerializer(obj, context=self.context)
            listing_type = 'service'
        elif isinstance(obj, SupplierProduct):
            serializer = SupplierProductSerializer(obj, context=self.context)
            listing_type = 'supplier_product'
        else:
            raise Exception(f"Unsupported object type: {type(obj)}")

        # Attach the listing_type dynamically
        self._listing_type = listing_type
        return serializer.data

    def to_representation(self, instance):
        """
        Overrides the default representation to include listing_type alongside serialized data.
        """
        data = super().to_representation(instance)
        data['listing_type'] = getattr(self, '_listing_type', 'unknown')
        return data
