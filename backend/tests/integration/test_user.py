import pytest
from httpx import AsyncClient

@pytest.mark.asyncio
async def test_login_user_successfully(client: AsyncClient):
    response = await client.post(
        "/user/login",  # <- caminho correto com prefixo
        json={
            "email": "admin@merceariaferrari.com",  # conforme populado no main.py
            "password": "Admin@123"                 # senha em texto puro
        }
    )

    assert response.status_code == 200, f"Erro: {response.text}"
    data = response.json()

    assert "access_token" in data
    assert data["token_type"] == "bearer"

    user = data["user"]
    assert user["email"] == "admin@merceariaferrari.com"
    assert user["nome"] == "Miguel Ferrari"
    assert user["tipo"] == "admin"

    import pytest
from httpx import AsyncClient

@pytest.mark.asyncio
async def test_login_user_with_wrong_password(client: AsyncClient):
    response = await client.post(
        "/user/login",  # rota correta com prefixo
        json={
            "email": "admin@merceariaferrari.com",
            "password": "senhaErrada123!"  # senha incorreta de propósito
        }
    )

    assert response.status_code == 401
    data = response.json()
    assert data["detail"] in ["Credenciais inválidas", "Invalid credentials", "Senha inválida", "Usuário ou senha incorretos"]

