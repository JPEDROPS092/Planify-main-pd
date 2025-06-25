from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import DocumentoViewSet, HistoricoDocumentoViewSet, ComentarioViewSet

# Define the app name to support namespace in include()
app_name = 'documents'

router = DefaultRouter()
router.register(r'', DocumentoViewSet)
router.register(r'historico', HistoricoDocumentoViewSet)
router.register(r'comentarios', ComentarioViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
