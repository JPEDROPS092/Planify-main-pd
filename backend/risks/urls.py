from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import RiscoViewSet, HistoricoRiscoViewSet

router = DefaultRouter()
router.register(r'riscos', RiscoViewSet)
router.register(r'historico', HistoricoRiscoViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
