import pytest
from mercearia.domain.value_objects.email_vo import Email
from mercearia.domain.value_objects.password_vo import Password

def test_valid_email():
    email = Email("teste@example.com")
    assert email.value() == "teste@example.com"
    assert str(email) == "teste@example.com"

def test_invalid_email_raises():
    with pytest.raises(ValueError):
        Email("invalido.com")

def test_email_equality():
    assert Email("a@b.com") == Email("a@b.com")
    assert Email("a@b.com") != Email("b@a.com")

def test_valid_password():
    senha = Password("abc12345")
    assert senha.value() == "abc12345"
    assert str(senha) == "*" * 8

def test_invalid_password_short():
    with pytest.raises(ValueError):
        Password("abc123")

def test_invalid_password_only_letters():
    with pytest.raises(ValueError):
        Password("abcdefgh")

def test_invalid_password_only_numbers():
    with pytest.raises(ValueError):
        Password("12345678")

def test_password_equality():
    assert Password("abc12345") == Password("abc12345")
    assert Password("abc12345") != Password("xyz98765")