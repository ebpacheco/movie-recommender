# app/dependencies.py
from uuid import UUID

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError
from sqlalchemy.orm import Session

from app.database import get_db
from app.repositories.user_repository import UserRepository, ProfileRepository
from app.repositories.recommendation_repository import RecommendationRepository
from app.services.auth_service import AuthService
from app.services.user_service import UserService
from app.services.recommendation_service import RecommendationService
from app.providers.gemini_provider import GeminiProvider
from app.builders.movie_prompt_builder import MoviePromptBuilder

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login")
auth_service  = AuthService()


def get_user_service(db: Session = Depends(get_db)) -> UserService:
    return UserService(
        user_repo    = UserRepository(db),
        profile_repo = ProfileRepository(db),
        auth_service = auth_service,
    )


def get_recommendation_service(db: Session = Depends(get_db)) -> RecommendationService:
    return RecommendationService(
        profile_repo        = ProfileRepository(db),
        recommendation_repo = RecommendationRepository(db),
        ai_provider         = GeminiProvider(),
        prompt_builder      = MoviePromptBuilder(),
    )


def get_current_user_id(token: str = Depends(oauth2_scheme)) -> UUID:
    try:
        user_id = auth_service.decode_token(token)
        return UUID(user_id)
    except (JWTError, ValueError):
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, "Token inválido ou expirado")