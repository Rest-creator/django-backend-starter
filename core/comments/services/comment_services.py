from ..repository.comment_repository import CommentRepository


class CommentService:

    @staticmethod
    def add_comment(user, product, content, parent=None):
        return CommentRepository.create_comment(user, product, content, parent)

    @staticmethod
    def get_product_comments(product_id):
        return CommentRepository.get_comments_by_product(product_id)

    @staticmethod
    def like_comment(user, comment_id):
        comment = CommentRepository.get_comment(comment_id)
        return CommentRepository.add_like(user, comment)

    @staticmethod
    def unlike_comment(user, comment_id):
        comment = CommentRepository.get_comment(comment_id)
        return CommentRepository.remove_like(user, comment)
