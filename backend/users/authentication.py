from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError, AuthenticationFailed
from django.conf import settings
from django.middleware.csrf import CsrfViewMiddleware
from rest_framework import exceptions
import logging
import traceback

logger = logging.getLogger(__name__)

class CustomJWTAuthentication(JWTAuthentication):
    """
    Autenticação JWT personalizada que verifica tokens em cookies e headers.
    """
    
    def authenticate(self, request):
        # Informações básicas da requisição
        logger.debug(f"Autenticando requisição para: {request.path} [{request.method}]")
        
        # Verificar se o usuário já está autenticado - IMPORTANTE: não acessar request.user diretamente
        # pois isso causará recursão infinita
        if hasattr(request, '_authenticator') and hasattr(request, '_user'):
            logger.debug(f"Usuário já autenticado via _authenticator")
            return request._user, None

        # Verificar o header de autorização
        auth_header = request.META.get('HTTP_AUTHORIZATION', '')
        if auth_header:
            logger.debug(f"Header de autorização encontrado: {auth_header[:20]}...")
        else:
            logger.debug("Nenhum header de autorização encontrado")
            
        # Obter o header de autorização usando o método da classe pai
        header = self.get_header(request)
        if header is None:
            logger.debug("Nenhum header de autorização válido encontrado, tentando cookie")
            return self.authenticate_from_cookie(request)

        # Extrair o token do header
        raw_token = self.get_raw_token(header)
        if raw_token is None:
            logger.debug("Header encontrado, mas nenhum token válido extraído, tentando cookie")
            return self.authenticate_from_cookie(request)

        # Tentar validar o token
        logger.debug(f"Token extraído do header: {raw_token[:15]}...")
        try:
            # Validar o token
            validated_token = self.get_validated_token(raw_token)
            logger.debug(f"Token validado com sucesso")
            
            # Obter o usuário a partir do token
            user = self.get_user(validated_token)
            logger.info(f"Usuário {user.username} (ID: {user.id}) autenticado com sucesso via token")
            return user, validated_token
        except (InvalidToken, TokenError, AuthenticationFailed) as e:
            logger.warning(f"Falha na validação do token: {str(e)}")
            if 'token_not_valid' in str(e):
                logger.warning("Token expirado ou inválido, tentando refresh")
            return self.authenticate_from_cookie(request)
        except Exception as e:
            logger.error(f"Erro inesperado durante autenticação: {str(e)}")
            logger.debug(f"Detalhes do erro: {traceback.format_exc()}")
            return self.authenticate_from_cookie(request)

    def authenticate_from_cookie(self, request):
        # Verificar se existe um token no cookie
        cookie_name = settings.SIMPLE_JWT.get('AUTH_COOKIE', 'auth_token')
        raw_token_cookie = request.COOKIES.get(cookie_name)
        
        if raw_token_cookie is None:
            logger.debug(f"Nenhum cookie '{cookie_name}' encontrado")
            return None
        
        # Tentar validar o token do cookie
        logger.debug(f"Token encontrado no cookie: {raw_token_cookie[:15] if len(raw_token_cookie) > 15 else raw_token_cookie}...")
        try:
            # Validar o token
            validated_token = self.get_validated_token(raw_token_cookie)
            logger.debug(f"Token do cookie validado com sucesso")
            
            # Obter o usuário a partir do token
            user = self.get_user(validated_token)
            if not user.is_active:
                logger.warning(f"Usuário {user.username} (ID: {user.id}) está inativo. Autenticação negada.")
                return None
                
            logger.info(f"Usuário {user.username} (ID: {user.id}) autenticado com sucesso via cookie")
            return user, validated_token
        except InvalidToken as e:
            logger.warning(f"Token inválido no cookie: {str(e)}")
            return None
        except TokenError as e:
            logger.warning(f"Erro no token do cookie: {str(e)}")
            if 'token_not_valid' in str(e):
                logger.warning("Token do cookie expirado ou inválido")
            return None
        except AuthenticationFailed as e:
            logger.warning(f"Autenticação falhou com token do cookie: {str(e)}")
            return None
        except Exception as e:
            logger.error(f"Erro inesperado durante autenticação via cookie: {str(e)}")
            logger.debug(f"Detalhes do erro: {traceback.format_exc()}")
            return None

    def enforce_csrf(self, request):
        """
        Verifica CSRF para requisições que usam cookies para autenticação.
        """
        check = CSRFCheck()
        check.process_request(request)
        reason = check.process_view(request, None, (), {})
        if reason:
            logger.warning(f"Verificação CSRF falhou: {reason}")
            raise exceptions.PermissionDenied('CSRF Failed: %s' % reason)
        logger.debug("Verificação CSRF passou com sucesso")


class CSRFCheck(CsrfViewMiddleware):
    def _reject(self, request, reason):
        # Retorna apenas o motivo em vez de uma resposta HTTP
        return reason
