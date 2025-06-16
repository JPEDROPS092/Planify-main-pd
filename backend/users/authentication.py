from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError
from rest_framework import authentication
from rest_framework import exceptions
from django.conf import settings

class CustomJWTAuthentication(JWTAuthentication):
    def authenticate(self, request):
        try:
            header = self.get_header(request)
            if header is None:
                return None

            raw_token = self.get_raw_token(header)
            if raw_token is None:
                return None

            validated_token = self.get_validated_token(raw_token)
            user = self.get_user(validated_token)
            return (user, validated_token)
        except InvalidToken:
            return None
        except TokenError:
            return None
        except Exception as e:
            return None

    def get_header(self, request):
        """
        Extracts the header containing the JWT from the given request.
        """
        header = request.META.get('HTTP_AUTHORIZATION')
        if not header:
            return None

        # Check if header starts with JWT or Bearer
        parts = header.split()
        if parts[0] not in ('JWT', 'Bearer'):
            return None

        if len(parts) != 2:
            return None

        return header


def get_tokens_for_user(user):
    """
    Generate JWT tokens for the given user
    """
    refresh = RefreshToken.for_user(user)

    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }
