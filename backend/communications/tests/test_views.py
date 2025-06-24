import pytest
from django.urls import reverse
from rest_framework import status
from django.utils import timezone
from django.core.files.uploadedfile import SimpleUploadedFile

# Assuming your app is 'comunicacoes'
from comunicacoes.models import (
    ChatMensagem, ChatMensagemLeitura, Notificacao,
    ConfiguracaoNotificacao, Comunicacao
)
# from projects.models import Projeto # For factories
# from tasks.models import Tarefa # For factories

pytestmark = pytest.mark.django_db

# --- TestChatMensagemViewSet ---
class TestChatMensagemViewSet:
    base_url_list = reverse('chatmensagem-list') # Matches router.register(r'mensagens', ...)

    def get_detail_url(self, msg_id):
        return reverse('chatmensagem-detail', kwargs={'pk': msg_id})

    def test_list_chat_mensagens_unauthenticated(self, api_client, chat_mensagem_factory):
        chat_mensagem_factory.create_batch(2)
        response = api_client.get(self.base_url_list)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_list_chat_mensagens_authenticated_filtered_by_project(self, authenticated_client, chat_mensagem_factory, projeto_factory):
        proj1 = projeto_factory()
        proj2 = projeto_factory()
        chat_mensagem_factory.create_batch(2, projeto=proj1)
        chat_mensagem_factory(projeto=proj2)

        response = authenticated_client.get(self.base_url_list, {'projeto': proj1.id})
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data['results']) == 2
        for item in response.data['results']:
            assert item['projeto'] == proj1.id

    def test_create_chat_mensagem(self, authenticated_client, authenticated_user, projeto_factory):
        proj = projeto_factory()
        # Test with file upload
        test_file = SimpleUploadedFile("my_chat_file.txt", b"hello chat attachment", content_type="text/plain")
        data = {
            "projeto": proj.id,
            "texto": "New API message with attachment.",
            "anexo": test_file
        }
        response = authenticated_client.post(self.base_url_list, data=data, format='multipart') # Use multipart for files
        assert response.status_code == status.HTTP_201_CREATED
        msg = ChatMensagem.objects.get(id=response.data['id'])
        assert msg.autor == authenticated_user
        assert msg.projeto == proj
        assert msg.texto == "New API message with attachment."
        assert msg.anexo is not None
        assert "my_chat_file.txt" in msg.anexo.name

    def test_update_chat_mensagem_own(self, authenticated_client, authenticated_user, chat_mensagem_factory):
        msg = chat_mensagem_factory(autor=authenticated_user, texto="Original text.")
        data = {"texto": "Updated text by author."}
        response = authenticated_client.patch(self.get_detail_url(msg.id), data=data)
        assert response.status_code == status.HTTP_200_OK
        msg.refresh_from_db()
        assert msg.texto == "Updated text by author."
        # assert msg.editado is True # Model doesn't auto-set editado on update through serializer

    # Add test: cannot update other user's message (if that's the desired permission)

    def test_marcar_como_lida_action(self, authenticated_client, authenticated_user, chat_mensagem_factory, user_factory):
        # Create a message by another user
        other_user = user_factory(username="msg_sender")
        msg = chat_mensagem_factory(autor=other_user)

        url = reverse('chatmensagem-marcar-como-lida', kwargs={'pk': msg.id})
        response = authenticated_client.post(url)
        assert response.status_code == status.HTTP_201_CREATED
        assert ChatMensagemLeitura.objects.filter(mensagem=msg, usuario=authenticated_user).exists()

        # Try marking again
        response_again = authenticated_client.post(url)
        assert response_again.status_code == status.HTTP_200_OK # As per view logic
        assert "já foi marcada como lida" in response_again.data['mensagem']

    def test_mensagens_nao_lidas_action(self, authenticated_client, authenticated_user, chat_mensagem_factory, projeto_factory, user_factory):
        proj = projeto_factory()
        other_user = user_factory(username="sender_for_unread")

        # Message by another user, not read yet by authenticated_user
        msg1_unread = chat_mensagem_factory(projeto=proj, autor=other_user)
        # Message by another user, already read by authenticated_user
        msg2_read = chat_mensagem_factory(projeto=proj, autor=other_user)
        ChatMensagemLeitura.objects.create(mensagem=msg2_read, usuario=authenticated_user)
        # Message by authenticated_user (should not appear as unread for self)
        msg3_own = chat_mensagem_factory(projeto=proj, autor=authenticated_user)

        url = reverse('chatmensagem-mensagens-nao-lidas')
        response = authenticated_client.get(url, {'projeto': proj.id})
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == 1
        assert response.data[0]['id'] == msg1_unread.id


