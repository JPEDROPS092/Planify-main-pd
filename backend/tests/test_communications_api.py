from rest_framework.test import APITestCase, APIClient
from django.urls import reverse
from rest_framework import status
from django.contrib.auth import get_user_model
from django.utils import timezone
from projects.models import Project
from tasks.models import Task
from communications.models import (
    ChatMensagem, ChatMensagemLeitura, Notificacao, 
    ConfiguracaoNotificacao, Comunicacao
)
from users.models import User
from datetime import date, timedelta

User = get_user_model()

class CommunicationAPITests(APITestCase):
    """
    Testes para a API do módulo de comunicações.
    
    Testa as funcionalidades de mensagens de chat, notificações,
    configurações de notificações e comunicações formais.
    """
    def setUp(self):
        # Cria usuários para teste
        self.admin = User.objects.create_superuser(
            username='admin',
            email='admin@example.com',
            password='password123'
        )
        self.user = User.objects.create_user(
            username='user',
            email='user@example.com',
            password='password123'
        )
        
        # Configura cliente API
        self.client = APIClient()
        self.client.force_authenticate(user=self.admin)
        
        # Cria projeto para teste
        self.project = Project.objects.create(
            name='Test Project',
            description='Test project description',
            owner=self.admin
        )
        
        # Cria tarefa para teste
        self.task = Task.objects.create(
            title='Test Task',
            description='Test task description',
            project=self.project,
            assigned_to=self.admin,
            created_by=self.admin,
            status='TODO'
        )

    # Testes para ChatMensagem
    
    def test_send_message(self):
        """
        Testa o envio de uma mensagem de chat.
        """
        url = reverse('chatmensagem-list')
        data = {'projeto': self.project.id, 'texto': 'Mensagem de teste'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(ChatMensagem.objects.filter(texto='Mensagem de teste').exists())
    
    def test_list_messages(self):
        """
        Testa a listagem de mensagens de chat.
        """
        # Cria uma mensagem para testar a listagem
        ChatMensagem.objects.create(
            projeto=self.project,
            autor=self.admin,
            texto='Mensagem para listar'
        )
        
        url = reverse('chatmensagem-list')
        response = self.client.get(url, {'projeto': self.project.id}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(response.data), 1)
        
    def test_mark_message_as_read(self):
        """
        Testa marcar uma mensagem como lida.
        """
        # Cria uma mensagem para testar
        mensagem = ChatMensagem.objects.create(
            projeto=self.project,
            autor=self.user,  # Outro usuário é o autor
            texto='Mensagem para marcar como lida'
        )
        
        # Autentica como admin para marcar como lida
        self.client.force_authenticate(user=self.admin)
        
        url = reverse('chatmensagem-marcar-como-lida', args=[mensagem.id])
        response = self.client.post(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        
        # Verifica se a mensagem foi marcada como lida
        self.assertTrue(ChatMensagemLeitura.objects.filter(
            mensagem=mensagem, 
            usuario=self.admin
        ).exists())
    
    def test_list_unread_messages(self):
        """
        Testa a listagem de mensagens não lidas.
        """
        # Cria mensagens de teste
        mensagem1 = ChatMensagem.objects.create(
            projeto=self.project,
            autor=self.user,
            texto='Mensagem não lida 1'
        )
        mensagem2 = ChatMensagem.objects.create(
            projeto=self.project,
            autor=self.user,
            texto='Mensagem não lida 2'
        )
        mensagem3 = ChatMensagem.objects.create(
            projeto=self.project,
            autor=self.admin,  # Mensagem enviada pelo próprio usuário
            texto='Mensagem própria'
        )
        
        # Marca uma mensagem como lida
        ChatMensagemLeitura.objects.create(
            mensagem=mensagem1,
            usuario=self.admin
        )
        
        # Autentica como admin
        self.client.force_authenticate(user=self.admin)
        
        url = reverse('chatmensagem-mensagens-nao-lidas')
        response = self.client.get(url, {'projeto': self.project.id}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Deve retornar apenas a mensagem2 (não lida e não enviada pelo usuário)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['texto'], 'Mensagem não lida 2')
        
    # Testes para Notificação
    
    def test_create_notification(self):
        """
        Testa a criação de uma notificação.
        """
        url = reverse('notificacao-list')
        data = {
            'usuario': self.admin.id,
            'tipo': 'SISTEMA',
            'titulo': 'Notificação de teste',
            'conteudo': 'Conteúdo da notificação de teste',
            'projeto': self.project.id,
            'prioridade': 'MEDIA'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(Notificacao.objects.filter(titulo='Notificação de teste').exists())
    
    def test_list_notifications(self):
        """
        Testa a listagem de notificações.
        """
        # Cria notificações para teste
        Notificacao.objects.create(
            usuario=self.admin,
            tipo='SISTEMA',
            titulo='Notificação 1',
            conteudo='Conteúdo da notificação 1',
            projeto=self.project,
            prioridade='ALTA'
        )
        Notificacao.objects.create(
            usuario=self.admin,
            tipo='TAREFA',
            titulo='Notificação 2',
            conteudo='Conteúdo da notificação 2',
            projeto=self.project,
            tarefa=self.task,
            prioridade='BAIXA'
        )
        
        url = reverse('notificacao-list')
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)
    
    def test_mark_notification_as_read(self):
        """
        Testa marcar uma notificação como lida.
        """
        # Cria uma notificação para teste
        notificacao = Notificacao.objects.create(
            usuario=self.admin,
            tipo='SISTEMA',
            titulo='Notificação para marcar como lida',
            conteudo='Conteúdo da notificação',
            projeto=self.project,
            prioridade='MEDIA'
        )
        
        url = reverse('notificacao-marcar-como-lida', args=[notificacao.id])
        response = self.client.post(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Verifica se a notificação foi marcada como lida
        notificacao.refresh_from_db()
        self.assertTrue(notificacao.lida)
        self.assertIsNotNone(notificacao.lida_em)
    
    def test_mark_all_notifications_as_read(self):
        """
        Testa marcar todas as notificações como lidas.
        """
        # Cria notificações para teste
        Notificacao.objects.create(
            usuario=self.admin,
            tipo='SISTEMA',
            titulo='Notificação 1',
            conteudo='Conteúdo da notificação 1',
            projeto=self.project,
            prioridade='ALTA'
        )
        Notificacao.objects.create(
            usuario=self.admin,
            tipo='TAREFA',
            titulo='Notificação 2',
            conteudo='Conteúdo da notificação 2',
            projeto=self.project,
            tarefa=self.task,
            prioridade='BAIXA'
        )
        
        url = reverse('notificacao-marcar-todas-como-lidas')
        response = self.client.post(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Verifica se todas as notificações foram marcadas como lidas
        self.assertEqual(Notificacao.objects.filter(lida=True).count(), 2)
    
    def test_list_unread_notifications(self):
        """
        Testa a listagem de notificações não lidas.
        """
        # Cria notificações para teste
        Notificacao.objects.create(
            usuario=self.admin,
            tipo='SISTEMA',
            titulo='Notificação não lida',
            conteudo='Conteúdo da notificação não lida',
            projeto=self.project,
            prioridade='ALTA'
        )
        notificacao_lida = Notificacao.objects.create(
            usuario=self.admin,
            tipo='TAREFA',
            titulo='Notificação lida',
            conteudo='Conteúdo da notificação lida',
            projeto=self.project,
            tarefa=self.task,
            prioridade='BAIXA'
        )
        
        # Marca uma notificação como lida
        notificacao_lida.lida = True
        notificacao_lida.lida_em = timezone.now()
        notificacao_lida.save()
        
        url = reverse('notificacao-nao-lidas')
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['titulo'], 'Notificação não lida')
    
    # Testes para ConfiguracaoNotificacao
    
    def test_create_notification_config(self):
        """
        Testa a criação de uma configuração de notificação.
        """
        url = reverse('configuracaonotificacao-list')
        data = {
            'tipo': 'SISTEMA',
            'email': True,
            'push': False,
            'in_app': True
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(ConfiguracaoNotificacao.objects.filter(tipo='SISTEMA', usuario=self.admin).exists())
    
    def test_get_my_notification_config(self):
        """
        Testa a obtenção da configuração de notificação do usuário.
        """
        # Cria uma configuração para teste
        ConfiguracaoNotificacao.objects.create(
            usuario=self.admin,
            tipo='SISTEMA',
            email=True,
            push=False,
            in_app=True
        )
        
        url = reverse('configuracaonotificacao-minha-configuracao')
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
