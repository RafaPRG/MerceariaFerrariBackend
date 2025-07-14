from pydantic import BaseModel, EmailStr, Field
from typing import Literal


class LoginRequest(BaseModel):
    email: EmailStr = Field(..., description="Email do usuário")
    password: str = Field(..., min_length=6, description="Senha do usuário")


class UpdatePasswordRequest(BaseModel):
    email: EmailStr = Field(..., description="Email do usuário")
    new_password: str = Field(..., min_length=6, description="Nova senha do usuário")


class UserResponse(BaseModel):
    nome: str = Field(..., description="Nome do usuário")
    email: EmailStr = Field(..., description="Email do usuário")
    tipo: Literal["user", "admin"] = Field(..., description="Tipo de usuário")


class TokenResponse(BaseModel):
    access_token: str
    token_type: str
    user: UserResponse
