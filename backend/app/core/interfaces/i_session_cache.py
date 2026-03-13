# app/core/interfaces/i_session_cache.py
from abc import ABC, abstractmethod
from typing import Optional
from uuid import UUID


class ISessionCache(ABC):

    @abstractmethod
    def set_session(self, user_id: UUID, data: dict) -> None:
        pass

    @abstractmethod
    def get_session(self, user_id: UUID) -> Optional[dict]:
        pass

    @abstractmethod
    def update_session(self, user_id: UUID, **kwargs) -> None:
        pass

    @abstractmethod
    def update_profile_session(self, user_id: UUID, profile: dict) -> None:
        pass

    @abstractmethod
    def clear_session(self, user_id: UUID) -> None:
        pass

    @abstractmethod
    def has_session(self, user_id: UUID) -> bool:
        pass
