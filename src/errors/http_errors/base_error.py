"""
Esse módulo contém a classe base de erros do código. Ela será usada
para tratamento de erros da API.
"""

class BaseError(Exception):
    """Classe base para tratamento de erros."""
    def __init__(self, message: str, status_code: int, type: str):
        super().__init__(message)
        self.status_code = status_code
        self.type = type
        self.message = message
