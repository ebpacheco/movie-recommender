# app/services/auth_service.py
from datetime import datetime, timedelta

from fastapi import HTTPException, status
from jose import jwt, JWTError
from pwdlib import PasswordHash
from pwdlib.hashers.bcrypt import BcryptHasher

from app.core.config import settings

pwd_hash = PasswordHash([BcryptHasher()])


class AuthService:

    def hash_password(self, password: str) -> str:
        return pwd_hash.hash(password)

    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        return pwd_hash.verify(plain_password, hashed_password)

    def create_access_token(self, user_id: str) -> str:
        expire  = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        payload = {"sub": user_id, "exp": expire}
        return jwt.encode(payload, settings.SECRET_KEY, algorithm=settings.ALGORITHM)

    def decode_token(self, token: str) -> str:
        """Retorna o user_id (sub) ou lança JWTError."""
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        user_id: str = payload.get("sub")
        if user_id is None:
            raise JWTError("Token inválido")
        return user_id

    def authenticate(self, email: str, password: str, user_repo) -> "User":  # noqa: F821
        """Valida credenciais e retorna o usuário ou lança 401/403."""
        user = user_repo.find_by_email(email)
        if not user or not self.verify_password(password, user.password_hash):
            raise HTTPException(status.HTTP_401_UNAUTHORIZED, "Credenciais inválidas")
        if not user.email_verified:
            raise HTTPException(
                status.HTTP_403_FORBIDDEN,
                "email_not_verified"
            )
        return user