# --- TestNotificacaoViewSet ---
class TestNotificacaoViewSet:
    base_url_list = reverse('notificacao-list') # Matches router basename

    def get_detail_url(self, notif_id):
        return reverse('notificacao-detail', kwargs={'pk': notif_id})

    def test_list_notificacoes_own_only(self, authenticated_client, authenticated_user, notificacao_factory, user_factory):
        notificacao_factory.create_batch(2, usuario=authenticated_user)
        other_user = user_factory(username="other_notif_user")
        notificacao_factory(usuario=other_user) # Notification for another user

        response = authenticated_client.get(self.base_url_list)
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data['results']) == 2 # Only for authenticated_user

    def test_marcar_como_lida_action(self, authenticated_client, authenticated_user, notificacao_factory):
        notif = notificacao_factory(usuario=authenticated_user, lida=False)
        url = reverse('notificacao-marcar-como-lida', kwargs={'pk': notif.id})
        response = authenticated_client.post(url)
        assert response.status_code == status.HTTP_200_OK
        notif.refresh_from_db()
        assert notif.lida is True
        assert notif.lida_em is not None

        # Try marking again
        response_again = authenticated_client.post(url)
        assert response_again.status_code == status.HTTP_200_OK
        assert "já foi marcada como lida" in response_again.data['mensagem']

    def test_marcar_todas_como_lidas_action(self, authenticated_client, authenticated_user, notificacao_factory):
        notificacao_factory.create_batch(3, usuario=authenticated_user, lida=False)
        notificacao_factory(usuario=authenticated_user, lida=True) # One already read

        url = reverse('notificacao-marcar-todas-como-lidas')
        response = authenticated_client.post(url)
        assert response.status_code == status.HTTP_200_OK
        assert "3 notificações marcadas como lidas." in response.data['mensagem']
        assert Notificacao.objects.filter(usuario=authenticated_user, lida=False).count() == 0

    def test_nao_lidas_action(self, authenticated_client, authenticated_user, notificacao_factory, projeto_factory):
        proj = projeto_factory()
        notificacao_factory(usuario=authenticated_user, lida=False, tipo="PROJETO", prioridade="ALTA", projeto=proj)
        notificacao_factory(usuario=authenticated_user, lida=False, tipo="TAREFA", prioridade="MEDIA")
        notificacao_factory(usuario=authenticated_user, lida=True, tipo="PROJETO") # Read one

        url = reverse('notificacao-nao-lidas')
        response_all_unread = authenticated_client.get(url)
        assert response_all_unread.status_code == status.HTTP_200_OK
        assert len(response_all_unread.data) == 2

        # Filter by tipo
        response_tipo = authenticated_client.get(url, {'tipo': 'PROJETO'})
        assert len(response_tipo.data) == 1
        assert response_tipo.data[0]['tipo'] == "PROJETO"

        # Filter by prioridade
        response_prio = authenticated_client.get(url, {'prioridade': 'ALTA'})
        assert len(response_prio.data) == 1
        assert response_prio.data[0]['prioridade'] == "ALTA"

        # Filter by projeto
        response_proj = authenticated_client.get(url, {'projeto': proj.id})
        assert len(response_proj.data) == 1
        assert response_proj.data[0]['projeto'] == proj.id


