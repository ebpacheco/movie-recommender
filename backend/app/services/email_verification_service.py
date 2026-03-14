# app/services/email_verification_service.py
import secrets
from datetime import datetime, timedelta

from fastapi import HTTPException, status

from app.models.email_verification_model import EmailVerificationToken
from app.repositories.email_verification_repository import EmailVerificationRepository
from app.repositories.interfaces.i_user_repository import IUserRepository
from app.services.email_service import EmailService

TOKEN_EXPIRY_HOURS = 24


class EmailVerificationService:

    def __init__(
        self,
        user_repo:          IUserRepository,
        verification_repo:  EmailVerificationRepository,
        email_service:      EmailService,
    ):
        self.user_repo         = user_repo
        self.verification_repo = verification_repo
        self.email_service     = email_service

    def send_verification(self, user_id, email: str, name: str, language: str = "pt") -> None:
        """Gera token e envia e-mail de confirmação."""
        self.verification_repo.invalidate_pending(user_id)

        token = secrets.token_urlsafe(48)
        rec = EmailVerificationToken(
            user_id    = user_id,
            token      = token,
            expires_at = datetime.utcnow() + timedelta(hours=TOKEN_EXPIRY_HOURS),
        )
        self.verification_repo.save(rec)
        self.email_service.send_email_verification(
            to       = email,
            name     = name,
            token    = token,
            language = language,
        )

    def verify_email(self, token: str) -> None:
        """Marca e-mail como verificado a partir do token."""
        rec = self.verification_repo.find_valid(token)
        if not rec:
            raise HTTPException(
                status.HTTP_400_BAD_REQUEST,
                "Link inválido ou expirado. Solicite um novo e-mail de confirmação."
            )

        rec.used_at = datetime.utcnow()
        self.verification_repo.save(rec)

        user = self.user_repo.find_by_id(rec.user_id)
        if not user:
            raise HTTPException(status.HTTP_404_NOT_FOUND, "Usuário não encontrado")

        user.email_verified    = True
        user.email_verified_at = datetime.utcnow()
        self.user_repo.save(user)

    def resend_verification(self, email: str) -> None:
        """Reenvia o e-mail de confirmação. Sempre retorna 200."""
        user = self.user_repo.find_by_email(email)
        if not user or user.email_verified:
            return  # silencioso

        language = getattr(user.profile, "language", "pt") or "pt"
        self.send_verification(user.id, user.email, user.name, language)
