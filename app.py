
from http import HTTPStatus

from flask_restful import Api
from db import db
from constant.app_constants import *
from flask import Flask, jsonify
from flask_jwt_extended import JWTManager
from flask_swagger_ui import get_swaggerui_blueprint
from werkzeug.exceptions import HTTPException
from exceptions import InternalServerErrorException
from resource.authentication_resource import AuthenticationResource
from resource.health_resource import HealthResource
from resource.health_resource_v2 import HealthResourceV2
from resource.registration_resource import RegistrationResource
from resource.task_resource import (
    TaskByUserResource,
    TaskResource,
    TaskSearchResource,
    TasksByUserResource,
)
from swagger_docs import OPENAPI_SPEC
from utils.api_response import CustomApiResponse



swagger_ui = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config={"app_name": "Todo API"},
)

app = Flask(__name__)
app.config["JWT_SECRET_KEY"] = JWT_SECRET_KEY
jwt = JWTManager(app)
api = Api(app)
app.register_blueprint(swagger_ui, url_prefix=SWAGGER_URL)


@app.route(API_URL, methods=["GET"])
def swagger_spec():
    return jsonify(OPENAPI_SPEC)


@app.errorhandler(Exception)
def handle_unexpected_exception(error):
    if isinstance(error, HTTPException):
        return error

    app.logger.exception("Unhandled application exception")
    internal_error = InternalServerErrorException("Internal Server Error")
    return internal_error.data, internal_error.code


@jwt.unauthorized_loader
def handle_missing_authorization_header(error):
    return CustomApiResponse.get_response(
        HTTPStatus.UNAUTHORIZED,
        error,
        None,
    ), HTTPStatus.UNAUTHORIZED


app.config[SQLALCHEMY_DATABASE_URI] = DB_CONNECTION_STRING
app.config[SQL_MODIFICATION_STRING] = False
app.config[PROPAGATE_EXCEPTIONS] = True
app.config[JWT_SECRET] = 'joe'
db.init_app(app)


@app.before_first_request
def create_tables():
    db.create_all()


# API VERSION = "1.0.0"
api.add_resource(HealthResource, "/api/health")
api.add_resource(RegistrationResource, "/api/v1/register")
api.add_resource(AuthenticationResource, "/api/v1/auth/login")

api.add_resource(TaskResource, "/api/v1/tasks")
api.add_resource(TaskSearchResource, "/api/v1/tasks/search")
api.add_resource(TasksByUserResource, "/api/v1/users/<string:user_id>/tasks")

api.add_resource(TaskByUserResource, "/api/v1/users/<string:user_id>/tasks/<string:task_id>")

# API VERSION = "2.0.0"
api.add_resource(HealthResourceV2, "/api/v2/health")


if __name__ == "__main__":
    app.run(port=5001, debug=True)