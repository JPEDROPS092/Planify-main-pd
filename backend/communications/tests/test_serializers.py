import pytest
from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile

# Assuming your app is 'comunicacoes'
from comunicacoes.models import (
    ChatMensagem, ChatMensagemLeitura, Notificacao,
    ConfiguracaoNotificacao, Comunicacao
)
from comunicacoes.serializers import (
    ChatMensagemSerializer, ChatMensagemLeituraSerializer,
    NotificacaoSerializer, ConfiguracaoNotificacaoSerializer,
    ComunicacaoSerializer
)

User = get_user_model()
pytestmark = pytest.mark.django_db

class TestChatMensagemSerializer:
    def test_serialize_chat_mensagem(self, chat_mensagem_factory, chat_mensagem_leitura_factory, authenticated_user, projeto_factory, user_factory):
        proj = projeto_factory(name="Project Serializer Test") # Ensure 'name' is used by serializer
        author = authenticated_user
        # author.full_name = "Author FullName" # Set if you want to test autor_nome
        # author.save()

        msg = chat_mensagem_factory(
            projeto=proj,
            autor=author,
            texto="Serializing this message.",
            anexo=SimpleUploadedFile("test_attach.pdf", b"%PDF-", content_type="application/pdf")
        )
        reader1 = user_factory(username="reader_s1")
        # reader1.full_name = "Reader One FullName"
        # reader1.save()
        chat_mensagem_leitura_factory(mensagem=msg, usuario=reader1)

        serializer = ChatMensagemSerializer(msg)
        data = serializer.data

        assert data['id'] == msg.id
        assert data['projeto'] == proj.id
        assert data['projeto_nome'] == proj.name # Check 'projeto.name' or 'projeto.titulo' based on your Projeto model
        assert data['autor'] == author.id
        # assert data['autor_nome'] == "Author FullName"
        assert data['autor_username'] == author.username
        assert data['texto'] == "Serializing this message."
        assert "test_attach.pdf" in data['anexo']
        assert len(data['leituras']) == 1
        assert data['leituras'][0]['usuario'] == reader1.id
        # assert data['leituras'][0]['usuario_nome'] == "Reader One FullName"

    def test_deserialize_chat_mensagem_valid(self, projeto_factory, authenticated_user):
        proj = projeto_factory()
        data = {
            "projeto": proj.id,
            "texto": "New message from API."
            # 'autor' will be set by perform_create
        }
        serializer = ChatMensagemSerializer(data=data, context={'request': type('Request', (), {'user': authenticated_user})})
        assert serializer.is_valid(), serializer.errors
        msg = serializer.save(autor=authenticated_user) # Pass autor explicitly if not using perform_create context correctly
        assert msg.texto == "New message from API."
        assert msg.autor == authenticated_user
        assert msg.projeto == proj

class TestNotificacaoSerializer:
    def test_serialize_notificacao(self, notificacao_factory, authenticated_user, projeto_factory, tarefa_factory):
        user = authenticated_user
        proj = projeto_factory(name="Notif Project S") # Ensure 'name' for serializer
        task = tarefa_factory(titulo="Notif Task S")  # Ensure 'titulo' for serializer
        notif = notificacao_factory(
            usuario=user,
            projeto=proj,
            tarefa=task,
            tipo="TAREFA",
            prioridade="ALTA",
            titulo="Urgent Task Update",
            lida=True
        )
        serializer = NotificacaoSerializer(notif)
        data = serializer.data

        assert data['id'] == notif.id
        assert data['tipo'] == "TAREFA"
        assert data['tipo_display'] == "Tarefa"
        assert data['prioridade'] == "ALTA"
        assert data['prioridade_display'] == "Alta"
        assert data['projeto'] == proj.id
        assert data['projeto_nome'] == proj.name
        assert data['tarefa'] == task.id
        assert data['tarefa_titulo'] == task.titulo
        assert data['lida'] is True

class TestConfiguracaoNotificacaoSerializer:
    def test_serialize_configuracao_notificacao(self, configuracao_notificacao_factory, authenticated_user):
        user = authenticated_user
        # user.full_name = "Config User FullName"
        # user.save()
        config = configuracao_notificacao_factory(usuario=user, tarefa_prazo="EMAIL")
        serializer = ConfiguracaoNotificacaoSerializer(config)
        data = serializer.data
        assert data['id'] == config.id
        assert data['usuario'] == user.id
        # assert data['usuario_nome'] == "Config User FullName"
        assert data['tarefa_prazo'] == "EMAIL"

    def test_create_or_update_configuracao(self, authenticated_user):
        # Test create
        data_create = {"usuario": authenticated_user.id, "mensagem_chat": "AMBOS"}
        serializer_create = ConfiguracaoNotificacaoSerializer(data=data_create)
        assert serializer_create.is_valid(), serializer_create.errors
        config1 = serializer_create.save()
        assert config1.usuario == authenticated_user
        assert config1.mensagem_chat == "AMBOS"

        # Test update (using the same serializer logic for create/update)
        data_update = {"usuario": authenticated_user.id, "mensagem_chat": "NENHUM", "tarefa_atribuida": "SISTEMA"}
        serializer_update = ConfiguracaoNotificacaoSerializer(instance=config1, data=data_update, partial=True)
        assert serializer_update.is_valid(), serializer_update.errors
        config_updated = serializer_update.save() # Serializer's create method handles update
        
        assert config_updated.id == config1.id
        assert config_updated.mensagem_chat == "NENHUM"
        assert config_updated.tarefa_atribuida == "SISTEMA"


class TestComunicacaoSerializer:
    def test_serialize_comunicacao(self, comunicacao_factory, authenticated_user, projeto_factory, user_factory):
        proj = projeto_factory(name="Comm Proj S")
        sender = authenticated_user
        # sender.full_name = "Sender FullName"
        # sender.save()

        recipient1 = user_factory(username="comm_rec_1")
        # recipient1.full_name = "Recipient One Comm"
        # recipient1.save()
        recipient2 = user_factory(username="comm_rec_2")
        # recipient2.full_name = "Recipient Two Comm"
        # recipient2.save()

        com = comunicacao_factory(
            projeto=proj,
            remetente=sender,
            destinatarios_users=[recipient1, recipient2],
            tipo="RELATORIO",
            titulo="Monthly Report"
        )
        serializer = ComunicacaoSerializer(com)
        data = serializer.data

        assert data['id'] == com.id
        assert data['projeto_nome'] == proj.name
        assert data['tipo'] == "RELATORIO"
        assert data['tipo_display'] == "Relatório"
        # assert data['remetente_nome'] == "Sender FullName"
        assert data['remetente_username'] == sender.username
        assert len(data['destinatarios']) == 2 # List of IDs
        assert recipient1.id in data['destinatarios']
        assert len(data['destinatarios_info']) == 2
        dest_info_usernames = {info['username'] for info in data['destinatarios_info']}
        assert recipient1.username in dest_info_usernames
        assert recipient2.username in dest_info_usernames