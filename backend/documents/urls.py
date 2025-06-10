from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import DocumentoViewSet, HistoricoDocumentoViewSet, ComentarioViewSet

router = DefaultRouter()
router.register(r'', DocumentoViewSet, basename='documents')
router.register(r'historic', HistoricoDocumentoViewSet)
router.register(r'comments', ComentarioViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
