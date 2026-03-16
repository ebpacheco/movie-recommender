# app/core/config.py
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    DATABASE_URL:                str
    SECRET_KEY:                  str
    ALGORITHM:                   str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60
    GEMINI_API_KEY:              str = ""
    OPENAI_API_KEY:              str = ""
    AI_PROVIDER:                 str = "gemini"
    APP_ENV:                     str = "development"
    RECAPTCHA_SECRET_KEY:        str = ""

    # E-mail
    EMAIL_PROVIDER:  str = "smtp"
    RESEND_API_KEY:  str = ""
    EMAIL_FROM:      str = "noreply@cinemagic.app"
    FRONTEND_URL:    str = "http://localhost:5173"

    @property
    def allowed_origins(self) -> list[str]:
        return [o.rstrip("/") for o in self.FRONTEND_URL.split(",") if o.strip()]
    SMTP_HOST:       str = "sandbox.smtp.mailtrap.io"
    SMTP_PORT:       int = 587
    SMTP_USER:       str = ""
    SMTP_PASSWORD:   str = ""
    AWS_REGION:      str = "us-east-1"
    AWS_ACCESS_KEY:  str = ""
    AWS_SECRET_KEY:  str = ""

    class Config:
        env_file = ".env"


settings = Settings()