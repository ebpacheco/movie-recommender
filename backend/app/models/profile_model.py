# app/models/profile_model.py
import uuid
from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.dialects.postgresql import UUID, ARRAY
from sqlalchemy.orm import relationship

from app.database import Base


class Profile(Base):
    __tablename__ = "profiles"

    id                  = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id             = Column(UUID(as_uuid=True), ForeignKey("users.id"), unique=True, nullable=False)
    favorite_genres     = Column(ARRAY(String), default=[])
    favorite_movies     = Column(ARRAY(String), default=[])
    favorite_actors     = Column(ARRAY(String), default=[])
    favorite_directors  = Column(ARRAY(String), default=[])
    language            = Column(String,    nullable=False, server_default='pt')
    country             = Column(String(2), nullable=False, server_default='BR')
    streaming_platforms = Column(ARRAY(String), nullable=False, server_default='{}')

    user = relationship("User", back_populates="profile")