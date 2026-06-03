from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ProjetoViewSet, SprintViewSet, HistoricoStatusProjetoViewSet

app_name = 'projects'

router = DefaultRouter()
# Rotas específicas precisam ser registradas ANTES do prefixo vazio do
# ProjetoViewSet; caso contrário /sprints/ e /historico-status/ seriam
# capturados pelo detail do projeto (pk='sprints').
router.register(r'sprints', SprintViewSet, basename='sprints')
router.register(r'historico-status', HistoricoStatusProjetoViewSet, basename='historico-status')
router.register(r'', ProjetoViewSet, basename='projects')

urlpatterns = [
    # Inclui as rotas do router
    path('', include(router.urls)),
]
