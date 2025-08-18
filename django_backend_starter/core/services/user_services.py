from core.interfaces.user_repository import UserRepository
from core.entities.user import User

class UserService:
    def __init__(self, repo: UserRepository):
        self.repo = repo

    def register_user(self, username: str, email: str) -> User:
        if self.repo.exists_by_email(email):
            raise ValueError("Email already registered")
        user = User(username=username, email=email)
        self.repo.save(user)
        return user
