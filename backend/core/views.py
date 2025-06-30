from django.db.models import Count, Sum, Q
from django.utils import timezone
from django.shortcuts import redirect
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny

# Imports para drf-spectacular e serializadores
from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiResponse, OpenApiExample
from drf_spectacular.types import OpenApiTypes
from rest_framework import serializers

class ErroSerializer(serializers.Serializer):
    """Serializador padrão para respostas de erro."""
    error = serializers.CharField(help_text="Mensagem descrevendo o erro ocorrido")

@api_view(['GET'])
@permission_classes([AllowAny])
def documentacao_api(request):
    """
    Redireciona para a documentação interativa da API Swagger/OpenAPI.
    Este endpoint facilita o acesso à documentação sem precisar digitar a URL completa.
    """
    return redirect('schema-swagger-ui')

@extend_schema(
    operation_id='verificacao_saude_simples',
    summary="Verificação de Saúde Simples",
    description="Endpoint simples para verificar se a API está operacional. Retorna 'ok' se estiver tudo certo.",
    responses={
        200: OpenApiResponse(
            response={'type': 'object', 'properties': {'status': {'type': 'string', 'example': 'ok'}}},
            description="API está operacional."
        )
    },
    tags=['Saúde do Sistema']
)
@api_view(['GET'])
@permission_classes([AllowAny])
def verificacao_saude(request):
    """
    Endpoint básico para verificar se a API está respondendo.
    Utilizado para health checks de infraestrutura e monitoramento.
    """
    return Response({"status": "ok"})

@extend_schema(
    operation_id='verificacao_saude_detalhada',
    summary="Verificação de Saúde Detalhada",
    description="Endpoint para verificar o estado da API, incluindo versão e ambiente. Não requer autenticação.",
    responses={
        200: OpenApiResponse(
            response={
                'type': 'object',
                'properties': {
                    'status': {'type': 'string', 'example': 'online'},
                    'versao': {'type': 'string', 'example': '1.0'},
                    'ambiente': {'type': 'string', 'example': 'desenvolvimento'},
                    'data_hora': {'type': 'string', 'format': 'date-time', 'example': '2024-07-15T14:30:00Z'}
                }
            },
            description="API está operacional com detalhes."
        )
    },
    tags=['Saúde do Sistema']
)
@api_view(['GET'])
@permission_classes([AllowAny])
def verificacao_saude_detalhada(request):
    """
    Endpoint para verificação detalhada do estado da API.
    Retorna informações sobre versão, ambiente e timestamp atual.
    Utilizado para monitoramento avançado e diagnóstico.
    """
    return Response({
        "status": "online",
        "versao": "1.0",
        "ambiente": "desenvolvimento",
        "data_hora": timezone.now().isoformat()
    })

# Aliases para manter compatibilidade com código existente
# Estes aliases permitem que o código cliente continue funcionando
# enquanto migramos para a nomenclatura padronizada em português
api_documentation = documentacao_api
health_check = verificacao_saude
health_check_original = verificacao_saude_detalhada
