"""
Módulo responsável pelas regras de negócio da aplicação. Aqui são feitas
todas as validações de dados necessárias antes das informações serem enviadas
ao repositório.
"""

from src.models.interfaces.entity_interface import EntityInterface
from src.validators.entity_type_enum import EntityType
from src.validators.schemas import DataResponseSchema, ResponseSchema
from src.errors.http_errors.bad_request_error import BadRequestError
from src.errors.http_errors.not_found_error import NotFoundError
from src.errors.http_errors.unprocessable_entity_error import UnprocessableEntityError

class EntityController:
    """
    Controller responsável pela lógica de negócio das contas,
    tanto para pessoa física quanto para jurídica.
    """
    def __init__(self, repository: EntityInterface):
        self.__repository = repository

    def create_user(self, user_data: dict) -> dict:
        """Método para criação de usuários."""
        monthly_income = user_data.get("monthly_income", 0)
        age = user_data.get("age", 0)
        full_name = user_data.get("full_name", "")
        phone = user_data.get("phone", "")
        email = user_data.get("email", "")
        category = user_data.get("category", "")
        balance = user_data.get("balance", 0)

        errors = self.__validate_user_data(age, full_name, email, category)

        if errors:
            raise BadRequestError("Dados inválidos, verifique as informações enviadas")

        self.__insert_user_into_db(monthly_income, age, full_name, phone, email, category, balance)
        response = self.__format_response(count=1, entity_type="User", operation="create_user")

        return response

    def list_users(self) -> list:
        """Método para listagem de usuários."""
        users = self.__repository.list_users()

        if not users:
            raise NotFoundError("Nenhum usuário encontrado")

        users_formatted = [{"full_name": user.full_name, "age": user.age, "email": user.email, "category": user.category} for user in users]
        response = self.__format_response(count=len(users), entity_type="User", operation="list_users", details=users_formatted)

        return response

    def withdraw(self, user_id, value):
        """Método para saque."""
        user = self.__validate_user(user_id)
        self.__validate_withdraw(user, value)
        self.__execute_withdraw(user_id, value)

        return self.__format_response(count=1, entity_type="Withdraw", operation="withdraw")

    def get_balance(self, user_id):
        """Método para verificação do saldo."""
        balance = self.__repository.check_balance(user_id)
        response = self.__format_response(count=1, entity_type="Balance", operation="check_balance", details=balance)

        return response


    # ==============================
    # Comunicação com o Repository
    # ==============================

    def __execute_withdraw(self, user_id, value):
        """Realiza o saque de fato. Conversa diretamente com o repositório"""
        self.__repository.withdraw(user_id, value)

    def __insert_user_into_db(self, monthly_income, age, full_name, phone, email, category, balance) -> None:
        """Realiza a criação de usuário. Conversa diretamente com o repositório"""
        self.__repository.create_user(monthly_income, age, full_name, phone, email, category, balance)


    # ==============================
    # Validações internas
    # ==============================

    def __validate_withdraw(self, user, value):
        """
        Valida se a operação de saque pode ser realizada, leva em consideração:

            1. Se o valor a ser sacado é maior que zero;
            2. Verifica o tipo da conta (física/jurídica), as contas físicas só podem sacar até R$500.
            3. Verifica se o usuário tem valor suficiente na conta para realizar o saque.

        Se qualquer condição não for atendida, levanta uma exceção.
        """
        if value <= 0:
            raise BadRequestError("Valor de saque não pode ser menor ou igual a zero.")

        if value > 500:
            if user.category == EntityType.INDIVIDUAL:
                raise UnprocessableEntityError("Sua conta é pessoa física, você só pode sacar até R$500.")

        if value > user.balance:
            raise UnprocessableEntityError("Saldo insuficiente.")

    def __validate_user(self, user_id):
        """
        Valida se o usuário existe no banco de dados. Não tem como você sacar dinheiro de
        uma conta que não existe.
        """
        user = self.__repository.get_user(user_id)

        if not user:
            raise NotFoundError("Nenhum usuário encontrado com o ID informado.")

        return user

    def __validate_user_data(self, age, full_name, email, category) -> list:
        """
        Valida se os dados enviados pelo usuário são válidos, leva em consideração:

            1. Se tem algum caractere no 'full_name' que seja número ou espaço.
            2. Se a pessoa tem, no mínimo, 16 anos.
            3. Se existe um arroba no e-mail (precisa ter para ser válido).
            4. Se a categoria enviada pelo usuário bate com as duas possíveis (individual ou legal).
        
        Se qualquer condição não for atendida, o método vai acumulando os erros em uma lista e envia todos
        de uma vez só para o usuário. Assim se mais de um erro for encontrado ele pode cosnertar todos de uma
        vez só.
        """
        errors = []
        valid_names = full_name.split()

        for name in valid_names:
            if not name.isalpha():
                errors.append({"field": "full_name", "error": "Nome inválido, somente letras e acentos são válidos"})

        if age < 16:
            errors.append({"field": "age", "erro": "Você precisa ter 16 ou mais anos para criar uma conta"})

        if "@" not in email:
            errors.append({"field": "email", "error": "E-mail inválido, verifique as informações enviadas"})

        if category not in EntityType:
            errors.append({"field": "category", "error": "Categoria inválida, uma conta só pode ser 'individual' (física) ou 'legal' (jurídica)"})

        return errors


    # ==============================
    # Formatação de resposta
    # ==============================

    def __format_response(self, count, entity_type, operation, details=None) -> DataResponseSchema:
        """Formata a resposta que será enviada para o usuário."""
        return DataResponseSchema(
            data=ResponseSchema(
                count=count,
                entity_type=entity_type,
                operation=operation,
                details=details
            )
        )
