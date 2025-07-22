import pytest
from httpx import AsyncClient
import pytest_asyncio
from sqlalchemy.ext.asyncio import AsyncSession
from mercearia.domain.entities.user import User # Assumindo a entidade User
from mercearia.domain.entities.produto import Produto # Assumindo a entidade Produto
from mercearia.domain.entities.favorito import Favorito # Assumindo a entidade Favorito
from mercearia.api.main import app # Importa seu app FastAPI principal
from mercearia.api import deps # Módulo de dependências para overrides

# Fixture para gerar um token JWT válido para testes (MOCK SIMPLIFICADO)
# Em um cenário real, você teria uma rota de login ou uma função para gerar um token de teste
@pytest_asyncio.fixture(scope="function")
async def mock_token():
    # Este é um token de exemplo. Em um cenário real, geraria um token JWT válido
    # para um usuário de teste específico.
    # Para este teste, vamos mockar get_current_user para aceitar qualquer token
    # ou para nem mesmo verificar o token, apenas retornar um usuário.
    return "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIiwiaWF0IjoxNTE2MjM5MDIyfQ.SflKxwRJSMeKKF2QT4fwpMeJf36POk6yJV_adQssw5c"


# Fixture para criar um usuário e um produto no banco de dados de teste
# e mockar o get_current_user para usar este usuário
@pytest_asyncio.fixture(scope="function")
async def setup_user_and_product(db_session: AsyncSession):
    # 1. Crie um usuário de teste
    test_user = User(
        id=1, # ID fixo para o teste
        username="testuser_favorito",
        email="test_favorito@example.com",
        password="hashed_password" # Em um teste real, usaria um hashed password
    )
    db_session.add(test_user)
    await db_session.commit()
    await db_session.refresh(test_user) # Recarrega para ter certeza que o ID foi atribuído pelo DB

    # 2. Crie um produto de teste
    test_product = Produto(
        id=101, # ID fixo para o teste
        nome="Produto Teste Favorito",
        descricao="Descricao do produto para teste de favorito",
        preco=99.99
    )
    db_session.add(test_product)
    await db_session.commit()
    await db_session.refresh(test_product) # Recarrega para ter certeza que o ID foi atribuído pelo DB

    # 3. Sobrescreva a dependência get_current_user para retornar nosso usuário de teste
    # Isso evita a necessidade de um token JWT real ou de ter que fazer login
    async def override_get_current_user():
        return test_user

    app.dependency_overrides[deps.get_current_user] = override_get_current_user

    yield test_user, test_product # Retorna o usuário e o produto criados

    # Limpar overrides após o teste
    app.dependency_overrides.pop(deps.get_current_user, None)


# Testes de Integração para as rotas de Favoritos

@pytest.mark.asyncio
async def test_adicionar_favorito(client: AsyncClient, setup_user_and_product, mock_token: str):
    user, product = setup_user_and_product

    # Realiza a requisição POST para adicionar um favorito
    response = await client.post(
        "/favoritos/", # A rota é "/favoritos/" se você não adicionou um prefixo no APIRouter
        headers={"Authorization": mock_token},
        json={"produto_id": product.id}
    )

    # Verifica o status code
    assert response.status_code == 200 # ou 201 se a rota retornar 201

    # Verifica a mensagem de sucesso
    assert response.json() == {"message": "Favorito adicionado com sucesso"}

    # Opcional: Verifica diretamente no banco de dados
    # Você precisaria de acesso à sessão do db_session para isso, ou injetá-la aqui
    # Alternativamente, o próximo teste de listar favoritos validará a adição

@pytest.mark.asyncio
async def test_listar_favoritos(client: AsyncClient, setup_user_and_product, mock_token: str):
    user, product = setup_user_and_product

    # Primeiro, garanta que há um favorito para listar
    # (poderia ser uma fixture separada que cria um favorito, ou confiamos no teste anterior)
    # Para independência, é melhor que cada teste configure seus próprios dados.
    # Vamos adicionar um favorito aqui para garantir que esteja presente.
    response_add = await client.post(
        "/favoritos/",
        headers={"Authorization": mock_token},
        json={"produto_id": product.id}
    )
    assert response_add.status_code == 200 # ou 201

    # Agora, liste os favoritos
    response_list = await client.get(
        "/favoritos/",
        headers={"Authorization": mock_token}
    )

    assert response_list.status_code == 200
    favoritos_list = response_list.json()

    # Verifica se a lista não está vazia e se o produto adicionado está nela
    assert len(favoritos_list) > 0
    assert any(fav["produto"]["id"] == product.id for fav in favoritos_list)
    assert any(fav["user_id"] == user.id for fav in favoritos_list)


@pytest.mark.asyncio
async def test_remover_favorito(client: AsyncClient, setup_user_and_product, mock_token: str):
    user, product = setup_user_and_product

    # Primeiro, adicione o favorito para poder removê-lo
    response_add = await client.post(
        "/favoritos/",
        headers={"Authorization": mock_token},
        json={"produto_id": product.id}
    )
    assert response_add.status_code == 200 # ou 201

    # Agora, remova o favorito
    response_remove = await client.delete(
        "/favoritos/",
        headers={"Authorization": mock_token},
        json={"produto_id": product.id}
    )

    assert response_remove.status_code == 200
    assert response_remove.json() == {"message": "Favorito removido com sucesso"}

    # Opcional: Verifique se o favorito realmente foi removido listando novamente
    response_list_after_remove = await client.get(
        "/favoritos/",
        headers={"Authorization": mock_token}
    )
    assert response_list_after_remove.status_code == 200
    favoritos_list_after_remove = response_list_after_remove.json()
    assert not any(fav["produto"]["id"] == product.id for fav in favoritos_list_after_remove)


@pytest.mark.asyncio
async def test_adicionar_favorito_produto_inexistente(client: AsyncClient, setup_user_and_product, mock_token: str):
    user, _ = setup_user_and_product
    non_existent_product_id = 99999 # Um ID que certamente não existe

    response = await client.post(
        "/favoritos/",
        headers={"Authorization": mock_token},
        json={"produto_id": non_existent_product_id}
    )
    assert response.status_code == 400 # Esperamos 400 se o usecase levantar HTTPException
    assert "Produto não encontrado" in response.json().get("detail", "") or \
           "Produto com ID" in response.json().get("detail", "") # Ajuste a mensagem de erro conforme sua exceção

@pytest.mark.asyncio
async def test_remover_favorito_inexistente(client: AsyncClient, setup_user_and_product, mock_token: str):
    user, product = setup_user_and_product

    # Tenta remover um favorito que não foi adicionado ou com um ID de produto inexistente
    non_existent_product_id = 99999

    response = await client.delete(
        "/favoritos/",
        headers={"Authorization": mock_token},
        json={"produto_id": non_existent_product_id}
    )
    assert response.status_code == 400 # Esperamos 400 se o usecase levantar HTTPException
    assert "Favorito não encontrado" in response.json().get("detail", "") or \
           "Favorito com ID de produto" in response.json().get("detail", "") # Ajuste a mensagem de erro conforme sua exceção