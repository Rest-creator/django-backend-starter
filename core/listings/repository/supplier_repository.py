from teseapi.models import SupplierProduct

class SupplierProductRepository:
    @staticmethod
    def get_all():
        return SupplierProduct.objects.all().order_by('-created_at').prefetch_related('images')

    @staticmethod
    def get_active():
        return SupplierProduct.objects.filter(status='active').prefetch_related('images')

    @staticmethod
    def get_by_user(user):
        return SupplierProduct.objects.filter(user=user).order_by('-created_at').prefetch_related('images')

    @staticmethod
    def get_by_id(id):
        return SupplierProduct.objects.prefetch_related('images').get(id=id)
