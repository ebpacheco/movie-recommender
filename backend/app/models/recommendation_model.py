# app/models/recommendation_model.py
import uuid
from datetime import datetime
from sqlalchemy import Column, String, ForeignKey, DateTime, JSON
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from app.database import Base


class Recommendation(Base):
    __tablename__ = "recommendations"

    id          = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id     = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    prompt_used = Column(String, nullable=False)
    response    = Column(JSON, nullable=False)  # lista de filmes retornada pela IA
    created_at  = Column(DateTime, default=datetime.utcnow, nullable=False)

    user = relationship("User", back_populates="recommendations")
