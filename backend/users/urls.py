from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenRefreshView
from .views import (
    UserViewSet, UserProfileViewSet, AccessProfileViewSet, 
    PermissionViewSet, UserAccessProfileViewSet
)
from .auth_views import CustomTokenObtainPairView

router = DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'profiles', UserProfileViewSet, basename='profile')
router.register(r'access-profiles', AccessProfileViewSet)
router.register(r'permissions', PermissionViewSet)

urlpatterns = [
    # Rotas de autenticação
    path('token/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    
    # Rotas de API
    path('', include(router.urls)),
]
