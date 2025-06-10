"""Configuração do schema para a API Planify."""
from drf_spectacular.extensions import OpenApiViewExtension
from drf_spectacular.utils import extend_schema, OpenApiParameter
from drf_spectacular.types import OpenApiTypes
from drf_spectacular.openapi import AutoSchema

class FlatApiSchema(AutoSchema):
    """Schema personalizado para uma documentação mais plana."""
    
    def get_tags(self):
        """Remove as tags para ter uma documentação sem divisões."""
        return []

    def get_operation_id(self):
        """Gera IDs de operação mais limpos e diretos."""
        method = self.method.lower()
        path = self.path.replace('{', '').replace('}', '').replace('/', '_')
        return f"{method}_{path}"

    def get_description(self):
        """Gera descrições padronizadas para operações."""
        doc = self.view.get_view_description()
        if doc:
            return doc

        method_descriptions = {
            'GET': 'Retorna os dados solicitados',
            'POST': 'Cria um novo registro',
            'PUT': 'Atualiza o registro completamente',
            'PATCH': 'Atualiza o registro parcialmente',
            'DELETE': 'Remove o registro'
        }
        return method_descriptions.get(self.method, '')
