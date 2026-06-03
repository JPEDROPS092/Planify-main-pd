from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    ChatMensagemViewSet,
    NotificacaoViewSet,
    ConfiguracaoNotificacaoViewSet,
    ComunicacaoViewSet,
)

router = DefaultRouter()
router.register(r'mensagens', ChatMensagemViewSet)
router.register(r'notificacoes', NotificacaoViewSet, basename='notificacao')
router.register(r'configuracoes', ConfiguracaoNotificacaoViewSet, basename='configuracao')
router.register(r'comunicacoes', ComunicacaoViewSet, basename='comunicacao')

urlpatterns = [
    path('', include(router.urls)),
]
