# app/services/cleanup_service.py
import asyncio
import logging
from datetime import datetime, timedelta

from app.database import SessionLocal
from app.models.user_model import User
from app.models.email_verification_model import EmailVerificationToken

logger = logging.getLogger(__name__)

INTERVAL_HOURS = 6
EXPIRY_HOURS   = 24


def _delete_unverified_users() -> int:
    """
    Remove usuários não verificados cujo token mais recente tem mais de 24h.
    Se o usuário reenviou o e-mail há menos de 24h, NÃO é deletado.
    Retorna a quantidade de usuários removidos.
    """
    db = SessionLocal()
    try:
        cutoff = datetime.utcnow() - timedelta(hours=EXPIRY_HOURS)

        # user_ids que têm pelo menos um token criado nas últimas 24h (resend recente)
        recent_token_user_ids = (
            db.query(EmailVerificationToken.user_id)
            .filter(EmailVerificationToken.created_at >= cutoff)
            .subquery()
        )

        # user_ids que têm algum token (ou seja, receberam e-mail de verificação)
        any_token_user_ids = (
            db.query(EmailVerificationToken.user_id)
            .subquery()
        )

        users = (
            db.query(User)
            .filter(
                User.email_verified == False,
                User.id.in_(any_token_user_ids),
                User.id.notin_(recent_token_user_ids),
            )
            .all()
        )

        count = len(users)
        for user in users:
            db.delete(user)

        db.commit()
        return count
    except Exception:
        db.rollback()
        logger.exception("Erro ao limpar usuários não verificados")
        return 0
    finally:
        db.close()


async def run_cleanup_loop() -> None:
    """Loop assíncrono que executa a limpeza a cada INTERVAL_HOURS horas."""
    logger.info(
        "Serviço de limpeza iniciado (intervalo: %dh, expiração: %dh)",
        INTERVAL_HOURS, EXPIRY_HOURS,
    )
    while True:
        await asyncio.sleep(INTERVAL_HOURS * 3600)
        logger.info("Executando limpeza de usuários não verificados...")
        deleted = _delete_unverified_users()
        logger.info("Limpeza concluída: %d usuário(s) removido(s)", deleted)
