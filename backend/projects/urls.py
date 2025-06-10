from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ProjetoViewSet
from .project_dashboard_views import ProjetoDashboardView, ProjetoKanbanView, ProjetoGanttView
from .task_creation_views import ProjetoTarefaCreateView, ProjetoTarefasBulkCreateView
from .export_views import ProjetoExportView

app_name = 'projects'

router = DefaultRouter()
router.register(r'', ProjetoViewSet, basename='projects')

urlpatterns = [
    # Inclui as rotas do router
    path('', include(router.urls)),
]
