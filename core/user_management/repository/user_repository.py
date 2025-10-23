# django_backend_starter/apps/loan/core/interfaces/user_repository.py

from abc import ABC, abstractmethod
from ..entity.user_entity import UserEntity


class IUserRepository(ABC):
    @abstractmethod
    def get_by_email(self, email: str) -> UserEntity | None:
        pass
