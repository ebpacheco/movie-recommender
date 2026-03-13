# app/services/password_reset_service.py
import secrets
from datetime import datetime, timedelta

from fastapi import HTTPException, status

from app.models.reset_token_model import PasswordResetToken
from app.repositories.interfaces.i_user_repository import IUserRepository
from app.repositories.interfaces.i_reset_token_repository import IResetTokenRepository
from app.services.auth_service import AuthService
from app.services.email_service import EmailService

TOKEN_EXPIRY_HOURS = 1


class PasswordResetService:

    def __init__(
        self,
        user_repo:        IUserRepository,
        reset_token_repo: IResetTokenRepository,
        auth_service:     AuthService,
        email_service:    EmailService,
    ):
        self.user_repo        = user_repo
        self.reset_token_repo = reset_token_repo
        self.auth_service     = auth_service
        self.email_service    = email_service

    def request_reset(self, email: str) -> None:
        """
        Gera token e envia e-mail.
        Sempre retorna 200 mesmo se o e-mail não existir (evita enumeração de usuários).
        """
        user = self.user_repo.find_by_email(email)
        if not user:
            return  # silencioso — não revela se o e-mail existe

        self.reset_token_repo.invalidate_pending(user.id)

        token = secrets.token_urlsafe(48)
        rec = PasswordResetToken(
            user_id    = user.id,
            token      = token,
            expires_at = datetime.utcnow() + timedelta(hours=TOKEN_EXPIRY_HOURS),
        )
        self.reset_token_repo.save(rec)

        language = getattr(user.profile, "language", "pt") or "pt"
        self.email_service.send_password_reset_email(
            to       = user.email,
            name     = user.name,
            token    = token,
            language = language,
        )

    def reset_password(self, token: str, new_password: str) -> None:
        """Valida token e aplica nova senha."""
        rec = self.reset_token_repo.find_valid(token)

        if not rec:
            raise HTTPException(
                status.HTTP_400_BAD_REQUEST,
                "Link inválido ou expirado. Solicite um novo link."
            )

        rec.used_at = datetime.utcnow()
        self.reset_token_repo.save(rec)

        user = self.user_repo.find_by_id(rec.user_id)
        user.password_hash = self.auth_service.hash_password(new_password)
        self.user_repo.save(user)
