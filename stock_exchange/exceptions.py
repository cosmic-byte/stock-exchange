from rest_framework import status
from rest_framework.exceptions import APIException


class UnableToDeleteObject(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = 'You cannot delete this object. It is referenced by another object'
    default_code = 'disallowed_delete'


class ModelNotFoundException(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = 'Model not found'
    default_code = 'bad_request'


class ExpiredTokenException(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = 'Token expired'
    default_code = 'bad_request'


class InvalidModelException(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = 'The model is not properly constructed'
    default_code = 'bad_request'