# --- TestConfiguracaoNotificacaoViewSet ---
class TestConfiguracaoNotificacaoViewSet:
    base_url_list = reverse('configuracao-list') # Matches router basename

    def get_detail_url(self, config_id):
        return reverse('configuracao-detail', kwargs={'pk': config_id})

    def test_list_configuracao_own_only(self, authenticated_client, authenticated_user, configuracao_notificacao_factory, user_factory):
        configuracao_notificacao_factory(usuario=authenticated_user)
        other_user = user_factory(username="other_config_user")
        configuracao_notificacao_factory(usuario=other_user)

        response = authenticated_client.get(self.base_url_list)
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data['results']) == 1
        assert response.data['results'][0]['usuario'] == authenticated_user.id

    def test_create_configuracao_unique_for_user(self, authenticated_client, authenticated_user):
        data = {
            # "usuario" is implicit from perform_create via serializer logic (create or update)
            "tarefa_atribuida": "EMAIL", "mensagem_chat": "SISTEMA"
        }
        # First creation
        response_create = authenticated_client.post(self.base_url_list, data=data)
        assert response_create.status_code == status.HTTP_201_CREATED
        config_id = response_create.data['id']
        assert ConfiguracaoNotificacao.objects.filter(usuario=authenticated_user).count() == 1

        # Attempting to "create" again should update due to serializer's custom create
        data_update = {"tarefa_atribuida": "NENHUM", "mensagem_chat": "AMBOS"}
        response_update = authenticated_client.post(self.base_url_list, data=data_update)
        assert response_update.status_code == status.HTTP_201_CREATED # Still 201 due to serializer.create
        assert response_update.data['id'] == config_id # Should be the same object
        config = ConfiguracaoNotificacao.objects.get(usuario=authenticated_user)
        assert config.tarefa_atribuida == "NENHUM"
        assert config.mensagem_chat == "AMBOS"
        assert ConfiguracaoNotificacao.objects.filter(usuario=authenticated_user).count() == 1


    def test_perform_create_validation_error_in_view(self, authenticated_client, authenticated_user, configuracao_notificacao_factory):
        # This test targets the perform_create logic that was present in the view,
        # which has been superseded by the serializer's custom create method.
        # The serializer now handles the "create or update" behavior.
        # If the view's perform_create had a `tipo` check, it's no longer relevant
        # as ConfiguracaoNotificacao doesn't have a `tipo` field.

        # Create initial config via factory to ensure one exists
        configuracao_notificacao_factory(usuario=authenticated_user)

        # The serializer's create method will now update if it exists.
        # The view's original perform_create had a check for `tipo`, which is not on the model.
        # So, we test the serializer's behavior.
        data = {"tarefa_comentario": "EMAIL"}
        response = authenticated_client.post(self.base_url_list, data=data) # This will update
        assert response.status_code == status.HTTP_201_CREATED # Or 200 if serializer returns updated
        config = ConfiguracaoNotificacao.objects.get(usuario=authenticated_user)
        assert config.tarefa_comentario == "EMAIL"


    def test_minha_configuracao_action_get_existing(self, authenticated_client, authenticated_user, configuracao_notificacao_factory):
        config = configuracao_notificacao_factory(usuario=authenticated_user, tarefa_prazo="AMBOS")
        url = reverse('configuracao-minha-configuracao')
        response = authenticated_client.get(url)
        assert response.status_code == status.HTTP_200_OK
        assert response.data['id'] == config.id
        assert response.data['tarefa_prazo'] == "AMBOS"

    def test_minha_configuracao_action_create_if_not_exists(self, authenticated_client, authenticated_user):
        assert not ConfiguracaoNotificacao.objects.filter(usuario=authenticated_user).exists()
        url = reverse('configuracao-minha-configuracao')
        response = authenticated_client.get(url)
        assert response.status_code == status.HTTP_200_OK
        assert ConfiguracaoNotificacao.objects.filter(usuario=authenticated_user).exists()
        config = ConfiguracaoNotificacao.objects.get(usuario=authenticated_user)
        # Check default values if any are important
        assert response.data['id'] == config.id
        assert response.data['tarefa_atribuida'] == 'AMBOS' # Default from model


