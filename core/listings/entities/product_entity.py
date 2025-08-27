from dataclasses import dataclass
from typing import List, Optional

@dataclass
class ProductImageEntity:
    id: int
    image_url: str

@dataclass
class ProductEntity:
    id: int
    user_id: int
    name: str
    quantity: str
    unit: str
    price: str
    category: str
    description: str
    organic: bool
    location: str
    status: str
    inquiries: int
    views: int
    images: List[ProductImageEntity]

    @staticmethod
    def from_model(product):
        images = [
            ProductImageEntity(id=img.id, image_url=img.image_url)
            for img in product.product_images.all()
        ]
        return ProductEntity(
            id=product.id,
            user_id=product.user_id,
            name=product.name,
            quantity=product.quantity,
            unit=product.unit,
            price=str(product.price),
            category=product.category,
            description=product.description,
            organic=product.organic,
            location=product.location,
            status=product.status,
            inquiries=product.inquiries,
            views=product.views,
            images=images,
        )
