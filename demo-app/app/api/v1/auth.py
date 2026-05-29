from fastapi import APIRouter, Depends

from app.core.config import get_settings
from app.core.dependencies import get_auth_service, get_current_user
from app.db.models.user import User
from app.schemas.auth import LoginRequest, RegisterRequest, TokenResponse, UserResponse
from app.services.auth import AuthService


settings = get_settings()
router = APIRouter(prefix=f"{settings.api_prefix}/auth", tags=["auth"])


@router.post("/register", response_model=UserResponse, status_code=201)
async def register(
    payload: RegisterRequest,
    auth_service: AuthService = Depends(get_auth_service),
) -> UserResponse:
    user = await auth_service.register(payload.email, payload.full_name, payload.password)
    return UserResponse.from_model(user)


@router.post("/login", response_model=TokenResponse)
async def login(
    payload: LoginRequest,
    auth_service: AuthService = Depends(get_auth_service),
) -> TokenResponse:
    token = await auth_service.login(payload.email, payload.password)
    return TokenResponse(access_token=token)


@router.get("/me", response_model=UserResponse)
async def me(current_user: User = Depends(get_current_user)) -> UserResponse:
    return UserResponse.from_model(current_user)