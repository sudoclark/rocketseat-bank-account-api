"""
Módulo responsável pelos testes do controller. Valida todos os métodos
usando um repositório mockado como referência.
"""
import pytest

from src.controllers.entity_controller import EntityController
from src.models.sqlite.entities.entity import Entity
from src.errors.http_errors.not_found_error import NotFoundError
from src.errors.http_errors.bad_request_error import BadRequestError
from src.errors.http_errors.unprocessable_entity_error import UnprocessableEntityError

INDIVIDUAL_USER = Entity(id=2, monthly_income=200, age=27, full_name="John Doe", phone="21912345678", email="john.doe@email.com", category="individual", balance=400)
LEGAL_USER = Entity(id=10, monthly_income=300, age=42, full_name="Maria Silva", phone="21912345678", email="maria.silva@email.com", category="legal", balance=800)

class MockRepository:
    """Classe mockada que simula o repositório de Entity"""
    def create_user(self, monthly_income, age, full_name, phone, email, category, balance):
        """Mock de create_user do repositório"""

    def list_users(self):
        """Mock de list_users do repositório"""
        return [INDIVIDUAL_USER, LEGAL_USER]

    def get_user(self, user_id):
        """Mock de get_users do repositório"""
        return INDIVIDUAL_USER

    def withdraw(self, user_id, value):
        """Mock de withdraw do repositório"""

    def check_balance(self, user_id):
        """Mock de check_balance do repositório"""
        return 500

class MockRepositoryError:
    """
    Classe mockada para auxiliar nos testes dos 'caminhos tristes',
    ou seja, com erros.
    """
    def list_users(self):
        """Mock do 'list_users' para testes de erro"""
        return []

    def get_user(self, user_id):
        """Mock do 'get_user' para testes de erro"""
        return None

    def withdraw(self, user_id, value):
        """Mock do 'withdraw' para testes de erro"""

def test_controller_create_user():
    """
    Teste do controller de 'create_user'. Recebe informações do usuário,
    faz as validações necessárias e retorna uma resposta formatada.
    Usa um mock do repositório para não termos contato com o banco de verdade.
    """
    user_data = {
        "monthly_income": 2000,
        "age": 37,
        "full_name": "João Lopes",
        "phone": "21912345678",
        "email": "joao.lopes@email.com",
        "category": "individual",
        "balance": 4000
    }

    mock_repository = MockRepository()
    controller = EntityController(mock_repository)
    response = controller.create_user(user_data)

    assert "data" in response
    assert response["data"]["count"] == 1
    assert response["data"]["entity_type"] == "User"
    assert response["data"]["operation"] == "create_user"

def test_controller_list_user():
    """
    Teste do controller de 'list_users'. Recebe a requisição do usuário,
    vai no banco e busca a listagem de todos os usuários.
    Usa um mock para não termos acesso ao banco real.
    """
    mock_repository = MockRepository()
    controller = EntityController(mock_repository)
    response = controller.list_users()

    assert "data" in response
    assert response["data"]["entity_type"] == "User"
    assert response["data"]["operation"] == "list_users"
    assert response["data"]["count"] == 2

def test_controller_withdraw():
    """
    Teste do controller de 'withdraw'. Recebe um ID de usuário e
    um valor na requisição. Busca a conta, valida se é possível
    realizar o saque e faz a ação no saldo do usuário.
    Usa um mock para não termos acesso ao banco real.
    """
    mock_repository = MockRepository()
    controller = EntityController(mock_repository)
    response = controller.withdraw(2, 200)

    assert "data" in response
    assert response["data"]["entity_type"] == "Withdraw"
    assert response["data"]["operation"] == "withdraw"
    assert response["data"]["count"] == 1

def test_controller_get_balance():
    """
    Teste do controller de 'get_balance'. Recebe um ID de usuário e
    busca esse registro no Banco. Retorna o valor disponível de saldo.
    Usa um mock para não termos acesso ao banco real.
    """
    mock_repository = MockRepository()
    controller = EntityController(mock_repository)
    response = controller.get_balance(2)

    assert "data" in response
    assert response["data"]["entity_type"] == "Balance"
    assert response["data"]["operation"] == "check_balance"
    assert response["data"]["count"] == 1
    assert response["data"]["details"] == 500

def test_create_user_with_data_error():
    """
    Teste de erro do 'create_user'. Quando a validação dos dados
    que o usuário enviou não batem com as regras, é levantada uma
    exceção de 'BadRequest'.

    Regras:
        - Não podemos ter números no nome
        - O '@' no e-mail é obrigatório
        - A categoria só pode ser 'individual' ou 'legal'
    """
    user_data = {
        "monthly_income": 2000,
        "age": 37,
        "full_name": "João Lopes123",
        "phone": "21912345678",
        "email": "joao.lopesemail.com",
        "category": "batata",
        "balance": 4000
    }

    mock_repository = MockRepository()
    controller = EntityController(mock_repository)

    with pytest.raises(BadRequestError):
        controller.create_user(user_data)

def test_list_users_not_found_error():
    """
    Teste que valida o erro quando nenhum usuário é encontrado
    no sistema quando chamamos o 'list_users'.
    O controller precisa levatar um 'NotFoundError'.
    """
    mock_repository = MockRepositoryError()
    controller = EntityController(mock_repository)

    with pytest.raises(NotFoundError):
        controller.list_users()

def test_withdraw_user_not_found_error():
    """
    Quando fazemos um 'withdraw', internamente ele procura o
    usuário no sistema primeiro, se não achar levanta um 'NotFoundError'.
    Esse teste valida esse caminho.
    """
    mock_repository = MockRepositoryError()
    controller = EntityController(mock_repository)

    with pytest.raises(NotFoundError):
        controller.withdraw(1, 100)

def test_withdraw_amount_minor_than_zero():
    """
    O usuário não pode sacar um valor que seja menor ou igual a zero.
    Teste que valida esse caminho.
    """
    mock_repository = MockRepository()
    controller = EntityController(mock_repository)

    with pytest.raises(BadRequestError):
        controller.withdraw(1, 0)

def test_withdraw_individual_account_can_only_withdraw_a_value_under_500():
    """
    Contas físicas (individual) só podem sacar um valor até R$500.
    Esse teste valida esse caminho.
    """
    mock_repository = MockRepository()
    controller = EntityController(mock_repository)

    with pytest.raises(UnprocessableEntityError):
        controller.withdraw(1, 900)
