from django.urls import path
from .comment_views import ProductCommentsView, CommentLikeView

urlpatterns = [
    # Fetch & create comments on a product
    path(
        "products/<int:product_id>/comments/",
        ProductCommentsView.as_view(),
        name="product-comments",
    ),
    # Like / Unlike a comment
    path(
        "comments/<int:comment_id>/like/",
        CommentLikeView.as_view(),
        name="comment-like",
    ),
]
