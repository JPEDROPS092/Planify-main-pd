"""
Utilitários para o projeto Planify.
"""
from rest_framework.views import exception_handler
from rest_framework.response import Response
from rest_framework import status
from functools import wraps
from drf_spectacular.utils import extend_schema, OpenApiExample, OpenApiParameter, OpenApiResponse

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


def swagger_schema_with_examples(summary=None, description=None, examples=None, responses=None, parameters=None, tags=None):
    """
    Decorador personalizado para adicionar exemplos à documentação da API usando drf-spectacular.
    
    Args:
        summary (str): Resumo da operação em português
        description (str): Descrição detalhada da operação em português
        examples (dict): Dicionário com exemplos de requisição
        responses (dict): Dicionário com exemplos de resposta
        parameters (list): Lista de parâmetros da operação
        tags (list): Lista de tags para categorizar a operação
    
    Returns:
        function: Decorador configurado
    """
    formatted_examples = []
    formatted_responses = {}
    formatted_parameters = []
    
    # Formatar exemplos de requisição
    if examples:
        for name, example in examples.items():
            formatted_examples.append(
                OpenApiExample(
                    name=name,
                    value=example.get('value'),
                    summary=example.get('summary', ''),
                    description=example.get('description', ''),
                    request_only=example.get('request_only', True),
                    response_only=example.get('response_only', False),
                )
            )
    
    # Formatar exemplos de resposta
    if responses:
        for status_code, response in responses.items():
            formatted_responses[status_code] = OpenApiResponse(
                description=response.get('description', ''),
                examples=[
                    OpenApiExample(
                        name=example.get('name', f'exemplo-{i}'),
                        value=example.get('value'),
                        summary=example.get('summary', ''),
                        description=example.get('description', ''),
                        request_only=False,
                        response_only=True,
                    ) for i, example in enumerate(response.get('examples', []))
                ] if 'examples' in response else None
            )
    
    # Formatar parâmetros
    if parameters:
        for param in parameters:
            formatted_parameters.append(
                OpenApiParameter(
                    name=param.get('name'),
                    description=param.get('description', ''),
                    required=param.get('required', False),
                    type=param.get('type', 'string'),
                    location=param.get('location', 'query'),
                    enum=param.get('enum'),
                    examples=param.get('examples'),
                )
            )
    
    # Aplicar o decorador do drf-spectacular
    return extend_schema(
        summary=summary,
        description=description,
        examples=formatted_examples,
        responses=formatted_responses,
        parameters=formatted_parameters,
        tags=tags,
    )
