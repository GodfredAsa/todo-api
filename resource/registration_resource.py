from http import HTTPStatus

import bcrypt
from flask_restful import Resource

from exceptions import BadRequestException, ConflictException
from model.user_model import UserModel
from utils.api_response import CustomApiResponse
from utils.auth_utils import validate_preferred_name
from utils.user_utils import get_user_data
from flask import jsonify

class RegistrationResource(Resource):

    def post(self):
        data = get_user_data()
        if UserModel.find_by_preferred_name(data["preferred_name"]):
            raise ConflictException("Preferred name already taken")

        user = UserModel(
            preferred_name=data["preferred_name"],
            password=data["password"],
        )
        if not validate_preferred_name(user.preferred_name):
            raise BadRequestException("Invalid preferred name")

        user.password = bcrypt.hashpw(user.password.encode("utf-8"), bcrypt.gensalt())
        user.save_to_db()
        return CustomApiResponse.get_response(
            HTTPStatus.CREATED,
            "Registration successful",
            user.to_json(),
        ), HTTPStatus.CREATED
