# app/services/auth_service.py
from datetime import datetime, timedelta

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