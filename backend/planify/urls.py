"""
URL configuration for planify project.
"""

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic.base import RedirectView
from django.http import JsonResponse
import debug_toolbar

# Importações da drf_spectacular para geração de documentação OpenAPI
from drf_spectacular.views import SpectacularAPIView, SpectacularRedocView, SpectacularSwaggerView


# Customizar o site admin
admin.site.site_header = settings.ADMIN_SITE_HEADER
admin.site.site_title = settings.ADMIN_SITE_TITLE
admin.site.index_title = settings.ADMIN_INDEX_TITLE


def api_root(request):
    """Endpoint para a raiz da API (/api/)"""
    return JsonResponse({
        "message": "Bem-vindo à API Planify",
        "version": "1.0.0",
        "documentation": "/api/schema/swagger-ui/",
        "status": "online"
    })


# Lista principal de rotas do projeto
urlpatterns = [
    # Redireciona a rota raiz para o admin
    path('', RedirectView.as_view(url='/admin/', permanent=True), name='root'),
    
    # Admin do Django
    path('admin/', admin.site.urls),
    
    # === ROTAS DE AUTENTICAÇÃO E AUTORIZAÇÃO ===
    path('api/auth/', include('users.urls')),  
    
    # === MÓDULOS DO SISTEMA ===
    # Teams (gerenciamento de equipes)
    path('api/teams/', include('teams.urls')),
    
    # Outros módulos...
    path('api/projects/', include('projects.urls')),
    path('api/tasks/', include('tasks.urls')),
    path('api/risks/', include('risks.urls')),
    path('api/costs/', include('costs.urls')),
    path('api/documents/', include('documents.urls')),
    path('api/communications/', include('communications.urls')),
    
    # === DOCUMENTAÇÃO DA API ===
    # URLs para documentação da API com drf-spectacular
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    
    # URLs principais para documentação (mais curtas e amigáveis)
    path('docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('swagger/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger'),
    path('redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
    
    # URLs alternativas com prefixo api/ (mantidas por compatibilidade)
    path('api/docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='api-docs'),
    path('api/schema/swagger-ui/', SpectacularSwaggerView.as_view(url_name='schema'), name='schema-swagger-ui'),
    path('api/schema/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='schema-redoc'),
]

# Durante o desenvolvimento (DEBUG=True), serve arquivos estáticos e de mídia diretamente
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns.insert(0, path('__debug__/', include(debug_toolbar.urls)))
