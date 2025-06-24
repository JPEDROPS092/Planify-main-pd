# tests/conftest.py (add these to your existing conftest.py or a new one)
import pytest
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from datetime import datetime, timezone # Keep existing imports like Decimal, date if needed by other tests
from django.core.files.uploadedfile import SimpleUploadedFile # For file uploads

# Assuming your app is 'comunicacoes'
# from comunicacoes.models import ChatMensagem, ChatMensagemLeitura, Notificacao, ConfiguracaoNotificacao, Comunicacao

# Keep existing User, APIClient, Projeto, Tarefa factories
# ... (UserFactory, authenticated_user, authenticated_client, api_client)
# ... (projeto_factory, tarefa_factory)

User = get_user_model()


@pytest.fixture
def chat_mensagem_factory(db, projeto_factory, authenticated_user):
    from comunicacoes.models import ChatMensagem # Adjust import path
    def create_chat_mensagem(projeto=None, autor=None, **kwargs):
        if projeto is None:
            projeto = projeto_factory()
        if autor is None:
            autor = authenticated_user
        defaults = {
            "projeto": projeto,
            "autor": autor,
            "texto": "Test chat message content.",
        }
        defaults.update(kwargs)
        return ChatMensagem.objects.create(**defaults)
    return create_chat_mensagem

@pytest.fixture
def chat_mensagem_leitura_factory(db, chat_mensagem_factory, authenticated_user):
    from comunicacoes.models import ChatMensagemLeitura # Adjust import path
    def create_chat_mensagem_leitura(mensagem=None, usuario=None, **kwargs):
        if mensagem is None:
            mensagem = chat_mensagem_factory()
        if usuario is None:
            # Create a different user for reading to avoid self-read scenarios by default
            usuario = User.objects.create_user(username=f"reader_user_{User.objects.count()}", password="password")

        defaults = {
            "mensagem": mensagem,
            "usuario": usuario,
        }
        defaults.update(kwargs)
        # Handle unique_together: (mensagem, usuario)
        instance, created = ChatMensagemLeitura.objects.get_or_create(
            mensagem=defaults.pop('mensagem'),
            usuario=defaults.pop('usuario'),
            defaults=defaults
        )
        return instance
    return create_chat_mensagem_leitura


@pytest.fixture
def notificacao_factory(db, authenticated_user, projeto_factory, tarefa_factory):
    from comunicacoes.models import Notificacao # Adjust import path
    def create_notificacao(usuario=None, projeto=None, tarefa=None, **kwargs):
        if usuario is None:
            usuario = authenticated_user
        # projeto and tarefa can be None
        defaults = {
            "usuario": usuario,
            "tipo": "SISTEMA",
            "titulo": "Test Notification Title",
            "mensagem": "This is a test notification message.",
            "prioridade": "MEDIA",
            "projeto": projeto,
            "tarefa": tarefa,
        }
        defaults.update(kwargs)
        return Notificacao.objects.create(**defaults)
    return create_notificacao


@pytest.fixture
def configuracao_notificacao_factory(db, authenticated_user):
    from comunicacoes.models import ConfiguracaoNotificacao # Adjust import path
    def create_configuracao_notificacao(usuario=None, **kwargs):
        if usuario is None:
            usuario = authenticated_user
        defaults = {
            "usuario": usuario,
            "tarefa_atribuida": "AMBOS",
            "mensagem_chat": "SISTEMA",
            # Add other defaults as needed
        }
        defaults.update(kwargs)
        # Handle OneToOneField: usuario
        instance, created = ConfiguracaoNotificacao.objects.get_or_create(
            usuario=defaults.pop('usuario'),
            defaults=defaults
        )
        return instance
    return create_configuracao_notificacao


@pytest.fixture
def comunicacao_factory(db, projeto_factory, authenticated_user):
    from comunicacoes.models import Comunicacao # Adjust import path
    def create_comunicacao(projeto=None, remetente=None, destinatarios_users=None, **kwargs):
        if projeto is None:
            projeto = projeto_factory()
        if remetente is None:
            remetente = authenticated_user

        defaults = {
            "projeto": projeto,
            "tipo": "COMUNICADO",
            "titulo": "Test Formal Communication",
            "texto": "Detailed content of the formal communication.",
            "remetente": remetente,
        }
        defaults.update(kwargs)
        com = Comunicacao.objects.create(**defaults)
        if destinatarios_users:
            com.destinatarios.set(destinatarios_users)
        return com
    return create_comunicacao