"""
Decoradores personalizados para as views da API.
"""
from functools import wraps
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.schemas.coreapi import AutoSchema

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
            if 'swagger' in referer or 'redoc' in referer or 'api-docs' in referer or 'schema' in referer:
                is_swagger = True
        
        # Se for do Swagger/ReDoc, permite acesso sem autenticação
        if is_swagger:
            view_func.permission_classes = [AllowAny]
        else:
            view_func.permission_classes = [IsAuthenticated]
        
        return view_func(request, *args, **kwargs)
    
    return wrapper

def swagger_schema_with_examples(method='get', operation_description=None, manual_parameters=None, responses=None):
    """
    Decorador para adicionar exemplos e descrições à documentação da API usando DRF.
    Substitui o swagger_auto_schema do drf-yasg.
    """
    class CustomAutoSchema(AutoSchema):
        def get_link(self, path, method, base_url):
            link = super().get_link(path, method, base_url)
            
            # Adicionar descrição da operação
            if operation_description:
                link.description = operation_description
                
            return link
    
    def decorator(view_func):
        view_func.schema = CustomAutoSchema()
        return view_func
    
    return decorator
