"""
URL configuration for planify project.
"""
from django.contrib import admin
from django.urls import path, include
from django.shortcuts import redirect
from django.conf import settings
from django.conf.urls.static import static
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework.routers import DefaultRouter
from rest_framework.documentation import include_docs_urls
from rest_framework.schemas import get_schema_view

# Schema view for API documentation
schema_view = get_schema_view(
    title="Documentação da API Planify",
    description="API do sistema Planify para gerenciamento de projetos",
    version="1.0.0",
)

# Criando um router padrão para a API
router = DefaultRouter()

urlpatterns = [
    # Página inicial mostra a interface do DRF
    path('', include('core.urls')),
    
    path('admin/', admin.site.urls),
    path('api/auth/', include('djoser.urls')),
    path('api/auth/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/auth/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/projects/', include('projects.urls')),
    path('api/tasks/', include('tasks.urls')),
    path('api/teams/', include('teams.urls')),
    path('api/communications/', include('communications.urls')),
    path('api/risks/', include('risks.urls')),
    path('api/costs/', include('costs.urls')),
    path('api/documents/', include('documents.urls')),
    path('api/', include('core.urls')),
    
    # DRF documentation URLs
    path('api/schema/', schema_view, name='openapi-schema'),
    path('api/docs/', include_docs_urls(
        title='Documentação da API Planify',
        description='API do sistema Planify para gerenciamento de projetos',
        authentication_classes=[],
        permission_classes=[],
        public=True,
    )),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
