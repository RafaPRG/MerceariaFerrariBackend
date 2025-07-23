import pytest
from unittest.mock import AsyncMock

# Importe a classe do caso de uso
from mercearia.usecases.produto.get_all_produtos import (
    GetAllProdutos,
)  # Ajustado o path

# Importe a entidade Produto
from mercearia.domain.entities.produto import Produto

# Importe o ProductRepository (para especificação do mock)
from mercearia.domain.repositories.produto_repository import ProdutoRepository


@pytest.fixture
def mock_produto_repository() -> AsyncMock:
    """
    Fixture que retorna um mock assíncrono do ProdutoRepository.
    Usamos spec para garantir que o mock se comporte como o repositório real.
    """
    return AsyncMock(spec=ProdutoRepository)


class TestGetAllProdutos:
    @pytest.mark.asyncio  # Marca o teste como assíncrono
    async def test_execute_returns_all_produtos(
        self, mock_produto_repository: AsyncMock
    ):
        """
        Testa se o caso de uso GetAllProdutos retorna corretamente todos os produtos
        obtidos do repositório.
        """
        # Arrange (Configuração)
        # Cria alguns produtos de exemplo para o mock retornar
        expected_produtos = [
            Produto(
                id="prod1",
                nome="Arroz",
                descricao="Arroz agulhinha 5kg",
                preco=25.00,
                imagem="url1",
            ),
            Produto(
                id="prod2",
                nome="Feijão",
                descricao="Feijão carioca 1kg",
                preco=8.50,
                imagem="url2",
            ),
            Produto(
                id="prod3",
                nome="Leite",
                descricao="Leite integral 1L",
                preco=5.00,
                imagem="url3",
            ),
        ]

        # Configura o mock do repositório para retornar a lista de produtos esperada
        mock_produto_repository.get_all.return_value = expected_produtos

        # Instancia o caso de uso, injetando o mock do repositório
        get_all_produtos_use_case = GetAllProdutos(
            produto_repository=mock_produto_repository
        )

        # Act (Execução)
        # Chama o método execute do caso de uso (agora com await)
        produtos = await get_all_produtos_use_case.execute()

        # Assert (Verificação)
        # Verifica se o método 'get_all' do repositório foi chamado exatamente uma vez
        mock_produto_repository.get_all.assert_called_once()

        # Verifica se o resultado do caso de uso é exatamente a lista que o mock retornou
        assert produtos == expected_produtos

        # Verifica a quantidade de produtos retornados
        assert len(produtos) == len(expected_produtos)

        # Verifica se cada produto na lista tem 'id' e 'nome' (e outros atributos importantes)
        # Embora o '== expected_produtos' já cubra isso se o mock estiver bem definido,
        # adicionar uma verificação explícita pode ser útil para clareza em alguns casos.
        assert all(isinstance(p, Produto) for p in produtos)
        assert all(p.id and p.nome and p.preco for p in produtos)

    @pytest.mark.asyncio
    async def test_execute_returns_empty_list_if_no_produtos(
        self, mock_produto_repository: AsyncMock
    ):
        """
        Testa se o caso de uso GetAllProdutos retorna uma lista vazia
        quando o repositório não tem produtos.
        """
        # Arrange
        mock_produto_repository.get_all.return_value = (
            []
        )  # Repositório retorna lista vazia
        get_all_produtos_use_case = GetAllProdutos(
            produto_repository=mock_produto_repository
        )

        # Act
        produtos = await get_all_produtos_use_case.execute()

        # Assert
        mock_produto_repository.get_all.assert_called_once()
        assert produtos == []
        assert len(produtos) == 0
