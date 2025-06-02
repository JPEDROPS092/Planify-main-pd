from drf_spectacular.extensions import OpenApiAuthenticationExtension
from users.authentication import CustomJWTAuthentication


class CustomJWTAuthenticationScheme(OpenApiAuthenticationExtension):
    """Extensão para integrar o CustomJWTAuthentication com o OpenAPI/Swagger."""
    
    target_class = CustomJWTAuthentication
    name = 'JWT Authentication'
    
    def get_security_definition(self, auto_schema):
        return {
            'type': 'http',
            'scheme': 'bearer',
            'bearerFormat': 'JWT',
            'description': 'Token JWT para autenticação. Formato: Bearer [token]'
        }
