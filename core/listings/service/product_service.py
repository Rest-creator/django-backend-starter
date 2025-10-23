from typing import List, Optional, Tuple
from django.db import transaction
from ..repository.product_repository import ProductRepository
from ..repository.image_repository import ImageRepository
from ..entities.product_entity import ProductEntity
from core.utils.bytescale_client import BytescaleClient


class ProductService:

    @staticmethod
    @transaction.atomic
    def create_product(
        user_id: int, payload: dict, images_files: Optional[List] = None
    ) -> ProductEntity:
        """
        payload contains fields for Product model except 'user'.
        images_files: list of InMemoryUploadedFile from DRF.
        """
        product_data = {
            "user_id": user_id,
            "name": payload["name"],
            "quantity": payload["quantity"],
            "unit": payload["unit"],
            "price": payload["price"],
            "category": payload["category"],
            "description": payload["description"],
            "organic": payload.get("organic", False),
            "location": payload["location"],
            "status": payload.get("status", "active"),
        }
        product = ProductRepository.create(product_data)

        if images_files:
            urls = ProductService._upload_to_bytescale(images_files)
            ImageRepository.replace_product_images(product, urls)

        return ProductEntity.from_model(product)

    @staticmethod
    @transaction.atomic
    def update_product(
        product_id: int,
        user_id: int,
        payload: dict,
        images_files: Optional[List] = None,
    ) -> ProductEntity:
        product = ProductRepository.get_by_id(product_id)
        if not product:
            raise ValueError("Product not found")
        if product.user_id != user_id:
            raise PermissionError("Not authorized to modify this product")

        # Prepare update data (only allowed fields)
        allowed = [
            "name",
            "quantity",
            "unit",
            "price",
            "category",
            "description",
            "organic",
            "location",
            "status",
        ]
        update_data = {k: v for k, v in payload.items() if k in allowed}
        product = ProductRepository.update(product, update_data)

        if images_files is not None:  # if provided, we replace images
            urls = ProductService._upload_to_bytescale(images_files)
            ImageRepository.replace_product_images(product, urls)

        return ProductEntity.from_model(product)

    @staticmethod
    def get_product(product_id: int, increment_views: bool = False) -> ProductEntity:
        product = ProductRepository.get_by_id(product_id)
        if not product:
            raise ValueError("Product not found")
        if increment_views:
            ProductRepository.increment_views(product)
            # refresh views
            product = ProductRepository.get_by_id(product_id)
        return ProductEntity.from_model(product)

    @staticmethod
    def list_products(user_id: Optional[int] = None):
        qs = (
            ProductRepository.list_by_user(user_id)
            if user_id
            else ProductRepository.list_all()
        )
        return [ProductEntity.from_model(p) for p in qs]

    @staticmethod
    def delete_product(product_id: int, user_id: int) -> None:
        product = ProductRepository.get_by_id(product_id)
        if not product:
            raise ValueError("Product not found")
        if product.user_id != user_id:
            raise PermissionError("Not authorized to delete this product")
        ProductRepository.delete(product)

    # --------------------------
    # helpers
    # --------------------------
    @staticmethod
    def _upload_to_bytescale(images_files) -> List[str]:
        urls = []
        for f in images_files:
            f.seek(0)
            content = f.read()
            url = BytescaleClient.upload_file(
                f.name, content, getattr(f, "content_type", "application/octet-stream")
            )
            urls.append(url)
        return urls
