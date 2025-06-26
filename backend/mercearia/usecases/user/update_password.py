from mercearia.domain.repositories.user_repository import UserRepository
from mercearia.domain.value_objects.email_vo import Email
from mercearia.domain.value_objects.password_vo import Password

class UpdatePassword:
    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository

    def execute(self, email: str, new_password: str) -> None:
        email_vo = Email(email)
        new_password_vo = Password(new_password)

        user = None
        for u in self.user_repository._users:
            if u.email.value() == email_vo.value():
                user = u
                break

        if user is None:
            raise ValueError("Usuário não encontrado.")

        user.password = new_password_vo
