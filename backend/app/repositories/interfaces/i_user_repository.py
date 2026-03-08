# app/repositories/interfaces/i_user_repository.py
from abc import ABC, abstractmethod
from uuid import UUID

from app.models.user_model import User
from app.models.profile_model import Profile


class IUserRepository(ABC):

    @abstractmethod
    def find_by_id(self, user_id: UUID) -> User | None:
        pass

    @abstractmethod
    def find_by_email(self, email: str) -> User | None:
        pass

    @abstractmethod
    def find_by_cpf(self, cpf: str) -> User | None:
        pass

    @abstractmethod
    def save(self, user: User) -> User:
        pass


class IProfileRepository(ABC):

    @abstractmethod
    def find_by_user_id(self, user_id: UUID) -> Profile | None:
        pass

    @abstractmethod
    def save(self, profile: Profile) -> Profile:
        pass
