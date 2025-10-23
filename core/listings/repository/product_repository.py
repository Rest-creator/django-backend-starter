from typing import Optional, Iterable
from django.db.models import QuerySet
from teseapi.models import Product


class ProductRepository:
    @staticmethod
    def create(product_data: dict) -> Product:
        return Product.objects.create(**product_data)

    @staticmethod
    def update(product: Product, update_data: dict) -> Product:
        for k, v in update_data.items():
            setattr(product, k, v)
        product.save()
        return product

    @staticmethod
    def delete(product: Product) -> None:
        product.delete()

    @staticmethod
    def get_by_id(product_id: int) -> Optional[Product]:
        return Product.objects.filter(id=product_id).first()

    @staticmethod
    def list_all() -> QuerySet:
        return (
            Product.objects.all()
            .select_related("user")
            .prefetch_related("product_images")
        )

    @staticmethod
    def list_by_user(user_id: int) -> QuerySet:
        return (
            Product.objects.filter(user_id=user_id)
            .select_related("user")
            .prefetch_related("product_images")
        )

    @staticmethod
    def increment_views(product: Product) -> None:
        Product.objects.filter(id=product.id).update(views=product.views + 1)
