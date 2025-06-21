from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    UserViewSet, UserProfileViewSet, PermissionViewSet
)



# Configuração do router para ViewSets
router = DefaultRouter()
router.register(r'users', UserViewSet, basename='user')
router.register(r'profiles', UserProfileViewSet, basename='profile')
router.register(r'permissions', PermissionViewSet, basename='permission')

# URLs para autenticação e gerenciamento de usuários
urlpatterns = [
    # Inclusão das rotas automáticas do router
    path('', include(router.urls)),
    
    # Authentication endpoints
    path('login/', LoginView.as_view(), name='login'),
    path('token/refresh/', CustomTokenRefreshView.as_view(), name='token_refresh'),
    path('logout/', LogoutView.as_view(), name='logout'),
    
    # User specific endpoints
    path('users/me/', UserViewSet.as_view({'get': 'me'}), name='user-me'),
    path('users/permissions/', UserViewSet.as_view({'get': 'permissions'}), name='user-permissions'),
    path('users/change-password/', UserViewSet.as_view({'post': 'change_password'}), name='user-change-password'),
    
    # User management actions
    path('users/<int:pk>/activate/', UserViewSet.as_view({'post': 'activate'}), name='user-activate'),
    path('users/<int:pk>/deactivate/', UserViewSet.as_view({'post': 'deactivate'}), name='user-deactivate'),
    path('users/<int:pk>/unlock/', UserViewSet.as_view({'post': 'unlock'}), name='user-unlock'),
    path('users/<int:pk>/reset-password/', UserViewSet.as_view({'post': 'reset_password'}), name='user-reset-password'),
]
