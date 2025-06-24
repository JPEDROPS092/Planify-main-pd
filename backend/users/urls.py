from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    UserViewSet, UserProfileViewSet, PermissionViewSet
)
from .authentication import LoginView, LogoutView, CustomTokenRefreshView


app_name = 'users'

# Configuração do router para ViewSets
router = DefaultRouter()
router.register(r'users', UserViewSet, basename='user')
router.register(r'profiles', UserProfileViewSet, basename='profile')
router.register(r'permissions', PermissionViewSet, basename='permission')

# URLs para autenticação
auth_urlpatterns = [
    path('login/', LoginView.as_view(), name='login'),
    path('token/refresh/', CustomTokenRefreshView.as_view(), name='token_refresh'),
    path('logout/', LogoutView.as_view(), name='logout'),
]

# URLs para autenticação e gerenciamento de usuários
urlpatterns = [
    # Inclusão das rotas automáticas do router
    path('', include(router.urls)),
    
    # Authentication endpoints with namespace
    path('auth/', include((auth_urlpatterns, 'auth'), namespace='auth')),
]
