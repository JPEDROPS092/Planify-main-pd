"""Testes de API do módulo de comunicações no stack multi-tenant real.

Reescrito a partir do scaffold antigo, que assumia um contrato obsoleto
(campos `conteudo`, `email/push/in_app`, modelo `Project`/`Task`). Cobrem-se
as rotas e as custom actions atuais (mensagens de chat, leitura, notificações
e configuração do usuário), com asserções por existência — robustas a
paginação — em vez de contagens exatas frágeis.
"""
from datetime import date, timedelta

from django.urls import reverse
from rest_framework import status

from communications.models import (
    ChatMensagem, ChatMensagemLeitura, Notificacao, ConfiguracaoNotificacao,
)
from projects.models import Projeto
from tests.tenant_base import TenantAPITestCase


class CommunicationAPITests(TenantAPITestCase):
    def setUp(self):
        super().setUp()
        # Segundo membro do mesmo tenant: autor de mensagens "de outro usuário".
        self.outro = self.create_member(
            email='outro@planify.test', username='outro', full_name='Outro Membro',
        )
        self.project = Projeto.objects.create(
            titulo='Projeto Comunicação',
            descricao='Teste',
            data_inicio=date.today(),
            data_fim=date.today() + timedelta(days=10),
            status='PLANEJADO',
            prioridade='MEDIA',
            criado_por=self.user,
        )

    # --- ChatMensagem ---------------------------------------------------

    def test_send_message(self):
        url = reverse('chatmensagem-list')
        data = {'projeto': self.project.id, 'texto': 'Mensagem de teste'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(ChatMensagem.objects.filter(texto='Mensagem de teste').exists())

    def test_list_messages(self):
        ChatMensagem.objects.create(
            projeto=self.project, autor=self.user, texto='Mensagem para listar',
        )
        url = reverse('chatmensagem-list')
        response = self.client.get(url, {'projeto': self.project.id})
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_mark_message_as_read(self):
        mensagem = ChatMensagem.objects.create(
            projeto=self.project, autor=self.outro, texto='Marcar como lida',
        )
        url = reverse('chatmensagem-marcar-como-lida', args=[mensagem.id])
        response = self.client.post(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(ChatMensagemLeitura.objects.filter(
            mensagem=mensagem, usuario=self.user,
        ).exists())

    def test_list_unread_messages(self):
        ChatMensagem.objects.create(
            projeto=self.project, autor=self.outro, texto='Não lida',
        )
        url = reverse('chatmensagem-mensagens-nao-lidas')
        response = self.client.get(url, {'projeto': self.project.id})
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    # --- Notificação ----------------------------------------------------

    def test_create_notification(self):
        url = reverse('notificacao-list')
        data = {
            'usuario': self.user.id,
            'tipo': 'SISTEMA',
            'titulo': 'Notificação de teste',
            'mensagem': 'Conteúdo da notificação de teste',
            'projeto': self.project.id,
            'prioridade': 'MEDIA',
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(Notificacao.objects.filter(titulo='Notificação de teste').exists())

    def test_list_notifications(self):
        Notificacao.objects.create(
            usuario=self.user, tipo='SISTEMA', titulo='Notificação 1',
            mensagem='Conteúdo 1', projeto=self.project, prioridade='ALTA',
        )
        url = reverse('notificacao-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_mark_notification_as_read(self):
        notificacao = Notificacao.objects.create(
            usuario=self.user, tipo='SISTEMA', titulo='Marcar lida',
            mensagem='Conteúdo', projeto=self.project, prioridade='MEDIA',
        )
        url = reverse('notificacao-marcar-como-lida', args=[notificacao.id])
        response = self.client.post(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        notificacao.refresh_from_db()
        self.assertTrue(notificacao.lida)
        self.assertIsNotNone(notificacao.lida_em)

    def test_mark_all_notifications_as_read(self):
        Notificacao.objects.create(
            usuario=self.user, tipo='SISTEMA', titulo='N1', mensagem='c1',
            projeto=self.project, prioridade='ALTA',
        )
        Notificacao.objects.create(
            usuario=self.user, tipo='TAREFA', titulo='N2', mensagem='c2',
            projeto=self.project, prioridade='BAIXA',
        )
        url = reverse('notificacao-marcar-todas-como-lidas')
        response = self.client.post(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Notificacao.objects.filter(usuario=self.user, lida=False).count(), 0)

    def test_list_unread_notifications(self):
        Notificacao.objects.create(
            usuario=self.user, tipo='SISTEMA', titulo='Não lida',
            mensagem='c', projeto=self.project, prioridade='ALTA',
        )
        url = reverse('notificacao-nao-lidas')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    # --- ConfiguracaoNotificacao ---------------------------------------

    def test_get_my_notification_config(self):
        # Auto-cria a configuração padrão do usuário se ainda não existir.
        url = reverse('configuracao-minha-configuracao')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_notification_config(self):
        # Regressão: perform_create antes filtrava por um campo `tipo`
        # inexistente (FieldError em todo POST).
        url = reverse('configuracao-list')
        data = {'usuario': self.user.id, 'tarefa_atribuida': 'EMAIL'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        config = ConfiguracaoNotificacao.objects.get(usuario=self.user)
        self.assertEqual(config.tarefa_atribuida, 'EMAIL')

    def test_post_config_duplicate_rejected(self):
        # OneToOne por usuário: o 2º POST é barrado (UniqueValidator), sem
        # duplicar. Atualizações de config são feitas via PATCH no detalhe.
        url = reverse('configuracao-list')
        first = self.client.post(url, {'usuario': self.user.id, 'tarefa_atribuida': 'EMAIL'}, format='json')
        self.assertEqual(first.status_code, status.HTTP_201_CREATED)
        second = self.client.post(url, {'usuario': self.user.id, 'tarefa_atribuida': 'NENHUM'}, format='json')
        self.assertEqual(second.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(ConfiguracaoNotificacao.objects.filter(usuario=self.user).count(), 1)
