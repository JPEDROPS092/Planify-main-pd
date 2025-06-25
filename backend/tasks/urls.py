from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import TarefaViewSet, AtribuicaoTarefaViewSet, ComentarioTarefaViewSet

# Define the app name to support namespace in include()
app_name = 'tasks'

router = DefaultRouter()
router.register(r'tarefas', TarefaViewSet, basename='tarefas')
router.register(r'atribuicoes', AtribuicaoTarefaViewSet, basename='atribuicoes')
router.register(r'comentarios', ComentarioTarefaViewSet, basename='comentarios')

urlpatterns = [
    path('', include(router.urls)),
]
