"""
Decoradores personalizados para as views da API.
"""
from functools import wraps
from rest_framework.permissions import IsAuthenticated, AllowAny
from drf_yasg.utils import swagger_auto_schema

def swagger_public_schema(view_func):
    """
    Decorador para permitir que um endpoint seja acessível sem autenticação
    apenas para fins de documentação no Swagger/ReDoc.
    """
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        # Verifica se a requisição é do Swagger/ReDoc
        is_swagger = False
        if request.META.get('HTTP_REFERER'):
            referer = request.META.get('HTTP_REFERER')
            if 'swagger' in referer or 'redoc' in referer or 'api-docs' in referer:
                is_swagger = True
        
        # Se for do Swagger/ReDoc, permite acesso sem autenticação
        if is_swagger:
            view_func.permission_classes = [AllowAny]
        else:
            view_func.permission_classes = [IsAuthenticated]
        
        return view_func(request, *args, **kwargs)
    
    return wrapper

def swagger_schema_with_examples(**kwargs):
    """
    Decorador para adicionar exemplos de requisição e resposta à documentação do Swagger/ReDoc.
    """
    return swagger_auto_schema(**kwargs)
