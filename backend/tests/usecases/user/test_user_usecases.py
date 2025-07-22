import pytest
from unittest.mock import AsyncMock, MagicMock

# Importe as classes das suas pastas de domínio e casos de uso
from mercearia.domain.value_objects.email_vo import Email
from mercearia.domain.value_objects.password_vo import Password, PasswordValidationError # Adicionado PasswordValidationError
from mercearia.domain.entities.user import User
from mercearia.domain.repositories.user_repository import UserRepository # Para o spec do mock

# Importe os casos de uso
from mercearia.usecases.user.login_user import LoginUser
from mercearia.usecases.user.update_password import UpdatePassword


@pytest.fixture
def mock_user_repository() -> AsyncMock:
    """
    Fixture que retorna um mock assíncrono do UserRepository.
    Usamos spec para garantir que o mock tenha os mesmos métodos do repositório real.
    """
    return AsyncMock(spec=UserRepository)

# --- Testes para o Caso de Uso LoginUser ---
class TestLoginUser:
    @pytest.mark.asyncio
    async def test_login_success(self, mock_user_repository: AsyncMock):
        """
        Testa se o caso de uso LoginUser realiza o login com sucesso
        e define o usuário atual no repositório.
        """
        # Arrange
        test_email_str = "admin@merceariaferrari.com"
        test_password_str = "Admin123!" # Adicionei um caractere especial para garantir que passe na validação do Password VO
        
        # Cria um objeto User que o mock do repositório retornaria
        # AGORA COM O ARGUMENTO 'role' E PASSANDO INSTÂNCIAS DE VO
        expected_user = User(
            id="user1",
            name="Miguel Ferrari",
            email=Email(test_email_str),
            # Passa a string da senha para o Password VO, que fará o hash
            password=Password(test_password_str),
            role="admin" # <-- CORREÇÃO: Adicionado o argumento 'role'
        )
        
        # Configura o mock para simular o login bem-sucedido
        # O método login do repositório deve receber VOs, não strings
        mock_user_repository.login.return_value = expected_user
        
        login_usecase = LoginUser(mock_user_repository)

        # Act
        logged_in_user = await login_usecase.execute(test_email_str, test_password_str)

        # Assert
        # Verifica se 'login' foi chamado com os VOs corretos
        # É importante que o mock seja chamado com as instâncias de Email e Password corretas
        mock_user_repository.login.assert_called_once()
        
        # Acessa os argumentos com que o mock foi chamado
        called_args, _ = mock_user_repository.login.call_args
        called_email_vo, called_password_vo = called_args
        
        assert isinstance(called_email_vo, Email)
        assert called_email_vo.value() == test_email_str # Verifica o valor da string do Email VO
        
        assert isinstance(called_password_vo, Password)
        # CORREÇÃO: Se Password VO faz hash, verifique se a senha original pode ser validada
        assert called_password_vo.verify(str(Password(test_password_str))) is True 

        # Verifica se 'set_current_user' foi chamado com o usuário retornado
        mock_user_repository.set_current_user.assert_called_once_with(expected_user)
        
        # Verifica se o usuário retornado pelo caso de uso é o esperado
        assert logged_in_user == expected_user
        assert logged_in_user.name == "Miguel Ferrari"
        assert logged_in_user.role == "admin" # Verifica o role também

    @pytest.mark.asyncio
    async def test_login_failure_invalid_credentials(self, mock_user_repository: AsyncMock):
        """
        Testa se o caso de uso LoginUser levanta um ValueError
        quando as credenciais são inválidas (e o Password VO é válido).
        """
        # Arrange
        test_email_str = "admin@merceariaferrari.com"
        # CORREÇÃO: Use uma senha que passe na validação do Password VO, mas que seja errada
        test_wrong_password_str = "SenhaErrada123!" 
        
        # Configura o mock para levantar ValueError no método 'login' do repositório
        mock_user_repository.login.side_effect = ValueError("Credenciais inválidas")
        
        login_usecase = LoginUser(mock_user_repository)

        # Act & Assert
        with pytest.raises(ValueError, match="Credenciais inválidas"):
            await login_usecase.execute(test_email_str, test_wrong_password_str)

        # Assert
        # Verifica se 'login' foi chamado com os VOs corretos (instanciados a partir das strings)
        mock_user_repository.login.assert_called_once()
        
        called_args, _ = mock_user_repository.login.call_args
        called_email_vo, called_password_vo = called_args
        
        assert isinstance(called_email_vo, Email)
        assert called_email_vo.value() == test_email_str
        assert isinstance(called_password_vo, Password)
        assert called_password_vo.verify(str(Password(test_wrong_password_str))) is True # A senha é válida para o VO, mas o login falha no repositório

        # Verifica que 'set_current_user' NÃO foi chamado, pois o login falhou
        mock_user_repository.set_current_user.assert_not_called()

# --- Testes para o Caso de Uso UpdatePassword ---
class TestUpdatePassword:
    @pytest.mark.asyncio
    async def test_update_password_success(self, mock_user_repository: AsyncMock):
        """
        Testa se o caso de uso UpdatePassword atualiza a senha com sucesso.
        """
        # Arrange
        test_email_str = "admin@merceariaferrari.com"
        new_password_str = "NovaSenha123!" # Adicionado caractere especial
        
        # O mock não precisa retornar nada para update_password, apenas ser chamado
        mock_user_repository.update_password.return_value = None 
        
        update_usecase = UpdatePassword(mock_user_repository)

        # Act
        await update_usecase.execute(test_email_str, new_password_str)

        # Assert
        # Verifica se 'update_password' foi chamado com os VOs corretos
        mock_user_repository.update_password.assert_called_once()
        
        called_args, _ = mock_user_repository.update_password.call_args
        called_email_vo, called_new_password_vo = called_args
        
        # CORREÇÃO: Verificar Email VO
        assert isinstance(called_email_vo, Email)
        assert called_email_vo.value() == test_email_str # <-- CORREÇÃO: Comparando Email VO com a string do email
        
        # CORREÇÃO: Verificar Password VO usando check_password
        assert isinstance(called_new_password_vo, Password)
        assert called_new_password_vo.verify(str(Password(new_password_str))) is True 

    @pytest.mark.asyncio
    async def test_update_password_user_not_found(self, mock_user_repository: AsyncMock):
        """
        Testa se o caso de uso UpdatePassword levanta um ValueError
        quando o usuário não é encontrado para atualização da senha.
        """
        # Arrange
        non_existent_email_str = "naoexiste@example.com"
        new_password_str = "novaSenha123!" # Adicionado caractere especial
        
        # Configura o mock para levantar ValueError no método 'update_password'
        mock_user_repository.update_password.side_effect = ValueError("Usuário não encontrado")
        
        update_usecase = UpdatePassword(mock_user_repository)

        # Act & Assert
        with pytest.raises(ValueError, match="Usuário não encontrado"):
            await update_usecase.execute(non_existent_email_str, new_password_str)

        # Assert
        mock_user_repository.update_password.assert_called_once()
        
        called_args, _ = mock_user_repository.update_password.call_args
        called_email_vo, called_new_password_vo = called_args
        
        # CORREÇÃO: Verificar Email VO
        assert isinstance(called_email_vo, Email)
        assert called_email_vo.value() == non_existent_email_str # <-- CORREÇÃO: Comparando Email VO com a string do email
        
        # CORREÇÃO: Verificar Password VO usando check_password
        assert isinstance(called_new_password_vo, Password)
        assert called_new_password_vo.verify(str(Password(new_password_str))) is True