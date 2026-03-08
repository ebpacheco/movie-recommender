# app/routers/auth_router.py
from fastapi import APIRouter, Depends

from app.dependencies import get_user_service, auth_service
from app.schemas.user_schema import UserCreate, LoginRequest, TokenResponse, UserResponse
from app.services.user_service import UserService

router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post("/register", response_model=UserResponse, status_code=201)
def register(data: UserCreate, service: UserService = Depends(get_user_service)):
    user = service.register(data)
    return user


@router.post("/login", response_model=TokenResponse)
def login(data: LoginRequest, service: UserService = Depends(get_user_service)):
    user  = service.authenticate(data.email, data.password)
    token = auth_service.create_access_token(str(user.id))
    return TokenResponse(access_token=token)
