# app/routers/user_router.py
from uuid import UUID
from fastapi import APIRouter, Depends

from app.dependencies import get_user_service, get_current_user_id
from app.schemas.user_schema import UserResponse, ProfileResponse, ProfileUpdate
from app.services.user_service import UserService

router = APIRouter(prefix="/users", tags=["Users"])


@router.get("/me", response_model=UserResponse)
def get_me(
    user_id: UUID          = Depends(get_current_user_id),
    service: UserService   = Depends(get_user_service),
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
    user_id: UUID          = Depends(get_current_user_id),
    service: UserService   = Depends(get_user_service),
):
    return service.update_profile(user_id, data)
