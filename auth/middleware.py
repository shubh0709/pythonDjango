import os
from typing import Any, Callable

from django.http import HttpRequest, HttpResponse
from jwt import JWT, AbstractJWKBase, jwk_from_dict

jwt_token_secret = os.getenv('JWT_TOKEN_SECRET')


class JWTMiddleware:
    def __init__(self, get_response: Callable[[HttpRequest], HttpResponse]) -> None:
        self.get_response = get_response

    def __call__(self, request: HttpRequest) -> HttpResponse:
        # Exclude certain routes from JWT middleware
        if request.path_info.startswith('/auth'):
            return self.get_response(request)

        # Retrieve the JWT token from the request headers or other sources
        token = self.get_token_from_request(request)

        # Verify and decode the JWT token
        decoded_token = self.verify_and_decode_token(token)

        # Attach the decoded token data to the request object
        request['jwt_data'] = decoded_token

        # Pass the request to the next middleware or view
        response = self.get_response(request)

        return response

    def get_token_from_request(self, request: HttpRequest) -> str:
        extracted_token = request.headers.get('loginToken')
        return "" if extracted_token is None else extracted_token

    def verify_and_decode_token(self, token: str) -> dict[str, Any]:
        try:
            key: AbstractJWKBase = jwk_from_dict(
                dct={'kty': 'oct', 'k': jwt_token_secret})
            # Verify and decode the JWT token using your secret key
            decoded_token = JWT().decode(
                message=token, key=key, algorithms=['HS256'])
            return decoded_token
        except Exception as exc:
            # Handle invalid tokens or token verification errors
            # You can raise an exception, return None, or handle it based on your application's needs
            return None
