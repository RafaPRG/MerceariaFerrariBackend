import pytest
from sqlalchemy.future import select
from mercearia.infra.models.user_model import UserModel

@pytest.mark.asyncio
async def test_login_update_password_and_check_db(client, db_session):
    email = "rafa@gmail.com"
    old_password = "123456@Aa"
    new_password = "NovaSenha@123"

    # 1. Login inicial via endpoint
    response = await client.post("/login", json={"email": email, "password": old_password})
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    token = data["access_token"]

    # 2. Atualizar senha via endpoint
    response = await client.put("/update-password", json={"email": email, "new_password": new_password})
    assert response.status_code == 200
    assert response.json()["message"] == "Senha atualizada com sucesso"

    # 3. Login com a nova senha
    response = await client.post("/login", json={"email": email, "password": new_password})
    assert response.status_code == 200
    assert "access_token" in response.json()

    # 4. Consulta direta no banco para confirmar alteração (exemplo: checar se usuário existe)
    result = await db_session.execute(select(UserModel).where(UserModel.email == email))
    user = result.scalars().first()
    assert user is not None
    assert user.email == email
    # Opcional: se quiser confirmar a senha mudou, precisaria desencriptar/saber a lógica da senha no banco
