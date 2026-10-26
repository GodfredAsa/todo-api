from http import HTTPStatus

from flask import request
from flask_restful import Resource

from exceptions import BadRequestException, UnauthorizedException
from model.user_model import UserModel
from utils.api_response import CustomApiResponse
from utils.auth_utils import verify_credentials, generate_token


class AuthenticationResource(Resource):

    def post(self):
        data = request.get_json(silent=True) or {}
        preferred_name = data.get("preferred_name")
        password = data.get("password")
        if not preferred_name or not password:
            raise BadRequestException("Preferred name and password are required")
        if not verify_credentials(preferred_name, password):
            raise UnauthorizedException("Invalid Credentials")
        user = UserModel.find_by_preferred_name(preferred_name)
        return CustomApiResponse.get_response(HTTPStatus.OK, "Login successful", generate_token(user)), HTTPStatus.OK