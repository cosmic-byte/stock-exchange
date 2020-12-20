from rest_framework_jwt.serializers import (
    JSONWebTokenSerializer, jwt_payload_handler as default_payload_handler, jwt_encode_handler
)


def authenticate_user(client, user, admin_user=False, serializer_class=None):
    if admin_user:
        user.is_superuser = True
        user.save()

    serializer = JSONWebTokenSerializer()
    if serializer_class:
        serializer = serializer_class()

    attrs = {
        user.USERNAME_FIELD: user.get_username(),
        "password": "password",
    }
    user_credential = serializer.validate(attrs)
    client.credentials(HTTP_AUTHORIZATION="Bearer " + user_credential.get("token"))
    return client


def generate_token(user, jwt_payload_handler=None):
    payload_handler = default_payload_handler
    if jwt_payload_handler:
        payload_handler = jwt_payload_handler

    payload = payload_handler(user)
    return jwt_encode_handler(payload)
