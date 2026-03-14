# app/repositories/email_verification_repository.py
from datetime import datetime
from uuid import UUID

from sqlalchemy.orm import Session

from app.models.email_verification_model import EmailVerificationToken


class EmailVerificationRepository:

    def __init__(self, db: Session):
        self.db = db

    def save(self, token: EmailVerificationToken) -> EmailVerificationToken:
        self.db.add(token)
        self.db.commit()
        self.db.refresh(token)
        return token

    def find_valid(self, token: str) -> EmailVerificationToken | None:
        return (
            self.db.query(EmailVerificationToken)
            .filter(
                EmailVerificationToken.token      == token,
                EmailVerificationToken.used_at    == None,
                EmailVerificationToken.expires_at >  datetime.utcnow(),
            )
            .first()
        )

    def invalidate_pending(self, user_id: UUID) -> None:
        now = datetime.utcnow()
        (
            self.db.query(EmailVerificationToken)
            .filter(
                EmailVerificationToken.user_id    == user_id,
                EmailVerificationToken.used_at    == None,
                EmailVerificationToken.expires_at >  now,
            )
            .update({"used_at": now})
        )
        self.db.commit()
