from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from adapters.repositories.user_repository import DjangoUserRepository
from core.services.user_services import UserService


class UserRegisterView(APIView):
    def post(self, request):
        username = request.data.get("username")
        email = request.data.get("email")

        service = UserService(DjangoUserRepository())

        try:
            user = service.register_user(username, email)
            return Response(user.__dict__, status=status.HTTP_201_CREATED)
        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
