# app/models/user_model.py
import uuid
from sqlalchemy import Column, String, ARRAY
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from app.database import Base


class User(Base):
    __tablename__ = "users"

    id            = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name          = Column(String, nullable=False)
    email         = Column(String, unique=True, nullable=False, index=True)
    cpf           = Column(String(11), unique=True, nullable=False)
    password_hash = Column(String, nullable=False)

    profile         = relationship("Profile", back_populates="user", uselist=False, cascade="all, delete-orphan")
    recommendations = relationship("Recommendation", back_populates="user", cascade="all, delete-orphan")