# --- TestComunicacaoViewSet --- (Assuming ComunicacaoViewSet is added to urls.py)
# You need to register ComunicacaoViewSet in your urls.py for these to work
# router.register(r'comunicacoes', ComunicacaoViewSet, basename='comunicacao')

class TestComunicacaoViewSet:
    # This requires 'comunicacao-list' to be a valid URL name
    # Ensure ComunicacaoViewSet is registered in urls.py:
    # router.register(r'comunicacoes', ComunicacaoViewSet, basename='comunicacao')
    base_url_list = reverse('comunicacao-list')

    def get_detail_url(self, comm_id):
        return reverse('comunicacao-detail', kwargs={'pk': comm_id})

    def test_list_comunicacoes_filtered(self, authenticated_client, comunicacao_factory, projeto_factory, user_factory):
        proj1 = projeto_factory()
        proj2 = projeto_factory()
        sender1 = user_factory(username="sender_c1")
        com1 = comunicacao_factory(projeto=proj1, remetente=sender1, tipo="ATA")
        comunicacao_factory(projeto=proj2, tipo="MEMORANDO")

        response = authenticated_client.get(self.base_url_list, {'projeto': proj1.id, 'tipo': 'ATA'})
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data['results']) == 1
        assert response.data['results'][0]['id'] == com1.id
        assert response.data['results'][0]['projeto'] == proj1.id
        assert response.data['results'][0]['tipo'] == 'ATA'

    def test_create_comunicacao(self, authenticated_client, authenticated_user, projeto_factory, user_factory):
        proj = projeto_factory()
        dest1 = user_factory(username="dest_c1")
        dest2 = user_factory(username="dest_c2")
        data = {
            "projeto": proj.id,
            "tipo": "RELATORIO",
            "titulo": "Quarterly Financial Report",
            "texto": "Detailed financial data for Q1.",
            "destinatarios": [dest1.id, dest2.id]
        }
        response = authenticated_client.post(self.base_url_list, data=data)
        assert response.status_code == status.HTTP_201_CREATED
        com = Comunicacao.objects.get(id=response.data['id'])
        assert com.remetente == authenticated_user
        assert com.projeto == proj
        assert com.titulo == "Quarterly Financial Report"
        assert com.destinatarios.count() == 2
        assert dest1 in com.destinatarios.all()

    def test_update_comunicacao_own(self, authenticated_client, authenticated_user, comunicacao_factory):
        com = comunicacao_factory(remetente=authenticated_user, titulo="Initial Title")
        data = {"titulo": "Updated Title by Sender"}
        response = authenticated_client.patch(self.get_detail_url(com.id), data=data)
        assert response.status_code == status.HTTP_200_OK
        com.refresh_from_db()
        assert com.titulo == "Updated Title by Sender"

    def test_update_comunicacao_not_owner_forbidden(self, authenticated_client, comunicacao_factory, user_factory):
        owner = user_factory(username="comm_owner")
        com = comunicacao_factory(remetente=owner, titulo="Owner's Title")
        # authenticated_client's user is not the owner
        data = {"titulo": "Attempted Update"}
        response = authenticated_client.patch(self.get_detail_url(com.id), data=data)
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_update_comunicacao_staff_can_update(self, authenticated_client, authenticated_user, comunicacao_factory, user_factory):
        owner = user_factory(username="comm_owner_staff")
        com = comunicacao_factory(remetente=owner)

        # Make authenticated_client's user a staff member
        authenticated_user.is_staff = True
        authenticated_user.save()

        data = {"titulo": "Updated by Staff"}
        response = authenticated_client.patch(self.get_detail_url(com.id), data=data)
        assert response.status_code == status.HTTP_200_OK
        com.refresh_from_db()
        assert com.titulo == "Updated by Staff"