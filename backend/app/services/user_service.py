# app/services/user_service.py
from uuid import UUID
from fastapi import HTTPException, status

from app.models.user_model import User, UserRole
from app.models.profile_model import Profile
from app.repositories.interfaces.i_user_repository import IUserRepository, IProfileRepository
from app.schemas.user_schema import UserCreate, ProfileUpdate
from app.services.auth_service import AuthService


class UserService:

    def __init__(
        self,
        user_repo:    IUserRepository,
        profile_repo: IProfileRepository,
        auth_service: AuthService,
    ):
        self.user_repo    = user_repo
        self.profile_repo = profile_repo
        self.auth_service = auth_service

    def register(self, data: UserCreate) -> User:
        if self.user_repo.find_by_email(data.email):
            raise HTTPException(status.HTTP_409_CONFLICT, "E-mail já cadastrado")

        user = User(
            name          = data.name,
            email         = data.email,
            password_hash = self.auth_service.hash_password(data.password),
            birth_date    = data.birth_date,
        )
        self.user_repo.save(user)

        profile = Profile(
            user_id            = user.id,
            favorite_genres    = data.profile.favorite_genres,
            favorite_movies    = data.profile.favorite_movies,
            favorite_actors    = data.profile.favorite_actors,
            favorite_directors = data.profile.favorite_directors,
            country            = data.profile.country,
        )
        self.profile_repo.save(profile)

        return user

    def authenticate(self, email: str, password: str) -> User:
        user = self.user_repo.find_by_email(email)
        if not user or not self.auth_service.verify_password(password, user.password_hash):
            raise HTTPException(status.HTTP_401_UNAUTHORIZED, "Credenciais inválidas")
        return user

    def get_by_id(self, user_id: UUID) -> User:
        user = self.user_repo.find_by_id(user_id)
        if not user:
            raise HTTPException(status.HTTP_404_NOT_FOUND, "Usuário não encontrado")
        return user

    def update_profile(self, user_id: UUID, data: ProfileUpdate) -> Profile:
        profile = self.profile_repo.find_by_user_id(user_id)
        if not profile:
            raise HTTPException(status.HTTP_404_NOT_FOUND, "Perfil não encontrado")

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

    def get_profile_by_user_id(self, user_id: UUID):
        profile = self.profile_repo.find_by_user_id(user_id)
        if not profile:
            raise HTTPException(status.HTTP_404_NOT_FOUND, "Perfil não encontrado")
        return profile

    def list_all(self) -> list[User]:
        return self.user_repo.find_all()

    def list_paginated(self, page: int, page_size: int) -> dict:
        import math
        items, total = self.user_repo.find_paginated(page, page_size)
        return {
            "items": items,
            "total": total,
            "page":  page,
            "pages": max(1, math.ceil(total / page_size)),
        }

    def update_role(self, user_id: UUID, role: UserRole) -> User:
        user = self.user_repo.find_by_id(user_id)
        if not user:
            raise HTTPException(status.HTTP_404_NOT_FOUND, "Usuário não encontrado")
        user.role = role
        return self.user_repo.save(user)

    def update_user(self, user_id: UUID, data) -> User:
        user = self.user_repo.find_by_id(user_id)
        if not user:
            raise HTTPException(status.HTTP_404_NOT_FOUND, "Usuário não encontrado")
        existing = self.user_repo.find_by_email(data.email)
        if existing and existing.id != user_id:
            raise HTTPException(status.HTTP_409_CONFLICT, "E-mail já em uso por outro usuário")
        user.name  = data.name
        user.email = data.email
        user.role  = data.role
        return self.user_repo.save(user)

    def delete_user(self, user_id: UUID) -> None:
        user = self.user_repo.find_by_id(user_id)
        if not user:
            raise HTTPException(status.HTTP_404_NOT_FOUND, "Usuário não encontrado")
        self.user_repo.delete(user_id)