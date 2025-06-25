from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ProjetoViewSet, SprintViewSet, HistoricoStatusProjetoViewSet

app_name = 'projects'

router = DefaultRouter()
router.register(r'projects', ProjetoViewSet, basename='project')
router.register(r'sprints', SprintViewSet, basename='sprint')
router.register(r'history', HistoricoStatusProjetoViewSet, basename='history')

urlpatterns = [
    # Only include router URLs for cleaner structure
    path('', include(router.urls)),
]
