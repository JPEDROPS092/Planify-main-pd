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
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework import permissions
from drf_spectacular.views import SpectacularAPIView, SpectacularRedocView, SpectacularSwaggerView
# Criando um router padrão para a API
router = DefaultRouter()

# View para redirecionar a raiz para a documentação da API
def redirect_to_api_docs(request):
    return redirect('/api/schema/swagger-ui/')

urlpatterns = [
    # Rota raiz
    path('', redirect_to_api_docs, name='api-docs-redirect'),
    
    # Admin do Django
    path('admin/', admin.site.urls),
    
    # Rotas da API - todas consolidadas sob o prefixo api/
    path('api/auth/', include('djoser.urls')),
    path('api/auth/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/auth/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/users/', include('users.urls')),
    path('api/projects/', include('projects.urls')),
    path('api/tasks/', include('tasks.urls')),
    path('api/teams/', include('teams.urls')),
    path('api/communications/', include('communications.urls')),
    path('api/risks/', include('risks.urls')),
    path('api/costs/', include('costs.urls')),
    path('api/documents/', include('documents.urls')),
    path('api/', include('core.urls', namespace='api-core')),
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/schema/swagger-ui/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('api/schema/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
    
   
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
