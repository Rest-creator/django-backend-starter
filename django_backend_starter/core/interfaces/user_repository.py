from abc import ABC, abstractmethod
from core.entities.user import User

class UserRepository(ABC):
    @abstractmethod
    def save(self, user: User):
        pass

    @abstractmethod
    def exists_by_email(self, email: str) -> bool:
        pass
