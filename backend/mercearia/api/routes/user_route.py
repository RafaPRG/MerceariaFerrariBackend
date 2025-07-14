from fastapi import APIRouter, HTTPException, Depends
from mercearia.api.schemas.user_schema import (
    LoginRequest,
    UpdatePasswordRequest,
    UserResponse,
    TokenResponse,
)
from mercearia.domain.entities.user import User
from mercearia.infra.repositories.in_memory_user_repository import (
    InMemoryUserRepository,
)
from mercearia.usecases.user.login_user import LoginUser
from mercearia.usecases.user.update_password import UpdatePassword
from typing import cast, Literal
from mercearia.api.security import create_access_token
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

router = APIRouter()
repo = InMemoryUserRepository()
security = HTTPBearer()


@router.post("/login", response_model=TokenResponse, summary="Login de usuário")
def login(data: LoginRequest):
    try:
        usecase = LoginUser(repo)
        user: User = usecase.execute(data.email, data.password)
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
def update_password(
    data: UpdatePasswordRequest,
    credentials: HTTPAuthorizationCredentials = Depends(security),
):
    try:
        usecase = UpdatePassword(repo)
        usecase.execute(data.email, data.new_password)
        return {"message": "Senha atualizada com sucesso"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
