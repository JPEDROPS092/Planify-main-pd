from drf_spectacular.extensions import OpenApiAuthenticationExtension

class JWTAuthenticationScheme(OpenApiAuthenticationExtension):
    """Extensão para integrar o JWTAuthentication padrão com o OpenAPI/Swagger."""
    
    target_class = 'rest_framework_simplejwt.authentication.JWTAuthentication' 
    name = 'JWT Authentication'
    
    def get_security_definition(self, auto_schema):
        return {
            'type': 'http',
            'scheme': 'bearer',
            'bearerFormat': 'JWT',
            'description': 'Token JWT para autenticação. Formato: Bearer [token]. Obtenha o token em /api/auth/jwt/create/'
        }
