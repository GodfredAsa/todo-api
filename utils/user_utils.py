from flask_restful import reqparse

from constant.user_constant import BLANK_ERROR

_user_parser = reqparse.RequestParser()
_user_parser.add_argument("preferred_name", type=str, required=True, help=BLANK_ERROR.format("preferred_name"))
_user_parser.add_argument("password", type=str, required=True, help=BLANK_ERROR.format("password"))

def get_user_data() -> object:
    return _user_parser.parse_args()