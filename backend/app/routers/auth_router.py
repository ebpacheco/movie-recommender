# app/routers/auth_router.py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.dependencies import get_user_service, auth_service
from app.repositories.user_repository import UserRepository
from app.schemas.user_schema import UserCreate, LoginRequest, TokenResponse, UserResponse
from app.services.user_service import UserService
from app.services.recaptcha_service import verify_recaptcha
from app.core.session_cache import set_session

router = APIRouter(prefix="/auth", tags=["Auth"])


def _build_session(user) -> dict:
    """Monta o dicionário de sessão a partir do modelo User."""
    profile = user.profile
    return {
        "id":    str(user.id),
        "name":  user.name,
        "email": user.email,
        "role":  user.role.value if hasattr(user.role, "value") else user.role,
        "profile": {
            "language":           getattr(profile, "language",           "pt") if profile else "pt",
            "favorite_genres":    getattr(profile, "favorite_genres",    [])  if profile else [],
            "favorite_movies":    getattr(profile, "favorite_movies",    [])  if profile else [],
            "favorite_actors":    getattr(profile, "favorite_actors",    [])  if profile else [],
            "favorite_directors": getattr(profile, "favorite_directors", [])  if profile else [],
        },
    }


@router.post("/register", response_model=UserResponse, status_code=201)
def register(data: UserCreate, service: UserService = Depends(get_user_service)):
    user = service.register(data)
    set_session(user.id, _build_session(user))
    return user


@router.post("/login", response_model=TokenResponse)
def login(
    data: LoginRequest,
    db:   Session = Depends(get_db),
):
    if not verify_recaptcha(data.recaptcha_token):
        raise HTTPException(status.HTTP_400_BAD_REQUEST, "Verificação de segurança falhou. Tente novamente.")

    user_repo = UserRepository(db)
    user      = auth_service.authenticate(data.email, data.password, user_repo)
    token     = auth_service.create_access_token(str(user.id))
    set_session(user.id, _build_session(user))
    return TokenResponse(access_token=token, token_type="bearer")