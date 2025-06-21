from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError
from rest_framework import authentication
from rest_framework import exceptions
from django.conf import settings
import logging

logger = logging.getLogger(__name__)

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
            
            # Verificar se o token está na blacklist
            from .models import BlacklistedTokens
            if BlacklistedTokens.objects.filter(token=str(raw_token)).exists():
                logger.warning(f"Token blacklisted usado por usuário {user.username}")
                raise InvalidToken("Token foi invalidado")
            
            return (user, validated_token)
        except InvalidToken as e:
            logger.warning(f"Token inválido: {str(e)}")
            return None
        except TokenError as e:
            logger.warning(f"Erro no token: {str(e)}")
            return None
        except Exception as e:
            logger.error(f"Erro inesperado na autenticação: {str(e)}")
            return None

    def get_header(self, request):
        """
        Extracts the header containing the JWT from the given request.
        Aceita tanto 'Bearer' quanto 'JWT' como prefixos.
        """
        header = request.META.get('HTTP_AUTHORIZATION')
        if not header:
            return None

        # Check if header starts with JWT or Bearer
        parts = header.split()
        if len(parts) != 2:
            return None
            
        if parts[0] not in ('JWT', 'Bearer'):
            return None

        return header

    def get_raw_token(self, header):
        """
        Extracts the raw token from the authorization header.
        """
        parts = header.split()
        if len(parts) == 2:
            return parts[1].encode('utf-8')
        return None


def get_tokens_for_user(user):
    """
    Generate JWT tokens for the given user
    """
    refresh = RefreshToken.for_user(user)

    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }
