from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ComunicacaoViewSet, ChatMensagemViewSet, NotificacaoViewSet, ConfiguracaoNotificacaoViewSet

# Define the app name to support namespace in include()
app_name = 'communications'

router = DefaultRouter()
router.register(r'mensagens', ChatMensagemViewSet, basename='chatmensagem') # Added basename for clarity
router.register(r'notificacoes', NotificacaoViewSet, basename='notificacao')
router.register(r'configuracoes', ConfiguracaoNotificacaoViewSet, basename='configuracao')
router.register(r'', ComunicacaoViewSet, basename='comunicacao') # Register ComunicacaoViewSet

urlpatterns = [
    path('', include(router.urls)),
]
