"""
Extensões para o esquema OpenAPI para autenticação personalizada.
"""
from drf_spectacular.extensions import OpenApiAuthenticationExtension
from users.authentication import CustomJWTAuthentication


class CustomJWTAuthenticationScheme(OpenApiAuthenticationExtension):
    """
    Extensão para documentação da autenticação JWT personalizada.
    Esta classe permite que o drf-spectacular reconheça corretamente
    o método de autenticação CustomJWTAuthentication.
    """
    target_class = CustomJWTAuthentication
    name = 'JWT'  # Nome do esquema de segurança no OpenAPI

    def get_security_definition(self, auto_schema):
        """
        Define o esquema de segurança para a autenticação JWT.
        """
        return {
            'type': 'http',
            'scheme': 'bearer',
            'bearerFormat': 'JWT',
            'description': 'Token de autenticação JWT. Pode ser fornecido no header Authorization ou em um cookie.'
        }
