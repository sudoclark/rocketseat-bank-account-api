"""
Módulo que representa o erro de "Bad Request", ou seja, quando o usuário
envia um dado incorreto ou mal-formatado para a API.
"""

from .base_error import BaseError

class BadRequestError(BaseError):
    """Classe responsável pelos erros 'Bad Request'"""
    def __init__(self, message: str):
        super().__init__(message, status_code=400, type="BadRequest")
