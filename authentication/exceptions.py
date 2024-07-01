from rest_framework.exceptions import APIException

class InternalServerError(APIException):
    status_code = 500
    default_detail = 'Server Error'
    default_code = 'server_error'