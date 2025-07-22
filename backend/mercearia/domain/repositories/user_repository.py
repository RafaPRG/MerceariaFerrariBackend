from abc import ABC, abstractmethod
from mercearia.domain.entities.user import User
from mercearia.domain.value_objects.email_vo import Email
from mercearia.domain.value_objects.password_vo import Password


class UserRepository(ABC):
    @abstractmethod
    async def login(self, email: Email, password: Password) -> User: ...

    @abstractmethod
    async def logout(self) -> None: ...

    @abstractmethod
    async def get_current_user(self) -> User | None: ...

    @abstractmethod
    async def set_current_user(self, user: User) -> None: ...

    @abstractmethod
    async def update_password(self, email:Email, password:Password): ...

    @abstractmethod
    async def get_by_id(self, user_id: str) -> User|None:
        pass