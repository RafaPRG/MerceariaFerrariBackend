from mercearia.domain.value_objects.email_vo import Email
from mercearia.domain.value_objects.password_vo import Password


class User:
    def __init__(self, id: str, name: str, email: Email, password: Password, role: str):
        if role not in ["admin", "user"]:
            raise ValueError("Role must be 'admin' or 'user'.")
        self.id = id
        self.name = name
        self.email = email
        self.password = password
        self.role = role
