from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenRefreshView
from .views import (
    UserViewSet, UserProfileViewSet, AccessProfileViewSet, 
    PermissionViewSet, UserAccessProfileViewSet,
    ForgotPasswordView, ResetPasswordConfirmView
)
from .auth_views import CustomTokenObtainPairView

router = DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'profiles', UserProfileViewSet, basename='profile')
router.register(r'access-profiles', AccessProfileViewSet)
router.register(r'permissions', PermissionViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('token/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('forgot-password/', ForgotPasswordView.as_view(), name='forgot_password'),
    path('reset-password/', ResetPasswordConfirmView.as_view(), name='reset_password'),
    path('users/<int:user_pk>/access-profiles/', UserAccessProfileViewSet.as_view({'get': 'list', 'post': 'create'}), name='user-access-profiles'),
    path('users/<int:user_pk>/access-profiles/<int:pk>/', UserAccessProfileViewSet.as_view({'get': 'retrieve', 'put': 'update', 'patch': 'partial_update', 'delete': 'destroy'}), name='user-access-profile-detail'),
]
