import os
import warnings
from flask import Flask, render_template, jsonify

from flask_smorest import Api
from flask_cors import CORS

from marshmallow import ValidationError
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from werkzeug.exceptions import HTTPException

from utils.exception_utils import *

from flask_migrate import Migrate
from flask_jwt_extended import JWTManager
from models import db

from views.auth_routes import blp as AuthBlueprint
from views.user_routes import blp as UserBlueprint
from views.post_routes import blp as PostBlueprint
from views.comment_routes import blp as CommentBlueprint
from views.category_routes import blp as CategoryBlueprint
from views.stats_routes import blp as StatsBlueprint

app = Flask(__name__)

# --- Inicialización de CORS ---
# Para poder hacer las peticiones desde react en local
CORS(app,
     origins="*",  
     supports_credentials=True,
     allow_headers=["Content-Type", "Authorization"],
     expose_headers=["Authorization"])
# -----------------------------

# --- Configuración del Modo Debug (Seguridad) ---
app.config['DEBUG_MODE'] = os.getenv('DEBUG_MODE', 'False').lower() in ('true', '1', 't')
app.debug = app.config['DEBUG_MODE'] # Activa el modo debug de Flask
if app.config['DEBUG_MODE']:
    warnings.warn(
        "DEBUG_MODE IS ACTIVE: Flask will show detailed errors and full stack traces.",
        UserWarning
        )
# -----------------------------------------------

app.secret_key = "cualquiercosa"

# --- Conexión a la Base de Datos SQL ---
DB_USER = os.getenv("DB_USER","root")
DB_PASSWORD = os.getenv("DB_PASSWORD","")
DB_SERVER = os.getenv("DB_SERVER","localhost")
DB_PORT = os.getenv("DB_PORT","3306")
DB_NAME = os.getenv("DB_NAME","db_miniblog")

DATABASE_URL = f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_SERVER}:{DB_PORT}/{DB_NAME}"

app.config['SQLALCHEMY_DATABASE_URI'] = (DATABASE_URL)

app.config['JWT_SECRET_KEY'] = 'cualquier-cosa'

app.config["API_TITLE"] = "MiniBlog API"
app.config["API_VERSION"] = "v1"
app.config["OPENAPI_VERSION"] = "3.0.3"
app.config["OPENAPI_URL_PREFIX"] = "/api/docs"
app.config["OPENAPI_SWAGGER_UI_PATH"] = "/swagger"
app.config["OPENAPI_SWAGGER_UI_URL"] = "https://cdn.jsdelivr.net/npm/swagger-ui-dist/"

app.config["OPENAPI_COMPONENTS"] = {
    "securitySchemes": {
        "BearerAuth": {
            "type": "http",
            "scheme": "bearer",
            "bearerFormat": "JWT"
        }
    }
}

app.config["OPENAPI_JWT_SECURITY_NAME"] = "BearerAuth"

api = Api(app)

api.spec.components.security_scheme(
    "BearerAuth", {"type": "http", "scheme": "bearer", "bearerFormat": "JWT"}
)
api.spec.options["security"] = [{"BearerAuth": []}]

jwt = JWTManager(app)

db.init_app(app)
migrate = Migrate(app, db)

# Error codes
# 400 - Invalid Request
# 401 - Unauthorized
# 403 - Forbidden
# 404 - Not Found
# 409 - Conflict

# -- Custom handlers --

@app.errorhandler(ValidationError)
def handle_validation_error(err):
    return jsonify({"error":"Invalid Request", "details":err.messages}), 400

@app.errorhandler(ForbiddenError)
def handle_permission_error(err):
    return jsonify({"error":str(err)}), 403

@app.errorhandler(NotFoundError)
def handle_not_found_error(err):
    return jsonify({"error":str(err)}), 404

@app.errorhandler(AuthError)
def handle_auth_error(err):
    return jsonify({"error":str(err)}), 401

@app.errorhandler(InactiveUserError)
def handle_inactive_user_error(err):
    return jsonify({"error":str(err)}), 403

@app.errorhandler(RegisterError)
def handle_register_error(err):
    return jsonify({"error":str(err)}), 400

@app.errorhandler(UpdateError)
def handle_updates_error(err):
    return jsonify({"error":str(err)}), 400

@app.errorhandler(DeleteError)
def handle_delete_error(err):
    return jsonify({"error":str(err)}), 400

@app.errorhandler(ConflictError)
def handle_conflict_error(err):
    return jsonify({"error":str(err)}), 409

# -- Error handlers using SQLAlchemy exceptions. --

@app.errorhandler(IntegrityError)
def handle_integrity_error(err):
    if app.config['DEBUG_MODE']:
        error_message = str(err)
    else:
        error_message = "Data constraint violation. Ensure that the entered data is valid."
        
    return jsonify({"error":error_message}), 400

@app.errorhandler(SQLAlchemyError)
def handle_database_error(err):
 
    if app.config['DEBUG_MODE']:

        error_message = str(err)
    else:

        error_message = "An unexpected database error has occurred."

    return jsonify({"error":error_message}), 500

# -- Manejador general para todos los errores --
# (Al estar al final de los manejadores, solo va a usarse cuando
# la app no pueda captar el error con ninguno de los manejadores anteriores.)

@app.errorhandler(Exception)
def handle_general_exception(err):
     
    if isinstance(err, HTTPException):
        return jsonify({"error": err.description, "code": err.code}), err.code


    if app.config['DEBUG_MODE']:

        error_message = str(err)
    else:

        error_message = "An unexpected internal server error has occurred."

    return jsonify({"error":error_message}), 500


# --- API ROUTES ---

api.register_blueprint(AuthBlueprint)
api.register_blueprint(UserBlueprint)
api.register_blueprint(PostBlueprint)
api.register_blueprint(CommentBlueprint)
api.register_blueprint(CategoryBlueprint)
api.register_blueprint(StatsBlueprint)

if __name__ == '__main__':
    app.run()
