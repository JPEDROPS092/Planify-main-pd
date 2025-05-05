"""
Utilitários para o projeto Planify.
"""
from rest_framework.views import exception_handler
from rest_framework.response import Response
from rest_framework import status

def custom_exception_handler(exc, context):
    """
    Manipulador de exceções personalizado para o REST Framework.
    Permite que a documentação da API seja acessada sem autenticação.
    """
    # Chama o manipulador de exceções padrão primeiro
    response = exception_handler(exc, context)
    
    # Verifica se a requisição é do Swagger/ReDoc
    request = context.get('request')
    if request and request.META.get('HTTP_REFERER'):
        referer = request.META.get('HTTP_REFERER')
        if 'swagger' in referer or 'redoc' in referer or 'api-docs' in referer:
            # Para requisições do Swagger/ReDoc, retorna uma resposta simulada
            # para permitir a documentação dos endpoints
            view = context.get('view')
            if hasattr(view, 'get_serializer'):
                return Response(
                    {"detail": "Este é um exemplo de resposta para documentação."},
                    status=status.HTTP_200_OK
                )
    
    return response
