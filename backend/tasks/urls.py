from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import TarefaViewSet

# Define the app name to support namespace in include()
app_name = "tasks"

router = DefaultRouter()
router.register(r"tarefas", TarefaViewSet, basename="tarefas")

urlpatterns = [
    path("", include(router.urls)),
]
