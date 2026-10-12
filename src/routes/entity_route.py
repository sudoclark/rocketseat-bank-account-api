"""
Módulo onde centralizamos todas as rotas referentes às entidades,
tanto para criação e listagem dos usuários quanto para verificação
de saldo e realização de saque.
"""

from flask import Blueprint, request, jsonify

from src.models.sqlite.settings.connection import db_manager
from src.models.sqlite.repositories.entity_repository import SqliteEntityRepository
from src.controllers.entity_controller import EntityController
from src.errors.error_handler import handler_error

entity_route_bp = Blueprint("entity_routes", __name__)

# ===== Configuração do controller e do repositório =====

repository = SqliteEntityRepository(db_manager)
controller = EntityController(repository)


# ===== Declaração das rotas =====

@entity_route_bp.route("/entity", methods=["POST"])
def create_user():
    """
    Rota responsável pela criação de um novo usuário. Pega os dados
    enviados pelo usuário na requisição e envia para o controller fazer
    o registro do novo usuário.
    """
    try:
        user_data = request.json
        response = controller.create_user(user_data)

        return jsonify(response), 201
    except Exception as ex:
        error = handler_error(ex)

        return jsonify(error["data"]), error["status_code"]

@entity_route_bp.route("/entity", methods=["GET"])
def get_users():
    """
    Rota responsável pela listagem de todos os usuários da base.
    """
    try:
        users = controller.list_users()

        return users
    except Exception as ex:
        error = handler_error(ex)

        return jsonify(error["data"]), error["status_code"]

@entity_route_bp.route("/entity/withdraw/<int:user_id>", methods=["PATCH"])
def execute_withdraw(user_id):
    """
    Rota responsável pela execução do saque. Recebe um ID e um valor,
    valida as informações e realiza o saque, se possível.
    """
    try:
        request_data = request.json
        value = request_data["value"]

        response = controller.withdraw(user_id, value)

        return jsonify(response)
    except Exception as ex:
        error = handler_error(ex)

        return jsonify(error["data"]), error["status_code"]

@entity_route_bp.route("/entity/balance/<int:user_id>", methods=["GET"])
def get_balance(user_id):
    """
    Rota responsável por buscar o saldo atual de uma conta. Recebe o ID
    de um usuário, que será usado para encontrar o dado no banco.
    """
    try:
        balance = controller.get_balance(user_id)

        return jsonify(balance)
    except Exception as ex:
        error = handler_error(ex)

        return jsonify(error["data"]), error["status_code"]
