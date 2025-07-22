import pytest
from mercearia.domain.value_objects.email_vo import Email
from mercearia.domain.value_objects.password_vo import Password, PasswordValidationError


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



def test_invalid_password_short():
    with pytest.raises(PasswordValidationError):
        Password("abc123")


def test_invalid_password_only_letters():
    with pytest.raises(PasswordValidationError):
        Password("abcdefgh")


def test_invalid_password_only_numbers():
    with pytest.raises(PasswordValidationError):
        Password("12345678")


def test_password_equality():
    assert Password("Abc@12345").verify(str(Password("Abc@12345")))
    assert not Password("Abc@12345").verify(str(Password("Syz@98765")))
