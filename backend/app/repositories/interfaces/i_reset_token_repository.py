# app/repositories/interfaces/i_reset_token_repository.py
from abc import ABC, abstractmethod
from uuid import UUID

from app.models.reset_token_model import PasswordResetToken


class IResetTokenRepository(ABC):

    @abstractmethod
    def save(self, token: PasswordResetToken) -> PasswordResetToken:
        pass

    @abstractmethod
    def find_valid(self, token: str) -> PasswordResetToken | None:
        pass

    @abstractmethod
    def invalidate_pending(self, user_id: UUID) -> None:
        pass
