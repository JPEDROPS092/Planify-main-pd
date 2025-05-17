from django.urls import path
from . import views

app_name = 'api-core'

urlpatterns = [
    # API Root - Documentação principal da API
    path('', views.documentacao_api, name='api-root'),
    
    # Endpoints de saúde e monitoramento
    path('saude/', views.checagem_saude, name='checagem-saude'),
    path('saude/detalhes/', views.checagem_saude_original, name='checagem-saude-detalhes'),
    
    # Endpoints de dashboard e métricas
    path('dashboard/', views.visao_geral_dashboard, name='visao-geral-dashboard'),
    path('projetos/<int:project_id>/metricas/', views.metricas_projeto, name='metricas-projeto'),
    path('usuario/dashboard/', views.dashboard_usuario, name='dashboard-usuario'),
]
