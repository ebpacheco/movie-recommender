# app/schemas/user_schema.py
from uuid import UUID
from pydantic import BaseModel, EmailStr
from app.models.user_model import UserRole


# --- Profile ---

PROFILE_LIMITS = {
    "favorite_genres":    3,
    "favorite_movies":    3,
    "favorite_actors":    5,
    "favorite_directors": 3,
}


class ProfileBase(BaseModel):
    favorite_genres:    list[str] = []
    favorite_movies:    list[str] = []
    favorite_actors:    list[str] = []
    favorite_directors: list[str] = []


class ProfileCreate(ProfileBase):
    pass


class ProfileUpdate(ProfileBase):
    from pydantic import field_validator

    @field_validator("favorite_genres")
    @classmethod
    def limit_genres(cls, v):
        if len(v) > PROFILE_LIMITS["favorite_genres"]:
            raise ValueError(f"Máximo de {PROFILE_LIMITS['favorite_genres']} gêneros favoritos")
        return v

    @field_validator("favorite_movies")
    @classmethod
    def limit_movies(cls, v):
        if len(v) > PROFILE_LIMITS["favorite_movies"]:
            raise ValueError(f"Máximo de {PROFILE_LIMITS['favorite_movies']} filmes favoritos")
        return v

    @field_validator("favorite_actors")
    @classmethod
    def limit_actors(cls, v):
        if len(v) > PROFILE_LIMITS["favorite_actors"]:
            raise ValueError(f"Máximo de {PROFILE_LIMITS['favorite_actors']} atores favoritos")
        return v

    @field_validator("favorite_directors")
    @classmethod
    def limit_directors(cls, v):
        if len(v) > PROFILE_LIMITS["favorite_directors"]:
            raise ValueError(f"Máximo de {PROFILE_LIMITS['favorite_directors']} diretores favoritos")
        return v


class ProfileResponse(ProfileBase):
    id:      UUID
    user_id: UUID

    class Config:
        from_attributes = True


# --- User ---

class UserCreate(BaseModel):
    name:     str
    email:    EmailStr
    cpf:      str
    password: str
    profile:  ProfileCreate


class UserResponse(BaseModel):
    id:      UUID
    name:    str
    email:   str
    role:    UserRole
    profile: ProfileResponse | None = None

    class Config:
        from_attributes = True


# --- Auth ---

class LoginRequest(BaseModel):
    email:    EmailStr
    password: str


class TokenResponse(BaseModel):
    access_token: str
    token_type:   str = "bearer"


# --- Language ---

class LanguageUpdate(BaseModel):
    language: str


# --- Admin ---

class UserAdminUpdate(BaseModel):
    name:  str
    email: EmailStr
    role:  UserRole


class UserRoleUpdate(BaseModel):
    role: UserRole


class UserAdminResponse(BaseModel):
    id:    UUID
    name:  str
    email: str
    role:  UserRole

    class Config:
        from_attributes = True


class UserPageResponse(BaseModel):
    items: list[UserAdminResponse]
    total: int
    page:  int
    pages: int