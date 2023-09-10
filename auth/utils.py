# utils.py
import os
from typing import Any, Type, TypeVar
from uuid import UUID

from jwt import JWT, AbstractJWKBase, jwk_from_dict
from rest_framework import serializers
from rest_framework.serializers import Serializer
from twilio.rest import Client

jwt_token_secret = os.getenv('JWT_TOKEN_SECRET')


def generate_token(id: UUID) -> str:
    key: AbstractJWKBase = jwk_from_dict(
        dct={'kty': 'oct', 'k': jwt_token_secret})
    token = JWT().encode({'user_id': f'{id}'}, key=key, alg='HS256')
    return token


def send_sms(to_number: str, body: str):
    client = Client(os.getenv('ENV_TWILIO_ACCOUNT_SID'),
                    os.getenv('ENV_TWILIO_AUTH_TOKEN'))

    message: Any = client.messages.create(
        body=body,
        from_=os.getenv('ENV_TWILIO_PHONE_NUMBER'),
        to=to_number
    )

    return message.sid


T = TypeVar('T', bound=Serializer)


def schema_validation(data: Any, serializer:  Type[T]) -> T:
    serialized_data = serializer(data=data)
    if serialized_data.is_valid():
        return serialized_data
    else:
        raise serializers.ValidationError(serialized_data.errors)
