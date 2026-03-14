# app/routers/password_reset_router.py
from fastapi import APIRouter, Depends

from app.dependencies import get_password_reset_service, get_email_verification_service
from app.schemas.password_reset_schema import ForgotPasswordRequest, ResetPasswordRequest, MessageResponse
from app.services.password_reset_service import PasswordResetService
from app.services.email_verification_service import EmailVerificationService

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/forgot-password", response_model=MessageResponse)
def forgot_password(
    data:    ForgotPasswordRequest,
    service: PasswordResetService = Depends(get_password_reset_service),
):
    service.request_reset(data.email)
    return {"message": "Se este e-mail estiver cadastrado, você receberá o link em breve."}


@router.post("/reset-password", response_model=MessageResponse)
def reset_password(
    data:    ResetPasswordRequest,
    service: PasswordResetService = Depends(get_password_reset_service),
):
    service.reset_password(data.token, data.password)
    return {"message": "Senha redefinida com sucesso."}


@router.post("/verify-email", response_model=MessageResponse)
def verify_email(
    token:   str,
    service: EmailVerificationService = Depends(get_email_verification_service),
):
    service.verify_email(token)
    return {"message": "E-mail confirmado com sucesso!"}


@router.post("/resend-verification", response_model=MessageResponse)
def resend_verification(
    data:    ForgotPasswordRequest,   # reutiliza schema {email}
    service: EmailVerificationService = Depends(get_email_verification_service),
):
    service.resend_verification(data.email)
    return {"message": "Se este e-mail ainda não foi confirmado, um novo link foi enviado."}
