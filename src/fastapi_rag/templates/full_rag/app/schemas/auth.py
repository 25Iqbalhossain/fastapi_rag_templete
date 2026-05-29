from pydantic import BaseModel, EmailStr, Field


class RegisterRequest(BaseModel):
    email: EmailStr
    full_name: str = Field(min_length=1, max_length=255)
    password: str = Field(min_length=8, max_length=128)


class LoginRequest(BaseModel):
    email: EmailStr
    password: str = Field(min_length=8, max_length=128)


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"


class UserResponse(BaseModel):
    id: int
    email: EmailStr
    full_name: str
    is_active: bool

    @classmethod
    def from_model(cls, user) -> "UserResponse":
        return cls(
            id=user.id,
            email=user.email,
            full_name=user.full_name,
            is_active=user.is_active,
        )
