# app/services/user_service.py
import logging
from datetime import datetime
from uuid import UUID

from fastapi import HTTPException, status

logger = logging.getLogger(__name__)

from app.models.profile_model import Profile
from app.models.user_model import User
from app.repositories.interfaces.i_user_repository import IUserRepository, IProfileRepository
from app.schemas.user_schema import UserCreate
from app.services.auth_service import AuthService


class UserService:

    def __init__(
        self,
        user_repo:              IUserRepository,
        profile_repo:           IProfileRepository,
        auth_service:           AuthService,
        email_verification_svc=None,
    ):
        self.user_repo              = user_repo
        self.profile_repo           = profile_repo
        self.auth_service           = auth_service
        self.email_verification_svc = email_verification_svc

    def register(self, data: UserCreate) -> User:
        if self.user_repo.find_by_email(data.email):
            raise HTTPException(status.HTTP_409_CONFLICT, "E-mail já cadastrado")

        if not data.terms_accepted:
            raise HTTPException(status.HTTP_400_BAD_REQUEST, "É necessário aceitar os Termos de Uso para se cadastrar")

        user = User(
            name              = data.name,
            email             = data.email,
            password_hash     = self.auth_service.hash_password(data.password),
            birth_date        = data.birth_date,
            terms_accepted_at = datetime.utcnow() if data.terms_accepted else None,
        )
        self.user_repo.save(user)

        profile = Profile(
            user_id             = user.id,
            favorite_genres     = data.profile.favorite_genres,
            favorite_movies     = data.profile.favorite_movies,
            favorite_actors     = data.profile.favorite_actors,
            favorite_directors  = data.profile.favorite_directors,
            country             = data.profile.country,
            streaming_platforms = [],
        )
        self.profile_repo.save(profile)

        if self.email_verification_svc:
            try:
                language = getattr(data.profile, "language", "pt") or "pt"
                self.email_verification_svc.send_verification(
                    user_id  = user.id,
                    email    = user.email,
                    name     = user.name,
                    language = language,
                )
            except Exception as e:
                logger.error(f"[register] Falha ao enviar e-mail de verificação para {user.email}: {e}")

        return user

    def get_by_id(self, user_id: UUID) -> User:
        user = self.user_repo.find_by_id(user_id)
        if not user:
            raise HTTPException(status.HTTP_404_NOT_FOUND, "Usuário não encontrado")
        return user

    def delete_self(self, user_id: UUID) -> None:
        user = self.user_repo.find_by_id(user_id)
        if not user:
            raise HTTPException(status.HTTP_404_NOT_FOUND, "Usuário não encontrado")
        self.user_repo.delete(user_id)
