from core.interfaces.user_repository import UserRepository
from core.entities.user import User
from apps.appapi.models import UserModel  # Django ORM model

class UserRepository(UserRepository):
    def save(self, user: User):
        UserModel.objects.create(username=user.username, email=user.email)

    def exists_by_email(self, email: str) -> bool:
        return UserModel.objects.filter(email=email).exists()
