"""
URL configuration for planify project.
"""

from django.contrib import admin
from django.urls import path, include, reverse
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

# === API ROOT VIEW (Opcional, mas informativo) ===
def api_root_view(request): # Renomeado para evitar conflito de nome com o path
    """Endpoint para a raiz da API (/api/)"""
    return JsonResponse({
        "message": "Bem-vindo à API Planify",
        "version": "1.0.0",
        "documentation_swagger": request.build_absolute_uri(reverse('swagger-ui')),
        "documentation_redoc": request.build_absolute_uri(reverse('redoc')),
        "schema": request.build_absolute_uri(reverse('schema')),
        "status": "online"
    })

# Lista principal de rotas do projeto
urlpatterns = [
    # Redireciona a rota raiz para o admin
    path('', RedirectView.as_view(url='/admin/', permanent=True), name='root'),

    # Admin do Django
    path('admin/', admin.site.urls),

    # === API URLs ===
    # Todas as URLs da API serão prefixadas com 'api/'
    path('api/', include([
        # Raiz da API
        path('', api_root_view, name='api-root'), # Endpoint informativo na raiz da API

        # Documentação da API (OpenAPI)
        path('schema/', SpectacularAPIView.as_view(), name='schema'),
        path('schema/swagger-ui/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
        path('schema/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),

        # MÓDULO DE USUÁRIOS (Autenticação e Gerenciamento de Usuários)
        # users.urls já contém 'auth/' e os endpoints do router como 'users/', 'profiles/', etc.
        # Então, as URLs finais serão como:
        # /api/users/auth/login/
        # /api/users/users/
        # /api/users/profiles/
        path('users/', include('users.urls', namespace='users')),

        # === OUTROS MÓDULOS DO SISTEMA ===
        # Exemplo: /api/teams/
        path('teams/', include('teams.urls', namespace='teams')), # Adicionar namespace é boa prática
        # Exemplo: /api/projects/
        path('projects/', include('projects.urls', namespace='projects')),
        # Exemplo: /api/tasks/
        path('tasks/', include('tasks.urls', namespace='tasks')),
        # Exemplo: /api/risks/
        path('risks/', include('risks.urls', namespace='risks')),
        # Exemplo: /api/costs/
        path('costs/', include('costs.urls', namespace='costs')),
        # Exemplo: /api/documents/
        path('documents/', include('documents.urls', namespace='documents')),
        # Exemplo: /api/communications/
        path('communications/', include('communications.urls', namespace='communications')),
    ])),
]

# Durante o desenvolvimento (DEBUG=True), serve arquivos estáticos e de mídia diretamente
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    # A linha abaixo para static files geralmente não é necessária se você usa
    # o runserver do Django, pois ele já serve arquivos estáticos automaticamente.
    # Mas não faz mal se você quiser ser explícito ou se tiver uma configuração diferente.
    # urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    if 'debug_toolbar' in settings.INSTALLED_APPS: # Verifica se o debug_toolbar está instalado
        urlpatterns.append(path('__debug__/', include(debug_toolbar.urls)))