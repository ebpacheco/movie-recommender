# app/repositories/recommendation_repository.py
from uuid import UUID
from sqlalchemy.orm import Session

from app.models.recommendation_model import Recommendation
from app.repositories.interfaces.i_recommendation_repository import IRecommendationRepository


class RecommendationRepository(IRecommendationRepository):

    def __init__(self, db: Session):
        self.db = db

    def find_by_id(self, recommendation_id: UUID) -> Recommendation | None:
        return self.db.query(Recommendation).filter(Recommendation.id == recommendation_id).first()

    def find_all_by_user_id(self, user_id: UUID) -> list[Recommendation]:
        return (
            self.db.query(Recommendation)
            .filter(Recommendation.user_id == user_id)
            .order_by(Recommendation.created_at.desc())
            .all()
        )

    def save(self, recommendation: Recommendation) -> Recommendation:
        self.db.add(recommendation)
        self.db.commit()
        self.db.refresh(recommendation)
        return recommendation
