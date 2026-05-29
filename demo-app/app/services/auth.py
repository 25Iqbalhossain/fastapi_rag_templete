from fastapi import HTTPException, status

from app.core.config import Settings
from app.core.security import create_access_token, hash_password, verify_password
from app.db.models.user import User
from app.db.repositories.user_repository import UserRepository


class AuthService:
    def __init__(self, users: UserRepository, settings: Settings) -> None:
        self.users = users
        self.settings = settings

    async def register(self, email: str, full_name: str, password: str) -> User:
        existing = await self.users.get_by_email(email)
        if existing is not None:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="User already exists",
            )
        return await self.users.create(
            email=email,
            full_name=full_name,
            hashed_password=hash_password(password),
        )

    async def login(self, email: str, password: str) -> str:
        user = await self.users.get_by_email(email)
        if user is None or not verify_password(password, user.hashed_password):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid email or password",
            )
        return create_access_token(subject=user.email, settings=self.settings)