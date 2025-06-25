from django.urls import path
from .views import (
    documentacao_api,
    verificacao_saude,
    verificacao_saude_detalhada
)
app_name = 'core'

urlpatterns = [
    # Endpoints de documentação e verificação de saúde
    path('docs/', documentacao_api, name='api_docs'),
    path('health/', verificacao_saude, name='health_check'),
    path('health/detailed/', verificacao_saude_detalhada, name='health_check_detailed'),
]
