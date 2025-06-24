from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ComunicacaoViewSet, ChatMensagemViewSet, NotificacaoViewSet, ConfiguracaoNotificacaoViewSet

router = DefaultRouter()
router.register(r'mensagens', ChatMensagemViewSet, basename='chatmensagem') # Added basename for clarity
router.register(r'notificacoes', NotificacaoViewSet, basename='notificacao')
router.register(r'configuracoes', ConfiguracaoNotificacaoViewSet, basename='configuracao')
router.register(r'comunicacoes', ComunicacaoViewSet, basename='comunicacao') # Register ComunicacaoViewSet

urlpatterns = [
    path('', include(router.urls)),
]
