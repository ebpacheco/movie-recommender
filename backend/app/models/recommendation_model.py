# app/models/recommendation_model.py
import uuid
from datetime import datetime

from sqlalchemy import Column, String, Text, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import relationship

from app.database import Base


class Recommendation(Base):
    __tablename__ = "recommendations"

    id           = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id      = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False, unique=True)
    prompt_used  = Column(Text, nullable=True)
    response     = Column(JSONB, nullable=True)
    message      = Column(Text, nullable=True)
    language     = Column(String(8), nullable=False, server_default='pt')
    created_at   = Column(DateTime, nullable=False, default=datetime.utcnow)

    user = relationship("User", back_populates="recommendations")