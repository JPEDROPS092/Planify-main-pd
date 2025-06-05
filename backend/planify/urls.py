"""
URL configuration for planify project.
Define as rotas principais da aplicação Django, incluindo a documentação da API,
autenticação, administração e os módulos funcionais.
"""

# Importações padrão do Django para gerenciamento de URLs e admin
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic.base import RedirectView
from django.http import JsonResponse
import debug_toolbar

# Importações do Django REST Framework para autenticação via JWT
from rest_framework_simplejwt.views import TokenRefreshView

# Importação para o CustomTokenObtainPairView
from users.auth_views import CustomTokenObtainPairView

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
    
    # API Root - Endpoint específico para /api/
    path('api/', api_root, name='api-root'),
    
    # === ROTAS DE AUTENTICAÇÃO ===
    # Rotas de autenticação JWT do Djoser (mantidas como padrão primário)
    path('api/auth/', include('djoser.urls')),
    path('api/auth/', include('djoser.urls.jwt')),
    path('api/auth/token/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/auth/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    
    # === MÓDULOS DO SISTEMA ===
    # Core (saúde, dashboard, métricas)
    path('api/', include('core.urls')),
    
    # Módulos principais
    path('api/projects/', include('projects.urls')),
    path('api/tasks/', include('tasks.urls')),
    path('api/teams/', include('teams.urls')),
    path('api/risks/', include('risks.urls')),
    path('api/costs/', include('costs.urls')),
    path('api/documents/', include('documents.urls')),
    path('api/communications/', include('communications.urls')),
    path('api/users/', include('users.urls')),
    
    # === DOCUMENTAÇÃO DA API ===
    # URLs para documentação da API com drf-spectacular
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/schema/swagger-ui/', SpectacularSwaggerView.as_view(url_name='schema'), name='schema-swagger-ui'),
    path('api/schema/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='schema-redoc'),
]

# Durante o desenvolvimento (DEBUG=True), serve arquivos estáticos e de mídia diretamente
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns.insert(0, path('__debug__/', include(debug_toolbar.urls)))
