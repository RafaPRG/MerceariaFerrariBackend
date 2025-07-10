from mercearia.domain.repositories.user_repository import UserRepository
from mercearia.domain.value_objects.email_vo import Email
from mercearia.domain.value_objects.password_vo import Password
from mercearia.domain.entities.user import User

class UpdatePassword:
    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository

    def execute(self, email: str, new_password: str) -> None:
        email_vo = Email(email)
        new_password_vo = Password(new_password)

        user: User | None = self.user_repository.get_current_user()
        if user is None or user.email != email_vo:
            raise ValueError("Usuário não encontrado.")

        user.password = new_password_vo
