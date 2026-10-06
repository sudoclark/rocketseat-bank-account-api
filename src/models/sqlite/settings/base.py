"""
Módulo responsável pela 'base declarativa'. Essa ferramenta
indica ao SQLAlchemy que uma classe no python não é uma classe
comum e sim uma representação de uma tabela do banco de dados.
"""

from sqlalchemy.orm import declarative_base

Base = declarative_base()
