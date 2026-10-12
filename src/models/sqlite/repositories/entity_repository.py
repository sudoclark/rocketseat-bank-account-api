"""
Esse módulo é o responsável pela comunicação direta com o banco de dados. Nós usamos a 'session' declarada no arquivo
settings/connection para conversar com o Banco, representado pela classe 'Entity' declarada em entities/entity.
Importante ressaltar que 'Entity' é uma coisa só, representa a conta e o usuário, por isso coloquei todas as funções
no mesmo lugar.
"""

from src.models.interfaces.entity_interface import EntityInterface
from src.models.sqlite.settings.connection import DbConnectionManager
from src.models.sqlite.entities.entity import Entity

class SqliteEntityRepository(EntityInterface):
    """
    Classe responsável pela interação com o Banco de Dados.
    Ela herda de 'Client', ou seja, precisamos implementar
    os métodos withdraw() e check_balance().
    """
    def __init__(self, db_connection: DbConnectionManager):
        self.__db_connection = db_connection

    def create_user(self, monthly_income, age, full_name, phone, email, category, balance):
        with self.__db_connection as database:
            try:
                user = Entity(
                    monthly_income=monthly_income,
                    age=age,
                    full_name=full_name,
                    phone=phone,
                    email=email,
                    category=category,
                    balance=balance
                )

                database.session.add(user)
                database.session.commit()
            except Exception as ex:
                database.session.rollback()
                raise ex

    def list_users(self):
        with self.__db_connection as database:
            users = database.session.query(Entity).all()

            return users

    def get_user(self, user_id):
        with self.__db_connection as database:
            try:
                user = database.session.query(Entity).filter(Entity.id == user_id).first()

                return user
            except Exception as ex:
                raise ex

    def withdraw(self, user_id: int, value: float):
        with self.__db_connection as database:
            try:
                user = database.session.query(Entity).filter(Entity.id == user_id).first()
                user.balance -= value
                database.session.commit()

            except Exception as ex:
                database.session.rollback()
                raise ex

    def check_balance(self, user_id: int):
        with self.__db_connection as database:
            try:
                user = database.session.query(Entity).filter(Entity.id == user_id).first()

                return user.balance
            except Exception as ex:
                raise ex
