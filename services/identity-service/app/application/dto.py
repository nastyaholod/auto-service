from pydantic import BaseModel, EmailStr
from uuid import UUID
from datetime import datetime

class RegisterUserCommand(BaseModel):
    email: EmailStr
    password: str
    first_name: str
    last_name: str

class LoginUserCommand(BaseModel):
    email: EmailStr
    password: str

class TokenResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"

class UserDTO(BaseModel):
    id: UUID
    email: str
    first_name: str
    last_name: str
    role: str
    created_at: datetime