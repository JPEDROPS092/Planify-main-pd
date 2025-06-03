from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    CategoriaViewSet, CustoViewSet, OrcamentoProjetoViewSet, 
    OrcamentoTarefaViewSet, AlertaViewSet
)

router = DefaultRouter()
router.register(r'categorias', CategoriaViewSet)
router.register(r'custos', CustoViewSet)
router.register(r'orcamentos-projeto', OrcamentoProjetoViewSet)
router.register(r'orcamentos-tarefa', OrcamentoTarefaViewSet, basename='orcamentotarefa')
router.register(r'alertas', AlertaViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
