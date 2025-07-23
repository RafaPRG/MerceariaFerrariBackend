import pytest
from unittest.mock import AsyncMock, MagicMock

# Importa as classes da sua estrutura de projeto
from mercearia.domain.entities.favorito import Favorito
from mercearia.domain.repositories.favorito_repository import FavoritoRepository

# Importa os casos de uso
# Assumindo que os arquivos são add_favorito.py, get_user_favoritos.py, remove_favorito.py
# e que cada um define a sua classe de caso de uso.
from mercearia.usecases.favorito.add_favorito import AddFavorito
from mercearia.usecases.favorito.get_user_favoritos import GetUserFavoritos
from mercearia.usecases.favorito.remove_favorito import RemoveFavorito


# --- Fixture para o Repositório Mockado ---
# Esta fixture será executada antes de cada teste que a solicitar,
# garantindo um mock "limpo" para cada teste.
@pytest.fixture
def mock_favorito_repository() -> AsyncMock:
    """
    Fixture que retorna um mock assíncrono do FavoritoRepository.
    Usamos spec para garantir que o mock tenha os mesmos métodos do repositório real,
    evitando erros de digitação e garantindo a consistência.
    """
    return AsyncMock(spec=FavoritoRepository)


# --- Testes para o Caso de Uso AddFavorito ---
class TestAddFavorito:
    @pytest.mark.asyncio  # Marca o teste como assíncrono
    async def test_execute_adds_favorito_successfully(
        self, mock_favorito_repository: AsyncMock
    ):
        """
        Testa se o caso de uso AddFavorito adiciona um favorito com sucesso
        e chama o método 'add' do repositório com o objeto Favorito correto.
        """
        # Arrange (Configuração)
        user_id = "user_test_1"
        produto_id = "prod_test_A"

        # Instancia o caso de uso, injetando o mock do repositório
        add_favorito_use_case = AddFavorito(mock_favorito_repository)

        # Act (Execução)
        await add_favorito_use_case.execute(user_id, produto_id)

        # Assert (Verificação)
        # Verifica se o método 'add' do repositório foi chamado exatamente uma vez
        mock_favorito_repository.add.assert_called_once()

        # Obtém o objeto Favorito que foi passado como argumento para 'add'
        # call_args retorna uma tupla (args, kwargs)
        called_favorito: Favorito = mock_favorito_repository.add.call_args[0][0]

        # Verifica se o objeto é uma instância de Favorito e se seus atributos estão corretos
        assert isinstance(called_favorito, Favorito)
        assert called_favorito.user_id == user_id
        assert called_favorito.produto_id == produto_id


# --- Testes para o Caso de Uso GetUserFavoritos ---
class TestGetUserFavoritos:
    @pytest.mark.asyncio
    async def test_execute_returns_user_favoritos_when_exist(
        self, mock_favorito_repository: AsyncMock
    ):
        """
        Testa se o caso de uso GetUserFavoritos retorna a lista correta de favoritos
        para um usuário quando existem favoritos.
        """
        # Arrange
        user_id = "user_test_2"
        # Prepara uma lista de favoritos que o mock do repositório deve retornar
        expected_favoritos = [
            Favorito(user_id=user_id, produto_id="prod_test_B"),
            Favorito(user_id=user_id, produto_id="prod_test_C"),
        ]
        mock_favorito_repository.list_by_user.return_value = expected_favoritos

        get_user_favoritos_use_case = GetUserFavoritos(mock_favorito_repository)

        # Act
        result = await get_user_favoritos_use_case.execute(user_id)

        # Assert
        # Verifica se o método 'list_by_user' do repositório foi chamado com o user_id correto
        mock_favorito_repository.list_by_user.assert_called_once_with(user_id)
        # Verifica se o resultado retornado pelo caso de uso é o esperado
        assert result == expected_favoritos

    @pytest.mark.asyncio
    async def test_execute_returns_empty_list_if_no_favoritos(
        self, mock_favorito_repository: AsyncMock
    ):
        """
        Testa se o caso de uso GetUserFavoritos retorna uma lista vazia
        quando não há favoritos para o usuário.
        """
        # Arrange
        user_id = "user_test_3"
        mock_favorito_repository.list_by_user.return_value = (
            []
        )  # Repositório retorna lista vazia

        get_user_favoritos_use_case = GetUserFavoritos(mock_favorito_repository)

        # Act
        result = await get_user_favoritos_use_case.execute(user_id)

        # Assert
        mock_favorito_repository.list_by_user.assert_called_once_with(user_id)
        assert result == []


