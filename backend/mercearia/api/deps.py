from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from mercearia.api.settings import settings
from mercearia.domain.repositories.user_repository import UserRepository
from mercearia.infra.repositories.sqlalchemy.sqlalchemy_user_repository import (
    SQLAlchemyUserRepository,
)
from mercearia.infra.repositories.sqlalchemy.sqlalchemy_produto_repository import (
    SQLAlchemyProdutoRepository,
)
from mercearia.infra.repositories.sqlalchemy.sqlalchemy_favorito_repository import (
    SQLAlchemyFavoritoRepository,
)
from mercearia.domain.entities.user import User
from mercearia.infra.database import async_session
import sqlalchemy
from sqlalchemy.ext.asyncio import AsyncSession
from collections.abc import AsyncGenerator


# Geração de sessão assíncrona
async def get_db_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session() as session:
        yield session


# Repositórios com dependência da sessão
async def get_user_repository(
    db: AsyncSession = Depends(get_db_session),
) -> SQLAlchemyUserRepository:
    return SQLAlchemyUserRepository(db)


async def get_produto_repository(
    db: AsyncSession = Depends(get_db_session),
) -> SQLAlchemyProdutoRepository:
    return SQLAlchemyProdutoRepository(db)


async def get_favorito_repository(
    db: AsyncSession = Depends(get_db_session),
) -> SQLAlchemyFavoritoRepository:
    return SQLAlchemyFavoritoRepository(db)


# Autenticação OAuth2
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/users/login")


# Obter o usuário logado a partir do token JWT
async def get_current_user(
    token: str = Depends(oauth2_scheme),
    user_repo: UserRepository = Depends(get_user_repository),
) -> User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Não foi possível validar as credenciais",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = jwt.decode(
            token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
        )
        user_id: str = str(payload.get("sub"))
        if user_id is None:
            raise credentials_exception
        user = await user_repo.get_by_id(user_id)
        if user is None:
            raise credentials_exception
        await user_repo.set_current_user(user)
    except JWTError:
        raise credentials_exception

    user = await user_repo.get_current_user()
    if user is None:
        raise credentials_exception
    return user
