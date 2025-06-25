from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import EquipeViewSet, PermissaoEquipeViewSet

# Define the app name to support namespace in include()
app_name = 'teams'

router = DefaultRouter()
router.register(r'equipes', EquipeViewSet, basename='equipe')
router.register(r'permissoes', PermissaoEquipeViewSet, basename='permissaoequipe')

urlpatterns = [
    path('', include(router.urls)),
]
