# app/dependencies.py
from uuid import UUID

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError
from sqlalchemy.orm import Session

from app.core.config import settings
from app.database import get_db
from app.providers.interfaces.i_ai_provider import IAIProvider
from app.providers.gemini_provider import GeminiProvider
from app.providers.openai_provider import OpenAIProvider
from app.providers.smtp_provider import SmtpProvider
from app.providers.ses_provider import SesProvider
from app.repositories.user_repository import UserRepository, ProfileRepository
from app.repositories.recommendation_repository import RecommendationRepository
from app.repositories.reset_token_repository import ResetTokenRepository
from app.builders.movie_prompt_builder import MoviePromptBuilder
from app.services.auth_service import AuthService
from app.services.user_service import UserService
from app.services.profile_service import ProfileService
from app.services.admin_service import AdminService
from app.services.recommendation_service import RecommendationService
from app.services.email_service import EmailService
from app.services.password_reset_service import PasswordResetService
from app.services.email_verification_service import EmailVerificationService
from app.repositories.email_verification_repository import EmailVerificationRepository

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login")
auth_service  = AuthService()


def _make_ai_provider() -> IAIProvider:
    if settings.AI_PROVIDER == "openai":
        return OpenAIProvider()
    return GeminiProvider()


def _make_email_service() -> EmailService:
    provider = SesProvider() if settings.EMAIL_PROVIDER == "ses" else SmtpProvider()
    return EmailService(provider)


def get_email_verification_service(db: Session = Depends(get_db)) -> EmailVerificationService:
    return EmailVerificationService(
        user_repo         = UserRepository(db),
        verification_repo = EmailVerificationRepository(db),
        email_service     = _make_email_service(),
    )


def get_user_service(db: Session = Depends(get_db)) -> UserService:
    return UserService(
        user_repo              = UserRepository(db),
        profile_repo           = ProfileRepository(db),
        auth_service           = auth_service,
        email_verification_svc = EmailVerificationService(
            user_repo         = UserRepository(db),
            verification_repo = EmailVerificationRepository(db),
            email_service     = _make_email_service(),
        ),
    )


def get_profile_service(db: Session = Depends(get_db)) -> ProfileService:
    return ProfileService(
        profile_repo        = ProfileRepository(db),
        user_repo           = UserRepository(db),
        recommendation_repo = RecommendationRepository(db),
    )


def get_admin_service(db: Session = Depends(get_db)) -> AdminService:
    return AdminService(user_repo=UserRepository(db))


def get_recommendation_service(db: Session = Depends(get_db)) -> RecommendationService:
    return RecommendationService(
        profile_repo        = ProfileRepository(db),
        recommendation_repo = RecommendationRepository(db),
        ai_provider         = _make_ai_provider(),
        prompt_builder      = MoviePromptBuilder(),
    )


def get_password_reset_service(db: Session = Depends(get_db)) -> PasswordResetService:
    return PasswordResetService(
        user_repo        = UserRepository(db),
        reset_token_repo = ResetTokenRepository(db),
        auth_service     = auth_service,
        email_service    = _make_email_service(),
    )


def get_current_user_id(token: str = Depends(oauth2_scheme)) -> UUID:
    try:
        user_id = auth_service.decode_token(token)
        return UUID(user_id)
    except (JWTError, ValueError):
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, "Token inválido ou expirado")
