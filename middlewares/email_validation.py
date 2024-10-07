from rest_framework.exceptions import AuthenticationFailed
from rest_framework_simplejwt.authentication import JWTAuthentication


class EmailAndUsernameValidationMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if 'Authorization' in request.headers:
            jwt_auth = JWTAuthentication()
            header = jwt_auth.get_header(request)
            raw_token = jwt_auth.get_raw_token(header)
            validated_token = jwt_auth.get_validated_token(raw_token)
            user = jwt_auth.get_user(validated_token)

            if user.is_authenticated:
                token_email = validated_token.get('email')
                token_username = validated_token.get('username')
                if token_email != user.email or token_username != user.username:
                    raise AuthenticationFailed("Email or username mismatch, please log in again.")

        response = self.get_response(request)
        return response
