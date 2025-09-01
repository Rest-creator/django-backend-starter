from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from ..services.comment_services import CommentService
from ..serializers.comment_serializer import CommentSerializer

class ProductCommentsView(generics.ListCreateAPIView):
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        product_id = self.kwargs["product_id"]
        return CommentService.get_product_comments(product_id)

    def perform_create(self, serializer):
        product_id = self.kwargs["product_id"]
        serializer.save(user=self.request.user, product_id=product_id)

class CommentLikeView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, comment_id):
        CommentService.like_comment(request.user, comment_id)
        return Response({"message": "Comment liked"}, status=status.HTTP_200_OK)

    def delete(self, request, comment_id):
        CommentService.unlike_comment(request.user, comment_id)
        return Response({"message": "Comment unliked"}, status=status.HTTP_200_OK)