# --- Testes para o Caso de Uso RemoveFavorito ---
class TestRemoveFavorito:
    @pytest.mark.asyncio
    async def test_execute_removes_favorito_successfully_if_exists(
        self, mock_favorito_repository: AsyncMock
    ):
        """
        Testa se o caso de uso RemoveFavorito remove um favorito com sucesso
        quando ele já existe.
        """
        # Arrange
        user_id = "user_test_4"
        produto_id = "prod_test_D"

        # Configura o mock para que o método 'exists' retorne True
        mock_favorito_repository.exists.return_value = True
        remove_favorito_use_case = RemoveFavorito(mock_favorito_repository)

        # Act
        await remove_favorito_use_case.execute(user_id, produto_id)

        # Assert
        # Verifica se 'exists' foi chamado para verificar a existência do favorito
        mock_favorito_repository.exists.assert_called_once_with(user_id, produto_id)

        # Verifica se o método 'remove' do repositório foi chamado
        mock_favorito_repository.remove.assert_called_once()

        # Verifica se o Favorito passado para 'remove' está correto
        called_favorito: Favorito = mock_favorito_repository.remove.call_args[0][0]
        assert isinstance(called_favorito, Favorito)
        assert called_favorito.user_id == user_id
        assert called_favorito.produto_id == produto_id

    @pytest.mark.asyncio
    async def test_execute_raises_value_error_if_favorito_not_exists(
        self, mock_favorito_repository: AsyncMock
    ):
        """
        Testa se o caso de uso RemoveFavorito levanta um ValueError
        quando o favorito a ser removido não existe.
        """
        # Arrange
        user_id = "user_test_5"
        produto_id = "prod_test_E"

        # Configura o mock para que o método 'exists' retorne False
        mock_favorito_repository.exists.return_value = False
        remove_favorito_use_case = RemoveFavorito(mock_favorito_repository)

        # Act & Assert
        # Espera que um ValueError seja levantado com a mensagem específica
        with pytest.raises(ValueError, match="Favorito não existente"):
            await remove_favorito_use_case.execute(user_id, produto_id)

        # Assert
        # Verifica se 'exists' foi chamado
        mock_favorito_repository.exists.assert_called_once_with(user_id, produto_id)
        # Verifica que 'remove' NÃO foi chamado, pois o favorito não existe
        mock_favorito_repository.remove.assert_not_called()

    @pytest.mark.asyncio
    async def test_execute_does_nothing_if_favorito_does_not_exist_and_no_exception_expected(
        self, mock_favorito_repository: AsyncMock
    ):
        """
        Um teste adicional para garantir que, se por algum motivo a lógica mudasse
        para não levantar exceção, o 'remove' ainda não seria chamado.
        (Este teste é um pouco redundante com o anterior, mas mostra a flexibilidade).
        """
        # Arrange
        user_id = "user_test_6"
        produto_id = "prod_test_F"
        mock_favorito_repository.exists.return_value = False
        remove_favorito_use_case = RemoveFavorito(mock_favorito_repository)

        # Act
        # Neste caso, não esperamos uma exceção, apenas verificamos o comportamento
        with pytest.raises(
            ValueError
        ):  # Ainda esperamos a exceção conforme o código atual
            await remove_favorito_use_case.execute(user_id, produto_id)

        # Assert
        mock_favorito_repository.exists.assert_called_once_with(user_id, produto_id)
        mock_favorito_repository.remove.assert_not_called()
