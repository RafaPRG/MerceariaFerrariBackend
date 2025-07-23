from typing import Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update
from mercearia.domain.entities.user import User
from mercearia.domain.repositories.user_repository import UserRepository
from mercearia.domain.value_objects.email_vo import Email
from mercearia.domain.value_objects.password_vo import Password
from mercearia.infra.models.user_model import UserModel
from mercearia.api.security import verify_token


class SQLAlchemyUserRepository(UserRepository):
    def __init__(self, session: AsyncSession):
        self._session = session
        self._current_user: Optional[User] = None

    async def login(self, email: Email, password: Password) -> User:
        stmt = select(UserModel).where(UserModel.email == str(email))
        result = await self._session.execute(stmt)
        user_model = result.scalar_one_or_none()

        if user_model and password.verify(user_model.password):
            self._current_user = user_model.to_entity()
            return self._current_user

        raise ValueError("Credenciais inválidas")

    async def update_password(self, email: Email, password: Password):
        if await self._email_exist(email):
            result = await self._session.execute(
                update(UserModel)
                .where(UserModel.email == email.value())
                .values(password=str(password))
            )
            await self._session.commit()
            return
        raise ValueError("Email não existente")

    async def _email_exist(self, email: Email):
        result = await self._session.execute(
            select(UserModel).where(UserModel.email == email.value())
        )
        return result.scalar_one_or_none() is not None

    async def logout(self) -> None:
        self._current_user = None

    async def get_current_user(self) -> Optional[User]:
        return self._current_user

    async def set_current_user(self, user: User) -> None:
        self._current_user = user

    async def get_by_id(self, user_id: str) -> User:
        result = await self._session.execute(
            select(UserModel).where(UserModel.id == user_id)
        )
        user_model = result.scalar_one_or_none()
        if user_model is None:
            raise ValueError("Usuário não encontrado")
        return user_model.to_entity()
