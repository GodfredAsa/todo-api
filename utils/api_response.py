from typing import Any
from flask import jsonify


class CustomApiResponse:

    @staticmethod
    def get_response(status: int, message: str, data: Any = None):
        return {
            "status": status,
            "message": message,
            "data": data,
        }