from site.domain.entities.user import User
from site.domain.value_objects.email_vo import Email
from site.domain.value_objects.password_vo import Password
from site.domain.repositories.user_repository import UserRepository

class InMemoryUserRepository(UserRepository):
    def __init__(self):
        self._users = [
            User("1", "Miguel Ferrari", Email("admin@merceariaferrari.com"), Password("admin123"), "admin"),
            User("2", "Jucelino Freitas", Email("jucelinofreitas@gmail.com"), Password("juce123"), "user")
        ]
        self._current_user = None

    def login(self, email: str, password: str) -> User:
        for user in self._users:
            if user.email.value() == email and user.password.value() == password:
                self._current_user = user
                return user
        raise ValueError("Credenciais inválidas")

    def logout(self) -> None:
        self._current_user = None

    def get_current_user(self) -> User | None:
        return self._current_user

    def set_current_user(self, user: User) -> None:
        self._current_user = user
