from flask import Flask
from flask_restx import Api, Resource 
from .routes.frutas import frutas_ns 
from .routes.auth import auth_ns 

def create_app(script_info=None):
    app = Flask(__name__)
    app.config.from_object("app.config.DevelopmentConfig")
    api = Api(app, title="API de Frutas", version="1.0", description="Una API simple")
    api.add_namespace(frutas_ns)
    api.add_namespace(auth_ns)
    return app
    
