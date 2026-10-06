"""
Módulo onde criamos a classe Python que vai representar
a tabela existente no banco de dados para o SQLAlchemy.
"""

from sqlalchemy import Column, REAL, TEXT, INTEGER

from src.models.sqlite.settings.base import Base

class Entity(Base):
    """
    Classe Python que representa a tabela presente no
    banco de dados. A tabela Entity representa uma conta
    bancária, o tipo (pessoa física ou jurídica) é determinada
    pelo atributo/coluna 'category'.
    """

    __tablename__ = 'entity'

    id = Column(INTEGER, primary_key=True)
    monthly_income = Column(REAL)
    age = Column(INTEGER)
    full_name = Column(TEXT)
    phone = Column(TEXT)
    email = Column(TEXT)
    category = Column(TEXT)
    balance = Column(REAL)
