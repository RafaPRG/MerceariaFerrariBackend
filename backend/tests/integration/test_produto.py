import pytest
from httpx import AsyncClient

@pytest.mark.asyncio
async def test_listar_produtos_authenticated(client: AsyncClient):
    # Login com usuário real
    login = await client.post("/user/login", json={
        "email": "admin@merceariaferrari.com",
        "password": "Admin@123"
    })
    assert login.status_code == 200
    token = login.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    # Listar produtos
    response = await client.get("/produtos/", headers=headers)
    assert response.status_code == 200

    produtos = response.json()
    assert isinstance(produtos, list)
    assert len(produtos) >= 1  # sabemos que o main.py insere 7, mas podemos deixar flexível
    assert "nome" in produtos[0]
    assert "preco" in produtos[0]
    assert "descricao" in produtos[0]


@pytest.mark.asyncio
async def test_listar_produtos_unauthenticated(client: AsyncClient):
    """
    Testa a rota GET /produtos/ sem fornecer token.
    Espera um status 403 Forbidden, que é o comportamento padrão do HTTPBearer.
    """
    response = await client.get("/produtos/")

    assert response.status_code == 403
    assert "detail" in response.json()
    assert response.json()["detail"] == "Not authenticated"
