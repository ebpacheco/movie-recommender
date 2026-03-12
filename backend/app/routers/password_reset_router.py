# app/routers/password_reset_router.py
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.repositories.reset_token_repository import ResetTokenRepository
from app.repositories.user_repository import UserRepository
from app.schemas.password_reset_schema import ForgotPasswordRequest, ResetPasswordRequest, MessageResponse
from app.services.auth_service import AuthService
from app.services.password_reset_service import PasswordResetService

router = APIRouter(prefix="/auth", tags=["auth"])


def get_service(db: Session = Depends(get_db)) -> PasswordResetService:
    return PasswordResetService(
        user_repo        = UserRepository(db),
        reset_token_repo = ResetTokenRepository(db),
        auth_service     = AuthService(),
    )


@router.post("/forgot-password", response_model=MessageResponse)
def forgot_password(data: ForgotPasswordRequest, service: PasswordResetService = Depends(get_service)):
    service.request_reset(data.email)
    # Sempre retorna a mesma mensagem — não revela se o e-mail existe
    return {"message": "Se este e-mail estiver cadastrado, você receberá o link em breve."}


@router.post("/reset-password", response_model=MessageResponse)
def reset_password(data: ResetPasswordRequest, service: PasswordResetService = Depends(get_service)):
    service.reset_password(data.token, data.password)
    return {"message": "Senha redefinida com sucesso."}