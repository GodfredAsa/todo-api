import bcrypt, re
from flask_jwt_extended import create_refresh_token, create_access_token

from model.user_model import UserModel


def verify_credentials(preferred_name, password):
    if not UserModel.find_by_preferred_name(preferred_name):
        return False
    hashed_password = UserModel.find_by_preferred_name(preferred_name).password
    if bcrypt.hashpw(password.encode('utf8'), hashed_password) == hashed_password:
        return True
    else:
        return False

def validate_preferred_name(preferred_name):
    pattern = r"^[A-Za-z0-9]+(?:[ '-][A-Za-z0-9]+)*$"
    return re.match(pattern, preferred_name) is not None


def generate_token(user: 'UserModel') -> str:
    return create_access_token(identity=user.user_id)