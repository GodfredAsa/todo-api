from http import HTTPStatus
from flask_restful import Resource
from flask import jsonify

from utils.api_response import CustomApiResponse


class HealthResourceV2(Resource):
    def get(self):
        return jsonify(CustomApiResponse.get_response(HTTPStatus.OK,
                    "Application is up",
                    "Server is healthy"),
                HTTPStatus.OK)