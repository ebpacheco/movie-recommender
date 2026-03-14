# app/routers/user_router.py
from uuid import UUID

from fastapi import APIRouter, Depends

from app.dependencies import get_user_service, get_profile_service, get_current_user_id
from app.schemas.user_schema import UserResponse, ProfileResponse, ProfileUpdate, LanguageUpdate
from app.services.user_service import UserService
from app.services.profile_service import ProfileService
from app.core.session_cache import update_session, update_profile_session, get_session

router = APIRouter(prefix="/users", tags=["Users"])


@router.get("/me", response_model=UserResponse)
def get_me(
    user_id: UUID        = Depends(get_current_user_id),
    service: UserService = Depends(get_user_service),
):
    return service.get_by_id(user_id)


@router.get("/me/profile", response_model=ProfileResponse)
def get_profile(
    user_id: UUID           = Depends(get_current_user_id),
    service: ProfileService = Depends(get_profile_service),
):
    return service.get_profile_by_user_id(user_id)


@router.put("/me/profile", response_model=ProfileResponse)
def update_profile(
    data:    ProfileUpdate,
    user_id: UUID           = Depends(get_current_user_id),
    service: ProfileService = Depends(get_profile_service),
):
    profile = service.update_profile(user_id, data)
    session = get_session(user_id)
    language = session["profile"].get("language", "pt") if session else "pt"
    update_profile_session(user_id, {
        "language":            language,
        "favorite_genres":     data.favorite_genres,
        "favorite_movies":     data.favorite_movies,
        "favorite_actors":     data.favorite_actors,
        "favorite_directors":  data.favorite_directors,
        "streaming_platforms": data.streaming_platforms,
    })
    return profile


@router.delete("/me", status_code=204)
def delete_me(
    user_id: UUID        = Depends(get_current_user_id),
    service: UserService = Depends(get_user_service),
):
    service.delete_self(user_id)


@router.patch("/me/language", status_code=204)
def update_language(
    data:    LanguageUpdate,
    user_id: UUID           = Depends(get_current_user_id),
    service: ProfileService = Depends(get_profile_service),
):
    """Atualiza apenas o idioma — não toca em gêneros, filmes, atores ou diretores."""
    service.update_language(user_id, data.language)
    update_session(user_id, language=data.language)
