# users/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ( # Supondo que você tem esses ViewSets
    UserViewSet, UserProfileViewSet, AccessProfileViewSet, PermissionViewSet
)
from .authentication import LoginView, LogoutView, CustomTokenRefreshView


app_name = 'users'

router = DefaultRouter()
router.register(r'users', UserViewSet, basename='user') # URL final: /api/users/users/
router.register(r'profiles', UserProfileViewSet, basename='userprofile') # URL final: /api/users/profiles/
router.register(r'access-profiles', AccessProfileViewSet, basename='accessprofile') # URL final: /api/users/access-profiles/
router.register(r'permissions', PermissionViewSet, basename='permission') # URL final: /api/users/permissions/

auth_patterns = [
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('token/refresh/', CustomTokenRefreshView.as_view(), name='token_refresh'),
    path('register/', RegisterView.as_view(), name='register'),
]

urlpatterns = [
    # URLs do router (users, profiles, etc.) estarão diretamente sob /api/users/
    path('', include(router.urls)),

    # URLs de autenticação estarão sob /api/users/auth/
    path('auth/', include(auth_patterns)),
]