# app/schemas/user_schema.py
import re
from uuid import UUID
from datetime import date
from pydantic import BaseModel, EmailStr, field_validator
from app.models.user_model import UserRole


def _parse_date(v) -> date | None:
    """
    Aceita datas nos formatos:
      - date object          → passa direto
      - YYYY-MM-DD           → ISO (padrão Pydantic)
      - DD/MM/YYYY           → Brasileiro
      - MM/DD/YYYY           → Americano  (detectado quando dia > 12 na 2ª posição)
      - YYYY/MM/DD           → variação ISO com barra
    Ambiguidade (ambos ≤ 12): assume DD/MM/YYYY (padrão brasileiro).
    """
    if v is None or isinstance(v, date):
        return v
    if not isinstance(v, str) or not v.strip():
        return None
    v = v.strip()

    if re.match(r'^\d{4}-\d{2}-\d{2}$', v):
        return v  # Pydantic converte ISO normalmente

    if '/' in v:
        parts = v.split('/')
        if len(parts) == 3:
            a, b, c = parts
            if len(a) == 4:                   # YYYY/MM/DD
                return date(int(a), int(b), int(c))
            if len(c) == 4:
                ai, bi, ci = int(a), int(b), int(c)
                if ai > 12:                   # DD/MM/YYYY (dia na 1ª posição)
                    return date(ci, bi, ai)
                elif bi > 12:                 # MM/DD/YYYY (dia na 2ª posição)
                    return date(ci, ai, bi)
                else:                         # ambíguo → assume DD/MM/YYYY
                    return date(ci, bi, ai)

    raise ValueError(f"Formato de data inválido: '{v}'. Use DD/MM/AAAA ou AAAA-MM-DD")


# --- Profile ---

PROFILE_LIMITS = {
    "favorite_genres":    3,
    "favorite_movies":    3,
    "favorite_actors":    5,
    "favorite_directors": 3,
}


class ProfileBase(BaseModel):
    favorite_genres:     list[str] = []
    favorite_movies:     list[str] = []
    favorite_actors:     list[str] = []
    favorite_directors:  list[str] = []
    streaming_platforms: list[str] = []
    country:             str = 'BR'


class ProfileCreate(ProfileBase):
    pass


class ProfileUpdate(ProfileBase):

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

    @field_validator('streaming_platforms', mode='before')
    @classmethod
    def coerce_streaming(cls, v):
        return v or []

    class Config:
        from_attributes = True


# --- User ---

_PASSWORD_RULES = re.compile(
    r'^(?=.*[A-Z])(?=.*[0-9])(?=.*[!@#$%^&*()\-_=+\[\]{};:\'",.<>?/\\|`~]).{8,}$'
)


class UserCreate(BaseModel):
    name:           str
    email:          EmailStr
    password:       str
    birth_date:     date | None = None
    terms_accepted: bool = False
    profile:        ProfileCreate

    @field_validator("birth_date", mode="before")
    @classmethod
    def parse_birth_date(cls, v):
        return _parse_date(v)

    @field_validator("password")
    @classmethod
    def validate_password_strength(cls, v):
        if len(v) < 8:
            raise ValueError("A senha deve ter pelo menos 8 caracteres")
        if not re.search(r'[A-Z]', v):
            raise ValueError("A senha deve conter pelo menos uma letra maiúscula")
        if not re.search(r'[0-9]', v):
            raise ValueError("A senha deve conter pelo menos um número")
        if not re.search(r'[!@#$%^&*()\-_=+\[\]{};:\'",.<>?/\\|`~]', v):
            raise ValueError("A senha deve conter pelo menos um caractere especial")
        return v


class UserResponse(BaseModel):
    id:         UUID
    name:       str
    email:      str
    role:       UserRole
    birth_date: date | None = None
    profile:    ProfileResponse | None = None

    class Config:
        from_attributes = True


# --- Auth ---

class LoginRequest(BaseModel):
    email:             EmailStr
    password:          str
    recaptcha_token:   str = ""


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