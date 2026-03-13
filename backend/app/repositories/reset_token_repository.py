# app/repositories/reset_token_repository.py
from datetime import datetime
from uuid import UUID

from sqlalchemy.orm import Session

from app.models.reset_token_model import PasswordResetToken
from app.repositories.interfaces.i_reset_token_repository import IResetTokenRepository


class ResetTokenRepository(IResetTokenRepository):

    def __init__(self, db: Session):
        self.db = db

    def save(self, token: PasswordResetToken) -> PasswordResetToken:
        self.db.add(token)
        self.db.commit()
        self.db.refresh(token)
        return token

    def find_valid(self, token: str) -> PasswordResetToken | None:
        """Retorna token se existir, não estiver usado e não estiver expirado."""
        return (
            self.db.query(PasswordResetToken)
            .filter(
                PasswordResetToken.token      == token,
                PasswordResetToken.used_at    == None,
                PasswordResetToken.expires_at >  datetime.utcnow(),
            )
            .first()
        )

    def invalidate_pending(self, user_id: UUID) -> None:
        """Invalida todos os tokens pendentes de um usuário marcando used_at = now."""
        now = datetime.utcnow()
        (
            self.db.query(PasswordResetToken)
            .filter(
                PasswordResetToken.user_id    == user_id,
                PasswordResetToken.used_at    == None,
                PasswordResetToken.expires_at >  now,
            )
            .update({"used_at": now})
        )
        self.db.commit()