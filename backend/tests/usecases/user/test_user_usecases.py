import pytest
from site.domain.value_objects.email_vo import Email
from site.domain.value_objects.password_vo import Password
from site.domain.entities.user import User
from site.infra.repositories.in_memory_user_repository import InMemoryUserRepository
from site.usecases.user.login_user import LoginUser
from site.usecases.user.update_password import UpdatePassword

@pytest.fixture
def user_repository():
    return InMemoryUserRepository()

def test_login_success(user_repository):
    login_usecase = LoginUser(user_repository)
    user = login_usecase.execute("alice@example.com", "senha1234")
    assert user.name == "Alice"
    assert user_repository.get_current_user() == user

def test_login_failure(user_repository):
    login_usecase = LoginUser(user_repository)
    with pytest.raises(ValueError):
        login_usecase.execute("alice@example.com", "senhaErrada")

def test_update_password_success(user_repository):
    update_usecase = UpdatePassword(user_repository)
    update_usecase.execute("alice@example.com", "novaSenha123")

    login_usecase = LoginUser(user_repository)
    user = login_usecase.execute("alice@example.com", "novaSenha123")
    assert user.name == "Alice"

def test_update_password_user_not_found(user_repository):
    update_usecase = UpdatePassword(user_repository)
    with pytest.raises(ValueError):
        update_usecase.execute("naoexiste@example.com", "novaSenha123")
