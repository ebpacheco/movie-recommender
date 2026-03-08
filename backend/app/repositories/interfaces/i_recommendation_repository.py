# app/repositories/interfaces/i_recommendation_repository.py
from abc import ABC, abstractmethod
from uuid import UUID

from app.models.recommendation_model import Recommendation


class IRecommendationRepository(ABC):

    @abstractmethod
    def find_by_id(self, recommendation_id: UUID) -> Recommendation | None:
        pass

    @abstractmethod
    def find_all_by_user_id(self, user_id: UUID) -> list[Recommendation]:
        pass

    @abstractmethod
    def save(self, recommendation: Recommendation) -> Recommendation:
        pass
