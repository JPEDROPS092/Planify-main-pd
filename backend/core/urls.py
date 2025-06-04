from django.urls import path
from .views import (
    documentacao_api, verificacao_saude, verificacao_saude_detalhada,
    visao_geral_dashboard, metricas_projeto, dashboard_usuario
)

app_name = 'core'

urlpatterns = [
    # Endpoints de documentação e verificação de saúde
    path('docs/', documentacao_api, name='api_docs'),
    path('health/', verificacao_saude, name='health_check'),
    path('health/detailed/', verificacao_saude_detalhada, name='health_check_detailed'),
    
    # Endpoints de dashboard
    path('dashboard/', visao_geral_dashboard, name='dashboard_overview'),
    path('projects/<int:id_projeto>/metrics/', metricas_projeto, name='project_metrics'),
    path('user/dashboard/', dashboard_usuario, name='user_dashboard'),
]

# Aliases para nomes em inglês (compatibilidade com código existente)
# Estes aliases não afetam as rotas, apenas permitem referências programáticas
# aos mesmos endpoints por nomes diferentes
