import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
import sqlalchemy as sa
import uuid

# 1. Importa a aplicação FastAPI principal
# Assume que 'main.py' está na raiz do seu projeto.
from mercearia.api.main import app 

# 2. Importa a dependência que será sobrescrita (para injetar a sessão de teste)
from mercearia.api.deps import get_db_session

# 3. Importa os modelos SQLAlchemy e Base (necessário para criar e manipular tabelas)
from mercearia.infra.models.produto_model import ProdutoModel
from mercearia.infra.models.user_model import UserModel # Incluído para completar Base.metadata.create_all
from mercearia.infra.database import Base # A Base declarativa usada pelos seus modelos

# 4. Importa a função de hash de senha (para popular dados de usuário de teste)
from mercearia.api.security import get_password_hash


# --- Testes de Integração para a Rota /produtos ---

class TestProdutoRoutesIntegration:
    @pytest.mark.asyncio # Opcional se asyncio_mode = auto no pytest.ini, mas bom para clareza
    async def test_listar_produtos_success(self, client: AsyncClient):
   
        headers = {"Authorization": "Bearer faked_valid_jwt_token"} 

        # Act
        response = await client.get("/produtos/", headers=headers)

        # Assert
        assert response.status_code == 200
        response_data = response.json()
        
        assert isinstance(response_data, list)
        assert len(response_data) == 7 # Esperamos os 2 produtos inseridos pela fixture

       
    
    @pytest.mark.asyncio
    async def test_listar_produtos_unauthenticated(self, client: AsyncClient):
        """
        Testa a rota GET /produtos/ sem fornecer um token de autenticação.
        Espera um status 401 Unauthorized, conforme a configuração do FastAPI HTTPBearer.
        """
        # Arrange (não fornece headers de autenticação)

        # Act
        response = await client.get("/produtos/")

        # Assert
        assert response.status_code == 403
        assert "detail" in response.json()
        assert response.json()["detail"] == "Not authenticated" 
        # Esta é a mensagem padrão do FastAPI para HTTPBearer quando nenhuma credencial é fornecida.