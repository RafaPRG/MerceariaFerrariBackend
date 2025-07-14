import pytest
from mercearia.domain.entities.user import User
from mercearia.domain.entities.produto import Produto
from mercearia.domain.entities.favorito import Favorito
from mercearia.domain.value_objects.email_vo import Email
from mercearia.domain.value_objects.password_vo import Password

# ---------- User ----------


def test_create_valid_user():
    email = Email("user@example.com")
    password = Password("senha123")
    user = User(id="1", name="João", email=email, password=password, role="user")

    assert user.id == "1"
    assert user.name == "João"
    assert user.email == email
    assert user.password == password
    assert user.role == "user"


def test_create_user_invalid_role():
    email = Email("user@example.com")
    password = Password("senha123")
    with pytest.raises(ValueError):
        User(id="1", name="João", email=email, password=password, role="guest")


# ---------- Produto ----------


def test_create_produto():
    produto = Produto(
        id="10", nome="Arroz", descricao="Arroz tipo 1", preco=5.99, imagem="arroz.jpg"
    )

    assert produto.id == "10"
    assert produto.nome == "Arroz"
    assert produto.descricao == "Arroz tipo 1"
    assert produto.preco == 5.99
    assert produto.imagem == "arroz.jpg"


# ---------- Favorito ----------


def test_create_favorito_and_compare():
    f1 = Favorito(user_id="1", produto_id="10")
    f2 = Favorito(user_id="1", produto_id="10")
    f3 = Favorito(user_id="1", produto_id="99")

    assert f1 == f2
    assert f1 != f3
    assert hash(f1) == hash(f2)
