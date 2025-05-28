from rest_framework_simplejwt.authentication import JWTAuthentication
from django.conf import settings
from rest_framework.authentication import CSRFCheck
from rest_framework import exceptions

class CustomJWTAuthentication(JWTAuthentication):
    """
    Autenticação JWT personalizada que verifica tokens em cookies e headers.
    """
    
    def authenticate(self, request):
        # Primeiro tenta autenticar usando o método padrão (Authorization header)
        try:
            return super().authenticate(request)
        except:
            # Se falhar, tenta obter o token do cookie
            raw_token = request.COOKIES.get(settings.SIMPLE_JWT.get('AUTH_COOKIE', 'auth_token'))
            
            if raw_token is None:
                return None
            
            validated_token = self.get_validated_token(raw_token)
            return self.get_user(validated_token), validated_token
    
    def enforce_csrf(self, request):
        """
        Verifica CSRF para requisições que usam cookies para autenticação.
        """
        check = CSRFCheck()
        check.process_request(request)
        reason = check.process_view(request, None, (), {})
        if reason:
            raise exceptions.PermissionDenied('CSRF Failed: %s' % reason)
