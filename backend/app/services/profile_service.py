# app/services/profile_service.py
from uuid import UUID

from fastapi import HTTPException, status

from app.models.profile_model import Profile
from app.models.user_model import UserRole
from app.repositories.interfaces.i_user_repository import IUserRepository, IProfileRepository
from app.repositories.recommendation_repository import RecommendationRepository
from app.schemas.user_schema import ProfileUpdate


class ProfileService:

    def __init__(
        self,
        profile_repo:        IProfileRepository,
        user_repo:           IUserRepository,
        recommendation_repo: RecommendationRepository,
    ):
        self.profile_repo        = profile_repo
        self.user_repo           = user_repo
        self.recommendation_repo = recommendation_repo

    def get_profile_by_user_id(self, user_id: UUID) -> Profile:
        profile = self.profile_repo.find_by_user_id(user_id)
        if not profile:
            raise HTTPException(status.HTTP_404_NOT_FOUND, "Perfil não encontrado")
        return profile

    def update_profile(self, user_id: UUID, data: ProfileUpdate) -> Profile:
        profile = self.profile_repo.find_by_user_id(user_id)
        if not profile:
            raise HTTPException(status.HTTP_404_NOT_FOUND, "Perfil não encontrado")

        is_admin = profile.user.role == UserRole.admin
        if not is_admin:
            locked_changed = (
                data.country != profile.country or
                set(data.streaming_platforms) != set(profile.streaming_platforms or [])
            )
            if locked_changed and self.recommendation_repo.find_within_12h(user_id):
                raise HTTPException(
                    status.HTTP_423_LOCKED,
                    "País e streamings estão bloqueados por 12h após gerar recomendações",
                )

        profile.favorite_genres     = data.favorite_genres
        profile.favorite_movies     = data.favorite_movies
        profile.favorite_actors     = data.favorite_actors
        profile.favorite_directors  = data.favorite_directors
        profile.streaming_platforms = data.streaming_platforms
        profile.country             = data.country

        return self.profile_repo.save(profile)

    def update_language(self, user_id: UUID, language: str) -> None:
        profile = self.profile_repo.find_by_user_id(user_id)
        if not profile:
            raise HTTPException(status.HTTP_404_NOT_FOUND, "Perfil não encontrado")
        profile.language = language
        self.profile_repo.save(profile)
