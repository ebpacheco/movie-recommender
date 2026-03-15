# app/repositories/recommendation_repository.py
from uuid import UUID
from datetime import datetime, timedelta
from sqlalchemy.orm import Session

from app.models.recommendation_model import Recommendation


class RecommendationRepository:

    def __init__(self, db: Session):
        self.db = db

    def find_within_12h(self, user_id: UUID) -> Recommendation | None:
        """Retorna a recomendação mais recente do usuário se criada nas últimas 3h."""
        cutoff = datetime.utcnow() - timedelta(hours=3)
        return (
            self.db.query(Recommendation)
            .filter(
                Recommendation.user_id   == user_id,
                Recommendation.created_at >= cutoff,
            )
            .order_by(Recommendation.created_at.desc())
            .first()
        )

    def delete_expired(self) -> None:
        """Remove recomendações expiradas (mais de 3h) de todos os usuários."""
        cutoff = datetime.utcnow() - timedelta(hours=3)
        self.db.query(Recommendation).filter(
            Recommendation.created_at < cutoff
        ).delete(synchronize_session=False)
        self.db.commit()

    def upsert(self, recommendation: Recommendation) -> Recommendation:
        """Substitui qualquer recomendação anterior do usuário, mantendo 1 linha por usuário."""
        self.db.query(Recommendation).filter(
            Recommendation.user_id == recommendation.user_id
        ).delete(synchronize_session=False)
        self.db.add(recommendation)
        self.db.commit()
        self.db.refresh(recommendation)
        return recommendation