"""
Utilitários para a documentação da API com drf-spectacular.
"""
from drf_spectacular.utils import extend_schema, OpenApiExample, OpenApiResponse

def documentar_api(summary, description, responses=None, tags=None):
    """
    Decorador simplificado para documentar endpoints com drf-spectacular.
    
    Args:
        summary (str): Resumo da operação (título no Swagger).
        description (str): Descrição detalhada da operação.
        responses (dict): Dicionário de respostas possíveis, usando serializers.
                          Ex: {200: MeuSerializer, 404: ErroSerializer}
        tags (list): Lista de tags para agrupar o endpoint.
    """
    # Adiciona respostas de erro comuns automaticamente se não forem fornecidas
    common_errors = {
        401: OpenApiResponse(description="Não autenticado"),
        403: OpenApiResponse(description="Permissão negada"),
        404: OpenApiResponse(description="Recurso não encontrado"),
    }
    if responses:
        for code, resp in common_errors.items():
            if code not in responses:
                responses[code] = resp
    else:
        responses = common_errors

    return extend_schema(
        summary=summary,
        description=description,
        responses=responses,
        tags=tags
    )