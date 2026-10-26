from http import HTTPStatus

from werkzeug.exceptions import HTTPException

from utils.api_response import CustomApiResponse


class ApiException(HTTPException):
    status_code = HTTPStatus.INTERNAL_SERVER_ERROR
    code = int(status_code)

    def __init__(self, message: str):
        super().__init__(description=message)
        self.message = message
        self.data = CustomApiResponse.get_response(
            self.status_code,
            message,
            None,
        )


class BadRequestException(ApiException):
    status_code = HTTPStatus.BAD_REQUEST
    code = int(status_code)


class UnauthorizedException(ApiException):
    status_code = HTTPStatus.UNAUTHORIZED
    code = int(status_code)


class NotFoundException(ApiException):
    status_code = HTTPStatus.NOT_FOUND
    code = int(status_code)


class ConflictException(ApiException):
    status_code = HTTPStatus.CONFLICT
    code = int(status_code)


class InternalServerErrorException(ApiException):
    status_code = HTTPStatus.INTERNAL_SERVER_ERROR
    code = int(status_code)
