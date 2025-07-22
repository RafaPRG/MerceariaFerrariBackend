from mercearia.domain.repositories.user_repository import UserRepository
from mercearia.domain.value_objects.email_vo import Email
from mercearia.domain.value_objects.password_vo import Password
from mercearia.domain.entities.user import User


class LoginUser:
    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository

    async def execute(self, email: str, password: str) -> User:
        email_vo = Email(email)
        password_vo = Password(password)

        user = await self.user_repository.login(email_vo, password_vo)

        await self.user_repository.set_current_user(user)

        return user
