import pytest
from httpx import AsyncClient
import json


@pytest.mark.asyncio
async def test_adicionar_listar_remover_favorito(client: AsyncClient):
    # 1. Login com usuário real
    login = await client.post(
        "/user/login",
        json={"email": "admin@merceariaferrari.com", "password": "Admin@123"},
    )
    assert login.status_code == 200
    token = login.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    # 2. Buscar um produto real pela API
    produtos_resp = await client.get("/produtos/", headers=headers)
    assert produtos_resp.status_code == 200
    produtos = produtos_resp.json()
    assert len(produtos) > 0
    produto_id = produtos[0]["id"]

    # 3. Adicionar o produto como favorito
    add_resp = await client.post(
        "/favoritos/", json={"produto_id": produto_id}, headers=headers
    )
    assert add_resp.status_code == 200, f"Erro ao adicionar favorito: {add_resp.text}"
    assert add_resp.json()["message"] == "Favorito adicionado com sucesso"

    # 4. Listar favoritos e verificar se o produto está presente
    list_resp = await client.get("/favoritos/", headers=headers)
    assert list_resp.status_code == 200
    favoritos = list_resp.json()
    assert any(f["produto"]["id"] == produto_id for f in favoritos)

    # 5. Remover o favorito (usando client.request devido à limitação do delete + body no httpx)
    del_resp = await client.request(
        "DELETE",
        "/favoritos/",
        headers=headers,
        content=json.dumps({"produto_id": produto_id}),
    )
    assert del_resp.status_code == 200
    assert del_resp.json()["message"] == "Favorito removido com sucesso"

    # 6. Verificar que o favorito foi removido
    list_after = await client.get("/favoritos/", headers=headers)
    assert list_after.status_code == 200
    assert all(f["produto"]["id"] != produto_id for f in list_after.json())
