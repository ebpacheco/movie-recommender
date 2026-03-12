# app/models/user_model.py
import uuid
import enum
from sqlalchemy import Column, String, Enum, Date
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from app.database import Base


class UserRole(str, enum.Enum):
    free    = "free"
    premium = "premium"
    admin   = "admin"


class User(Base):
    __tablename__ = "users"

    id            = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name          = Column(String, nullable=False)
    email         = Column(String, unique=True, nullable=False, index=True)
    cpf           = Column(String(11), unique=True, nullable=False)
    password_hash = Column(String, nullable=False)
    role          = Column(Enum(UserRole), nullable=False, default=UserRole.free)
    birth_date    = Column(Date, nullable=True)

    profile         = relationship("Profile", back_populates="user", uselist=False, cascade="all, delete-orphan")
    recommendations = relationship("Recommendation", back_populates="user", cascade="all, delete-orphan")