# app/routers/user_router.py
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, status

from app.dependencies import get_user_service, get_current_user_id
from app.schemas.user_schema import (
    UserResponse, ProfileResponse, ProfileUpdate,
    UserRoleUpdate, UserAdminResponse, UserAdminUpdate, UserPageResponse,
)
from app.models.user_model import UserRole
from app.services.user_service import UserService

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
    user = service.get_by_id(user_id)
    return user.profile


@router.put("/me/profile", response_model=ProfileResponse)
def update_profile(
    data:    ProfileUpdate,
    user_id: UUID        = Depends(get_current_user_id),
    service: UserService = Depends(get_user_service),
):
    return service.update_profile(user_id, data)


# ── Rotas de administrador ─────────────────────────────────────────────────────

@router.get("/admin/users", response_model=UserPageResponse)
def list_all_users(
    page:      int         = 1,
    page_size: int         = 20,
    _:         UUID        = Depends(require_admin),
    service:   UserService = Depends(get_user_service),
):
    if page < 1:       page = 1
    if page_size < 1:  page_size = 1
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