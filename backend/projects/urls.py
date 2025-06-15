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
    # Rotas para dashboard, kanban e gantt
    path('<int:projeto_id>/dashboard/', ProjetoDashboardView.as_view(), name='projeto-dashboard'),
    path('<int:projeto_id>/kanban/', ProjetoKanbanView.as_view(), name='projeto-kanban'),
    path('<int:projeto_id>/gantt/', ProjetoGanttView.as_view(), name='projeto-gantt'),
    # Rotas para criação de tarefas
    path('<int:projeto_id>/tarefas/criar/', ProjetoTarefaCreateView.as_view(), name='projeto-criar-tarefa'),
    path('<int:projeto_id>/tarefas/criar-multiplas/', ProjetoTarefasBulkCreateView.as_view(), name='projeto-criar-tarefas-multiplas'),
    # Rota para exportação de dados
    path('<int:projeto_id>/exportar/', ProjetoExportView.as_view(), name='projeto-exportar'),
]
