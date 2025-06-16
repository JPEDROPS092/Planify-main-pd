"""
Schema configurations for the Planify API.
"""

from drf_spectacular.openapi import AutoSchema
from drf_spectacular.utils import extend_schema
from drf_spectacular.types import OpenApiTypes


class PlanifyAutoSchema(AutoSchema):
    """Custom AutoSchema for Planify API with enhanced documentation."""
    
    def get_operation_id(self):
        """Generate more readable operation IDs."""
        operation_id = super().get_operation_id()
        # Remove redundant 'api_' prefix
        if operation_id.startswith('api_'):
            operation_id = operation_id[4:]
        return operation_id
    
    def get_tags(self):
        """Get tags for the endpoint."""
        tags = super().get_tags()
        if not tags:
            # Set default tag based on app name
            if hasattr(self.view, 'basename'):
                app_name = getattr(self.view, 'basename', '').split('_')[0]
                if app_name:
                    return [app_name.title()]
        return tags


# Common response schemas
COMMON_RESPONSES = {
    400: {
        "description": "Dados inválidos",
        "content": {
            "application/json": {
                "schema": {
                    "type": "object",
                    "properties": {
                        "error": {
                            "type": "string",
                            "example": "Dados inválidos fornecidos"
                        },
                        "details": {
                            "type": "object",
                            "additionalProperties": {
                                "type": "array",
                                "items": {"type": "string"}
                            }
                        }
                    }
                }
            }
        }
    },
    401: {
        "description": "Não autenticado",
        "content": {
            "application/json": {
                "schema": {
                    "type": "object",
                    "properties": {
                        "detail": {
                            "type": "string",
                            "example": "Token de autenticação não fornecido."
                        }
                    }
                }
            }
        }
    },
    403: {
        "description": "Permissão negada",
        "content": {
            "application/json": {
                "schema": {
                    "type": "object",
                    "properties": {
                        "detail": {
                            "type": "string",
                            "example": "Você não tem permissão para realizar esta ação."
                        }
                    }
                }
            }
        }
    },
    404: {
        "description": "Não encontrado",
        "content": {
            "application/json": {
                "schema": {
                    "type": "object",
                    "properties": {
                        "detail": {
                            "type": "string",
                            "example": "Recurso não encontrado."
                        }
                    }
                }
            }
        }
    },
    500: {
        "description": "Erro interno do servidor",
        "content": {
            "application/json": {
                "schema": {
                    "type": "object",
                    "properties": {
                        "error": {
                            "type": "string",
                            "example": "Erro interno do servidor. Tente novamente mais tarde."
                        }
                    }
                }
            }
        }
    }
}


def extend_schema_with_common_responses(**kwargs):
    """Extend schema with common response codes."""
    responses = kwargs.get('responses', {})
    
    # Add common responses if not already specified
    for code, response in COMMON_RESPONSES.items():
        if code not in responses:
            responses[code] = response
    
    kwargs['responses'] = responses
    return extend_schema(**kwargs)


# API Version information
API_VERSION_INFO = {
    'version': '1.0.0',
    'title': 'Planify API',
    'description': 'Sistema de Gerenciamento de Projetos',
    'terms_of_service': 'https://planify.com/terms/',
    'contact': {
        'name': 'Equipe Planify',
        'email': 'api@planify.com',
        'url': 'https://planify.com/support/'
    },
    'license': {
        'name': 'MIT License',
        'url': 'https://opensource.org/licenses/MIT'
    }
}
