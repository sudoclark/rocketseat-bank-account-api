"""
Módulo responsável pelo tratamento dos erros. Ele recebe um erro qualquer
e valida se é um dos tipos personalizados, se sim, a resposta também é
personalizada. Se não for, também retorna uma mensagem amigável para o usuário.
"""

from .http_errors.base_error import BaseError

def handler_error(error: Exception) -> dict:
    """
    Método de tratamento de erros, recebe um erro e valida se é do tipo personalizado.
    Sendo ou não, retorna uma mensagem mais amigável do que o traceback original.
    """
    if isinstance(error, BaseError):
        return({
            "status_code": error.status_code,
            "details": [{
                "title": error.type,
                "message": error.message
            }]
        })

    return({
        "status_code": 500,
        "details": [{
            "title": "Server Error",
            "message": str(error)
        }]
    })
