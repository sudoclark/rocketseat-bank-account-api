"""Módulo responsável pela criação da engine e da session"""

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

class DbConnectionManager:
    """
    Classe responsável pela criação da engine e da session.
    A engine é responsável pelo gerenciamento das sessions e
    as sessions é onde temos, efetivamente, a comunicação com
    o banco de dados.
    """
    def __init__(self):
        self.__url_connection = "sqlite:///database.db"
        self.__engine = None
        self.session = None

    def engine_creator(self):
        """Criando a nossa engine."""
        self.__engine = create_engine(self.__url_connection)

    def get_engine(self):
        """
        Como o atributo engine é privado, precisamos de um getter
        para usá-lo em outros módulos do projeto.
        """
        return self.__engine

    def __enter__(self):
        session_maker = sessionmaker()
        self.session = session_maker(bind=self.__engine)
        return self

    def __exit__(self, exc_type, exc, tb):
        self.session.close()

db_manager = DbConnectionManager()
