"""
Nesse módulo nós declaramos a interface para quaisquer entidades
que tenhamos no projeto. Consiste em dois métodos, um para saque
de valores e outro para verificação de saldo bancário.
Qualquer entidade criada precisa seguir essas regras.
"""

from abc import ABC, abstractmethod

class EntityInterface(ABC):
    """
    Classe abstrata reasponsável pelo 'contrato' dos repositórios.
    Qualquer repositório que for criado no projeto precisa herdar
    dessa classe e implementar os dois métodos abaixo.
    """

    @abstractmethod
    def withdraw(self, user_id: int, value: float):
        """Método responsável pelo saque, recebe o valor a ser sacado como argumento"""

    @abstractmethod
    def check_balance(self, user_id:int):
        """Método responsável pela verificação do saldo."""
