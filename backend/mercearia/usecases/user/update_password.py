from mercearia.domain.repositories.user_repository import UserRepository
from mercearia.domain.value_objects.email_vo import Email
from mercearia.domain.value_objects.password_vo import Password
from mercearia.domain.entities.user import User


class UpdatePassword:
    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository

    async def execute(self, email: str, new_password: str) -> None:
        email_vo = Email(email)
        new_password_vo = Password(new_password)

        await self.user_repository.update_password(email_vo, new_password_vo)
