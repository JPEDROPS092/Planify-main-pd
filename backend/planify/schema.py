"""
Configurações para a documentação da API usando drf-yasg (Swagger/ReDoc).
"""
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

schema_info = openapi.Info(
    title="Planify API",
    default_version='v1',
    description="""
    API para o sistema Planify - Gerenciamento de Projetos de P&D
    
    O Planify é um sistema completo para gerenciamento de projetos de Pesquisa e Desenvolvimento,
    oferecendo funcionalidades para:
    
    * Usuários - Autenticação, perfis e permissões
    * Projetos - Gerenciamento de projetos e sprints
    * Tarefas - Gerenciamento de tarefas e atribuições
    * Equipes - Gerenciamento de equipes e membros
    * Riscos - Identificação e mitigação de riscos
    * Custos - Controle de orçamentos e gastos
    * Documentos - Gerenciamento de documentação
    * Comunicações - Chat integrado e notificações
    
    Esta documentação fornece detalhes sobre todos os endpoints disponíveis na API.
    """,
    terms_of_service="https://www.planify.com/terms/",
    contact=openapi.Contact(email="contato@planify.com"),
    license=openapi.License(name="MIT License"),
)

schema_view = get_schema_view(
    schema_info,
    public=True,
    permission_classes=(permissions.AllowAny,),
)
