"""Módulo dedicado aos testes unitários de models/"""

from unittest import mock
import pytest
from mock_alchemy.mocking import UnifiedAlchemyMagicMock

from src.models.sqlite.entities.entity import Entity
from src.models.sqlite.repositories.entity_repository import SqliteEntityRepository
from src.models.sqlite.settings.connection import db_manager

# db_manager.engine_creator()

class MockConnection:
    """
    Classe mockada que será usada nos testes. Ela simula uma
    session com o banco de dados.
    """
    def __init__(self):
        self.session = UnifiedAlchemyMagicMock(
            data=[
                (
                    [mock.call.query(Entity), mock.call.filter(Entity.id == 1)],
                    [Entity(full_name="Maria Silva", balance=200)]
                )
            ]
        )

    def __enter__(self): return self
    def __exit__(self, exc_type, exc, tb): pass

@pytest.mark.skip(reason="Integração direta com o Banco de Dados")
def test_withdraw_real():
    """
    Teste real de saque com um usuário do banco. Como mexe com dados
    reais, coloquei um skip para ele não rodar junto com os demais.
    """
    repository = SqliteEntityRepository(db_manager)
    repository.withdraw(1, 50)

@pytest.mark.skip(reason="Integração direta com o Banco de Dados")
def test_check_balance_real():
    """
    Teste real de verificação de saldo com um usuário do banco. 
    Como mexe com dados reais, coloquei um skip para ele não 
    rodar junto com os demais.
    """
    repository = SqliteEntityRepository(db_manager)
    balance = repository.check_balance(1)

    assert balance == 950

def test_withdraw():
    """Testa se a operação de saque está funcionando."""
    connection = MockConnection()
    repository = SqliteEntityRepository(connection)

    repository.withdraw(1, 50)

    connection.session.query.assert_called_once_with(Entity)
    connection.session.filter.assert_called_once_with(Entity.id == 1)

def test_check_balance():
    """Testa se a operação de verificação de saldo está funcionando."""
    connection = MockConnection()
    repository = SqliteEntityRepository(connection)

    repository.check_balance(1)

    connection.session.query.assert_called_once_with(Entity)
    connection.session.filter.assert_called_once_with(Entity.id == 1)

def test_withdraw_error():
    """
    Testa se quando buscamos um usuário no banco que não existe
    para saque, sobe uma exceção e o rollback é chamado.
    """
    connection = MockConnection()
    repository = SqliteEntityRepository(connection)

    with pytest.raises(Exception):
        repository.withdraw(999, 50)

    connection.session.rollback.assert_called_once()

def test_check_balance_error():
    """
    Testa se quando buscamos um usuário no banco que não existe
    para validação de saldo, sobe uma exceção.
    """
    connection = MockConnection()
    repository = SqliteEntityRepository(connection)

    with pytest.raises(Exception):
        repository.check_balance(999)
