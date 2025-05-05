from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import EquipeViewSet, MembroEquipeViewSet, PermissaoEquipeViewSet

router = DefaultRouter()
router.register(r'equipes', EquipeViewSet)
router.register(r'membros', MembroEquipeViewSet)
router.register(r'permissoes', PermissaoEquipeViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
