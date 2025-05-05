from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ChatMensagemViewSet, NotificacaoViewSet, ConfiguracaoNotificacaoViewSet

router = DefaultRouter()
router.register(r'mensagens', ChatMensagemViewSet)
router.register(r'notificacoes', NotificacaoViewSet, basename='notificacao')
router.register(r'configuracoes', ConfiguracaoNotificacaoViewSet, basename='configuracao')

urlpatterns = [
    path('', include(router.urls)),
]
