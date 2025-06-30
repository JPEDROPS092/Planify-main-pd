# users/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    UserViewSet, UserProfileViewSet, AccessProfileViewSet, PermissionViewSet
)

app_name = 'users'

# Router para administração de usuários (funcionalidades específicas não cobertas pelo djoser)
admin_router = DefaultRouter()
admin_router.register(r'profiles', UserProfileViewSet, basename='profile') 
admin_router.register(r'access-profiles', AccessProfileViewSet, basename='accessprofile') 
admin_router.register(r'permissions', PermissionViewSet, basename='permission') 

# Router para operações administrativas avançadas de usuários
user_admin_router = DefaultRouter()
user_admin_router.register(r'', UserViewSet, basename='user-admin')

urlpatterns = [
    # URLs de administração avançada de usuários estarão sob /api/users/admin/
    # Estas são funcionalidades específicas que o djoser não cobre
    path('admin/', include([
        path('users/', include(user_admin_router.urls)),  # /api/users/admin/users/
        path('', include(admin_router.urls)),  # /api/users/admin/profiles/, etc.
    ])),
    
    # NOTA: URLs de autenticação básica agora estão em /api/auth/ via djoser
    # - POST /api/auth/users/ (registro)
    # - GET/PUT/PATCH /api/auth/users/me/ (perfil do usuário logado)
    # - POST /api/auth/users/set_password/ (trocar senha)
    # - POST /api/auth/jwt/create/ (login)
    # - POST /api/auth/jwt/refresh/ (refresh token)
    # - POST /api/auth/jwt/verify/ (verificar token)
]