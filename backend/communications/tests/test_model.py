import pytest
from django.core.exceptions import ValidationError
from django.utils import timezone
from django.core.files.uploadedfile import SimpleUploadedFile

# Assuming your app is 'comunicacoes'
from comunicacoes.models import (
    ChatMensagem, ChatMensagemLeitura, Notificacao,
    ConfiguracaoNotificacao, Comunicacao
)

pytestmark = pytest.mark.django_db

class TestChatMensagemModel:
    def test_chat_mensagem_creation(self, chat_mensagem_factory, projeto_factory, authenticated_user):
        proj = projeto_factory(titulo="Chat Project")
        user = authenticated_user
        msg = chat_mensagem_factory(
            projeto=proj,
            autor=user,
            texto="Hello world!",
            anexo=SimpleUploadedFile("file.txt", b"file_content", content_type="text/plain")
        )
        assert msg.projeto == proj
        assert msg.autor == user
        assert msg.texto == "Hello world!"
        assert msg.anexo is not None
        assert "file.txt" in msg.anexo.name
        assert str(msg) == f"Mensagem de {user.username} em {proj.titulo}"
        assert ChatMensagem.objects.count() == 1
        assert not msg.editado
        assert msg.enviado_em is not None

class TestChatMensagemLeituraModel:
    def test_chat_mensagem_leitura_creation(self, chat_mensagem_leitura_factory, chat_mensagem_factory, authenticated_user, user_factory):
        msg = chat_mensagem_factory()
        reader = user_factory(username="reader1")
        leitura = chat_mensagem_leitura_factory(mensagem=msg, usuario=reader)

        assert leitura.mensagem == msg
        assert leitura.usuario == reader
        assert leitura.lido_em is not None
        assert str(leitura) == f"Mensagem de {msg.autor.username} em {msg.projeto.titulo} lida por {reader.username}"
        assert ChatMensagemLeitura.objects.count() == 1

    def test_unique_together_mensagem_usuario(self, chat_mensagem_factory, authenticated_user, user_factory):
        msg = chat_mensagem_factory()
        reader = user_factory(username="reader2")
        ChatMensagemLeitura.objects.create(mensagem=msg, usuario=reader)
        with pytest.raises(Exception): # Django raises IntegrityError, DRF might raise others
            ChatMensagemLeitura.objects.create(mensagem=msg, usuario=reader)

class TestNotificacaoModel:
    def test_notificacao_creation(self, notificacao_factory, authenticated_user, projeto_factory):
        user = authenticated_user
        proj = projeto_factory(titulo="Notif Project")
        notif = notificacao_factory(
            usuario=user,
            tipo="PROJETO",
            titulo="Project Update",
            mensagem="Project status changed.",
            prioridade="ALTA",
            projeto=proj,
            url="https://example.com/project/1"
        )
        assert notif.usuario == user
        assert notif.tipo == "PROJETO"
        assert notif.titulo == "Project Update"
        assert notif.prioridade == "ALTA"
        assert notif.projeto == proj
        assert notif.url == "https://example.com/project/1"
        assert not notif.lida
        assert notif.lida_em is None
        assert str(notif) == f"Projeto: Project Update para {user.username}"
        assert Notificacao.objects.count() == 1

    def test_notificacao_url_validation_valid(self, notificacao_factory):
        notif = notificacao_factory(url="http://valid.com/path")
        notif.full_clean() # Should not raise ValidationError
        assert notif.url == "http://valid.com/path"

    def test_notificacao_url_validation_invalid(self, notificacao_factory):
        with pytest.raises(ValidationError) as excinfo:
            notif = notificacao_factory(url="invalid-url")
            notif.full_clean()
        assert 'url' in excinfo.value.message_dict
        assert "URL inválida" in excinfo.value.message_dict['url'][0]

class TestConfiguracaoNotificacaoModel:
    def test_configuracao_notificacao_creation(self, configuracao_notificacao_factory, authenticated_user):
        user = authenticated_user
        config = configuracao_notificacao_factory(
            usuario=user,
            tarefa_atribuida="EMAIL",
            mensagem_chat="NENHUM"
        )
        assert config.usuario == user
        assert config.tarefa_atribuida == "EMAIL"
        assert config.mensagem_chat == "NENHUM"
        assert str(config) == f"Configurações de notificação para {user.username}"
        assert ConfiguracaoNotificacao.objects.count() == 1

    def test_one_to_one_usuario_config(self, authenticated_user, configuracao_notificacao_factory):
        configuracao_notificacao_factory(usuario=authenticated_user)
        with pytest.raises(Exception): # IntegrityError
            configuracao_notificacao_factory(usuario=authenticated_user)

class TestComunicacaoModel:
    def test_comunicacao_creation(self, comunicacao_factory, projeto_factory, authenticated_user, user_factory):
        proj = projeto_factory(titulo="Comm Project")
        sender = authenticated_user
        recipient1 = user_factory(username="recipient_a")
        recipient2 = user_factory(username="recipient_b")

        com = comunicacao_factory(
            projeto=proj,
            remetente=sender,
            destinatarios_users=[recipient1, recipient2],
            tipo="ATA",
            titulo="Meeting Minutes",
            texto="Summary of the meeting."
        )
        assert com.projeto == proj
        assert com.remetente == sender
        assert com.tipo == "ATA"
        assert com.titulo == "Meeting Minutes"
        assert Comunicacao.objects.count() == 1
        assert com.destinatarios.count() == 2
        assert recipient1 in com.destinatarios.all()
        assert str(com) == "Meeting Minutes"