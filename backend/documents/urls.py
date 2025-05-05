from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import DocumentoViewSet, HistoricoDocumentoViewSet, ComentarioViewSet

router = DefaultRouter()
router.register(r'documentos', DocumentoViewSet)
router.register(r'historico', HistoricoDocumentoViewSet)
router.register(r'comentarios', ComentarioViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
