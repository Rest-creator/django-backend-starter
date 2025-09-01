from ..entity.comment_entity import Comment, CommentLike

class CommentRepository:

    @staticmethod
    def create_comment(user, product, content, parent=None):
        return Comment.objects.create(user=user, product=product, content=content, parent=parent)

    @staticmethod
    def get_comments_by_product(product_id):
        return Comment.objects.filter(product_id=product_id, parent=None).prefetch_related("replies", "likes")

    @staticmethod
    def get_comment(comment_id):
        return Comment.objects.get(id=comment_id)

    @staticmethod
    def add_like(user, comment):
        return CommentLike.objects.get_or_create(user=user, comment=comment)

    @staticmethod
    def remove_like(user, comment):
        return CommentLike.objects.filter(user=user, comment=comment).delete()
