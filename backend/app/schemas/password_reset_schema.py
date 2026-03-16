# app/schemas/password_reset_schema.py
import re
from pydantic import BaseModel, EmailStr, field_validator


class ForgotPasswordRequest(BaseModel):
    email: EmailStr


class ResetPasswordRequest(BaseModel):
    token:    str
    password: str

    @field_validator("password")
    @classmethod
    def validate_password_strength(cls, v):
        if len(v) < 8:
            raise ValueError("A senha deve ter pelo menos 8 caracteres")
        if not re.search(r'[A-Z]', v):
            raise ValueError("A senha deve conter pelo menos uma letra maiúscula")
        if not re.search(r'[0-9]', v):
            raise ValueError("A senha deve conter pelo menos um número")
        if not re.search(r'[!@#$%^&*()\-_=+\[\]{};:\'",.<>?/\\|`~]', v):
            raise ValueError("A senha deve conter pelo menos um caractere especial")
        return v


class MessageResponse(BaseModel):
    message: str