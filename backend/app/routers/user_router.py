# app/routers/user_router.py
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, status

from app.dependencies import get_user_service, get_current_user_id
from app.schemas.user_schema import (
    UserResponse, ProfileResponse, ProfileUpdate, LanguageUpdate,
    UserRoleUpdate, UserAdminResponse, UserAdminUpdate, UserPageResponse,
)
from app.models.user_model import UserRole
from app.services.user_service import UserService
from app.core.session_cache import update_session, update_profile_session, get_session

router = APIRouter(prefix="/users", tags=["Users"])


def require_admin(
    user_id: UUID        = Depends(get_current_user_id),
    service: UserService = Depends(get_user_service),
):
    user = service.get_by_id(user_id)
    if user.role != UserRole.admin:
        raise HTTPException(status.HTTP_403_FORBIDDEN, "Acesso restrito a administradores")
    return user_id


# ── Rotas do próprio usuário ───────────────────────────────────────────────────

@router.get("/me", response_model=UserResponse)
def get_me(
    user_id: UUID        = Depends(get_current_user_id),
    service: UserService = Depends(get_user_service),
):
    return service.get_by_id(user_id)


@router.get("/me/profile", response_model=ProfileResponse)
def get_profile(
    user_id: UUID        = Depends(get_current_user_id),
    service: UserService = Depends(get_user_service),
):
    # Tenta servir do cache antes de ir ao banco
    session = get_session(user_id)
    if session and "profile" in session:
        profile = service.get_profile_by_user_id(user_id)
        return profile
    user = service.get_by_id(user_id)
    return user.profile


@router.put("/me/profile", response_model=ProfileResponse)
def update_profile(
    data:    ProfileUpdate,
    user_id: UUID        = Depends(get_current_user_id),
    service: UserService = Depends(get_user_service),
):
    profile = service.update_profile(user_id, data)
    # Atualiza cache mantendo language intacta
    session = get_session(user_id)
    language = session["profile"].get("language", "pt") if session else "pt"
    update_profile_session(user_id, {
        "language":           language,
        "favorite_genres":    data.favorite_genres,
        "favorite_movies":    data.favorite_movies,
        "favorite_actors":    data.favorite_actors,
        "favorite_directors": data.favorite_directors,
    })
    return profile


@router.patch("/me/language", status_code=204)
def update_language(
    data:    LanguageUpdate,
    user_id: UUID        = Depends(get_current_user_id),
    service: UserService = Depends(get_user_service),
):
    """Atualiza apenas o idioma — não toca em gêneros, filmes, atores ou diretores."""
    service.update_language(user_id, data.language)
    update_session(user_id, language=data.language)


# ── Rotas de administrador ─────────────────────────────────────────────────────

@router.get("/admin/users", response_model=UserPageResponse)
def list_all_users(
    page:      int         = 1,
    page_size: int         = 20,
    _:         UUID        = Depends(require_admin),
    service:   UserService = Depends(get_user_service),
):
    if page < 1:        page = 1
    if page_size < 1:   page_size = 1
    if page_size > 100: page_size = 100
    return service.list_paginated(page, page_size)


@router.patch("/admin/users/{target_user_id}/role", response_model=UserAdminResponse)
def update_user_role(
    target_user_id: UUID,
    data:           UserRoleUpdate,
    _:              UUID        = Depends(require_admin),
    service:        UserService = Depends(get_user_service),
):
    return service.update_role(target_user_id, data.role)


@router.patch("/admin/users/{target_user_id}", response_model=UserAdminResponse)
def update_user(
    target_user_id: UUID,
    data:           UserAdminUpdate,
    _:              UUID        = Depends(require_admin),
    service:        UserService = Depends(get_user_service),
):
    return service.update_user(target_user_id, data)


@router.delete("/admin/users/{target_user_id}", status_code=204)
def delete_user(
    target_user_id: UUID,
    admin_id:       UUID        = Depends(require_admin),
    service:        UserService = Depends(get_user_service),
):
    if target_user_id == admin_id:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, "Não é possível excluir a própria conta")
    service.delete_user(target_user_id)