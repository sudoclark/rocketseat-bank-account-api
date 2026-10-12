"""
Módulo que representa o erro de "Unprocessable Entity", ou seja, quando um dado foi enviado
pelo usuário, mas o sistema não consegue processá-lo devido a alguma inconsistência ou
mal formatação desse dado.
"""

from .base_error import BaseError

class UnprocessableEntityError(BaseError):
    """Classe responsável pelos erros 'Unprocessable Entity'"""
    def __init__(self, message: str, details: dict = None):
        super().__init__(message, status_code=422, type="UnprocessableEntity", details=details)
