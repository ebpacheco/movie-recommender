# app/schemas/password_reset_schema.py
from pydantic import BaseModel, EmailStr


class ForgotPasswordRequest(BaseModel):
    email: EmailStr


class ResetPasswordRequest(BaseModel):
    token:    str
    password: str


class MessageResponse(BaseModel):
    message: str