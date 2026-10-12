"""
Módulo que representa o erro de "Not Found", ou seja, quando algum dado
não é encontrado no sistema.
"""

from .base_error import BaseError

class NotFoundError(BaseError):
    """Classe responsável pelos erros 'Not Found'"""
    def __init__(self, message: str, details: dict = None):
        super().__init__(message, status_code=404, type="NotFound", details=details)
