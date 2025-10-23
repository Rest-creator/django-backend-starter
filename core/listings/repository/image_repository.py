from typing import List
from teseapi.models import Product, ProductImage


class ImageRepository:
    @staticmethod
    def replace_product_images(product: Product, image_urls: List[str]) -> None:
        # Clear then add
        product.product_images.all().delete()
        ProductImage.objects.bulk_create(
            [ProductImage(product=product, image_url=url) for url in image_urls]
        )
