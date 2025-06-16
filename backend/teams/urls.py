from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import EquipeViewSet, PermissaoEquipeViewSet

router = DefaultRouter()
router.register(r'equipes', EquipeViewSet, basename='equipe')
router.register(r'permissoes', PermissaoEquipeViewSet, basename='permissao-equipe')

urlpatterns = [
    path('', include(router.urls)),
]
