# app/schemas/user_schema.py
from uuid import UUID
from pydantic import BaseModel, EmailStr
from app.models.user_model import UserRole


# --- Profile ---

class ProfileBase(BaseModel):
    favorite_genres:    list[str] = []
    favorite_movies:    list[str] = []
    favorite_actors:    list[str] = []
    favorite_directors: list[str] = []


class ProfileCreate(ProfileBase):
    pass


class ProfileUpdate(ProfileBase):
    pass


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