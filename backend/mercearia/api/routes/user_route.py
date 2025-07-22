from fastapi import APIRouter, HTTPException, Depends
from mercearia.api.schemas.user_schema import (
    LoginRequest,
    UpdatePasswordRequest,
    UserResponse,
    TokenResponse,
)
from mercearia.domain.entities.user import User
from mercearia.domain.repositories.user_repository import UserRepository
from mercearia.infra.repositories.sqlalchemy.sqlalchemy_user_repository import SQLAlchemyUserRepository
from mercearia.usecases.user.login_user import LoginUser
from mercearia.usecases.user.update_password import UpdatePassword
import sqlalchemy
from typing import cast, Literal
from mercearia.api.security import create_access_token
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from mercearia.api.deps import get_db_session, get_user_repository
from sqlalchemy.ext.asyncio import AsyncSession

router = APIRouter()
security = HTTPBearer()


@router.post("/login", response_model=TokenResponse, summary="Login de usuário")
async def login(data: LoginRequest, repo:UserRepository = Depends(get_user_repository)):
    try:
        usecase = LoginUser(repo)
        user: User = await usecase.execute(data.email, data.password)
        token = create_access_token(data={"sub": user.id})
        return TokenResponse(
            access_token=token,
            token_type="bearer",
            user=UserResponse(
                nome=user.name,
                email=str(user.email),
                tipo=cast(Literal["user", "admin"], user.role),
            ),
        )
    except Exception as e:
        raise HTTPException(status_code=401, detail=str(e))


@router.put("/update-password", summary="Atualizar senha do usuário")
async def update_password(
    data: UpdatePasswordRequest,
    session: AsyncSession = Depends(get_db_session),
    repo: UserRepository = Depends(get_user_repository)
):
    try:
        usecase = UpdatePassword(repo)
        await usecase.execute(data.email, data.new_password)
        return {"message": "Senha atualizada com sucesso"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
