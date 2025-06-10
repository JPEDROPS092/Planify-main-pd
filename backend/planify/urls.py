"""
URL configuration for planify project.
"""

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic.base import RedirectView
from django.http import JsonResponse
from rest_framework.permissions import AllowAny
from drf_spectacular.views import SpectacularAPIView, SpectacularRedocView, SpectacularSwaggerView

# Customizar o site admin
admin.site.site_header = "Planify Admin"
admin.site.site_title = "Planify"
admin.site.index_title = "Painel de Administração"


def api_root(request):
    """Endpoint para a raiz da API (/api/)"""
    return JsonResponse({
        "message": "Bem-vindo à API Planify",
        "version": "1.0.0",
        "documentation": "/api/docs/",
        "status": "online"
    })


# Lista principal de rotas do projeto
urlpatterns = [
    # Admin
    path('admin/', admin.site.urls),
    
    # API Schema & Documentation
    path('api/schema/', SpectacularAPIView.as_view(
        permission_classes=[AllowAny],
        authentication_classes=[],
    ), name='schema'),
    path('api/docs/', SpectacularSwaggerView.as_view(
        url_name='schema',
        permission_classes=[AllowAny],
        authentication_classes=[],
    ), name='swagger-ui'),
    path('api/redoc/', SpectacularRedocView.as_view(
        url_name='schema',
        permission_classes=[AllowAny],
        authentication_classes=[],
    ), name='redoc'),
    
    # API Root
    path('api/', api_root, name='api-root'),
    
    # App URLs
    path('api/auth/', include('djoser.urls')),
    path('api/auth/', include('djoser.urls.jwt')),
    path('api/projects/', include('projects.urls')),
    path('api/tasks/', include('tasks.urls')),
    path('api/teams/', include('teams.urls')),
    path('api/communications/', include('communications.urls')),
    path('api/risks/', include('risks.urls')),
    path('api/costs/', include('costs.urls')),
    path('api/documents/', include('documents.urls')),
] 

# Servir arquivos estáticos e de mídia em desenvolvimento
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
