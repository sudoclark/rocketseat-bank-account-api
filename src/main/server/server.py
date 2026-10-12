"""
Módulo responsável pela instanciação de um objeto Flask.
Além disso, também fazemos o registro das rotas.
"""

from flask import Flask

from src.routes.entity_route import entity_route_bp
from src.models.sqlite.settings.connection import db_manager

db_manager.engine_creator()

app = Flask(__name__)

app.register_blueprint(entity_route_bp)
