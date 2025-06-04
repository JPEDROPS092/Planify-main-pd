"""
URL configuration for planify project.
Define as rotas principais da aplicação Django, incluindo a documentação da API,
autenticação, administração e os módulos funcionais.
"""

# Importações padrão do Django para gerenciamento de URLs e admin
from django.contrib import admin
from django.urls import path, include
from django.shortcuts import redirect
from django.conf import settings
from django.conf.urls.static import static
from django.http import JsonResponse
import debug_toolbar
from django.conf import settings
from django.urls import include, path


# Importações do Django REST Framework para autenticação via JWT
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

# Importação do roteador padrão do DRF (não usado diretamente, mas pronto para uso)
from rest_framework.routers import DefaultRouter
router = DefaultRouter()

# Importações da biblioteca drf_yasg (caso queira utilizar uma doc alternativa no futuro)
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework import permissions

# Importações da drf_spectacular para geração de documentação OpenAPI
from drf_spectacular.views import SpectacularAPIView, SpectacularRedocView, SpectacularSwaggerView


def root_api(request):
    return JsonResponse({"message": "Bem-vindo à API Planify. Consulte /api/schema/swagger-ui/ para a documentação."})


# Lista principal de rotas do projeto
urlpatterns = [
    # Redireciona a rota raiz para a documentação Swagger
   path('', root_api, name='api-root'),


    # Usando o admin padrão do Django em vez do customizado
    path('admin/', admin.site.urls),

    # Rotas de autenticação JWT do Djoser
    path('api/auth/', include('djoser.urls')),
    path('api/auth/', include('djoser.urls.jwt')),
    
    # URLs dos aplicativos
    path('api/', include('core.urls')),
    path('api/projects/', include('projects.urls')),
    path('api/tasks/', include('tasks.urls')),
    path('api/teams/', include('teams.urls')),
    path('api/risks/', include('risks.urls')),
    path('api/costs/', include('costs.urls')),
    path('api/documents/', include('documents.urls')),
    path('api/communications/', include('communications.urls')),
    path('api/users/', include('users.urls')),
    
# URLs de autenticação JWT
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    
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
