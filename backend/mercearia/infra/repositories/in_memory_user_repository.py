from mercearia.domain.entities.user import User
from mercearia.domain.value_objects.email_vo import Email
from mercearia.domain.value_objects.password_vo import Password
from mercearia.domain.repositories.user_repository import UserRepository


class InMemoryUserRepository(UserRepository):
    def __init__(self):
        self._users = [
            User(
                "1",
                "Miguel Ferrari",
                Email("admin@merceariaferrari.com"),
                Password("Admin123@"),
                "admin",
            ),
            User(
                "2",
                "Jucelino Freitas",
                Email("jucelinofreitas@gmail.com"),
                Password("Juice123"),
                "user",
            ),
        ]
        self._current_user = None

    async def login(self, email: Email, password: Password) -> User:
        for user in self._users:
            if user.email.value() == email and user.password.value() == password:
                self._current_user = user
                return user
        raise ValueError("Credenciais inválidas")

    async def logout(self) -> None:
        self._current_user = None

    async def get_current_user(self) -> User | None:
        return self._current_user

    async def set_current_user(self, user: User) -> None:
        self._current_user = user
