from rest_framework.test import APITestCase, APIClient
from django.urls import reverse
from users.models import User
from projects.models import Projeto, Sprint
from tasks.models import Tarefa, AtribuicaoTarefa, ComentarioTarefa
from datetime import date, timedelta

class TaskAPITests(APITestCase):
    def setUp(self):
        self.admin = User.objects.create_superuser(
            email='admin@planify.com',
            username='admin',
            full_name='Administrador',
            password='admin123',
        )
        self.user = User.objects.create_user(
            email='user@planify.com',
            username='user',
            full_name='Usuário Regular',
            password='user123',
            role='TEAM_MEMBER'
        )
        self.client = APIClient()
        self.client.force_authenticate(user=self.admin)
        
        self.project = Projeto.objects.create(
            titulo='Projeto Tarefa',
            descricao='Projeto para teste de tarefas',
            data_inicio=date.today(),
            data_fim=date.today() + timedelta(days=30),
            status='PLANEJADO',
            prioridade='MEDIA',
            criado_por=self.admin
        )
        
        self.sprint = Sprint.objects.create(
            projeto=self.project,
            nome='Sprint 1',
            descricao='Sprint de teste',
            data_inicio=date.today(),
            data_fim=date.today() + timedelta(days=14),
            criado_por=self.admin
        )

    def test_create_task(self):
        """Teste de criação de tarefa"""
        url = reverse('tarefa-list')
        data = {
            'titulo': 'Tarefa Teste',
            'descricao': 'Descrição de teste',
            'data_inicio': date.today().isoformat(),
            'data_termino': (date.today() + timedelta(days=5)).isoformat(),
            'prioridade': 'MEDIA',
            'status': 'A_FAZER',
            'projeto': self.project.id
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, 201)
        self.assertTrue(Tarefa.objects.filter(titulo='Tarefa Teste').exists())

    def test_list_tasks(self):
        """Teste de listagem de tarefas"""
        # Criar uma tarefa para teste
        Tarefa.objects.create(
            titulo='Tarefa Lista',
            descricao='Tarefa para teste de listagem',
            data_inicio=date.today(),
            data_termino=date.today() + timedelta(days=5),
            projeto=self.project,
            criado_por=self.admin
        )
        
        url = reverse('tarefa-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertGreaterEqual(len(response.data['results']), 1)

    def test_get_task_detail(self):
        """Teste de detalhes da tarefa"""
        tarefa = Tarefa.objects.create(
            titulo='Tarefa Detalhes',
            descricao='Tarefa para teste de detalhes',
            data_inicio=date.today(),
            data_termino=date.today() + timedelta(days=5),
            projeto=self.project,
            criado_por=self.admin
        )
        
        url = reverse('tarefa-detail', kwargs={'pk': tarefa.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['titulo'], 'Tarefa Detalhes')

    def test_update_task(self):
        """Teste de atualização de tarefa"""
        tarefa = Tarefa.objects.create(
            titulo='Tarefa Atualizar',
            descricao='Tarefa para atualizar',
            data_inicio=date.today(),
            data_termino=date.today() + timedelta(days=5),
            projeto=self.project,
            criado_por=self.admin
        )
        
        url = reverse('tarefa-detail', kwargs={'pk': tarefa.pk})
        data = {
            'titulo': 'Tarefa Atualizada',
            'status': 'EM_ANDAMENTO'
        }
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, 200)
        tarefa.refresh_from_db()
        self.assertEqual(tarefa.titulo, 'Tarefa Atualizada')
        self.assertEqual(tarefa.status, 'EM_ANDAMENTO')

    def test_delete_task(self):
        """Teste de exclusão de tarefa"""
        tarefa = Tarefa.objects.create(
            titulo='Tarefa Deletar',
            descricao='Tarefa para deletar',
            data_inicio=date.today(),
            data_termino=date.today() + timedelta(days=5),
            projeto=self.project,
            criado_por=self.admin
        )
        
        url = reverse('tarefa-detail', kwargs={'pk': tarefa.pk})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, 204)
        self.assertFalse(Tarefa.objects.filter(pk=tarefa.pk).exists())

    def test_assign_task(self):
        """Teste de atribuição de tarefa"""
        tarefa = Tarefa.objects.create(
            titulo='Tarefa Atribuir',
            descricao='Tarefa para atribuir',
            data_inicio=date.today(),
            data_termino=date.today() + timedelta(days=5),
            projeto=self.project,
            criado_por=self.admin
        )
        
        url = reverse('tarefa-atribuir', kwargs={'pk': tarefa.pk})
        data = {'usuario': self.user.pk}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, 201)
        self.assertTrue(AtribuicaoTarefa.objects.filter(
            tarefa=tarefa,
            usuario=self.user
        ).exists())

    def test_add_task_comment(self):
        """Teste de adição de comentário à tarefa"""
        tarefa = Tarefa.objects.create(
            titulo='Tarefa Comentário',
            descricao='Tarefa para teste de comentário',
            data_inicio=date.today(),
            data_termino=date.today() + timedelta(days=5),
            projeto=self.project,
            criado_por=self.admin
        )
        
        url = reverse('tarefa-comentar', kwargs={'pk': tarefa.pk})
        data = {'texto': 'Este é um comentário de teste'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, 201)
        self.assertTrue(ComentarioTarefa.objects.filter(
            tarefa=tarefa,
            texto='Este é um comentário de teste'
        ).exists())

    def test_task_with_sprint(self):
        """Teste de tarefa associada a sprint"""
        url = reverse('tarefa-list')
        data = {
            'titulo': 'Tarefa Sprint',
            'descricao': 'Tarefa associada a sprint',
            'data_inicio': date.today().isoformat(),
            'data_termino': (date.today() + timedelta(days=5)).isoformat(),
            'prioridade': 'ALTA',
            'status': 'A_FAZER',
            'projeto': self.project.id,
            'sprint': self.sprint.id
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, 201)
        tarefa = Tarefa.objects.get(titulo='Tarefa Sprint')
        self.assertEqual(tarefa.sprint, self.sprint)

    def test_filter_tasks_by_project(self):
        """Teste de filtro de tarefas por projeto"""
        Tarefa.objects.create(
            titulo='Tarefa Projeto 1',
            descricao='Tarefa do projeto 1',
            data_inicio=date.today(),
            data_termino=date.today() + timedelta(days=5),
            projeto=self.project,
            criado_por=self.admin
        )
        
        url = reverse('tarefa-list')
        response = self.client.get(url, {'projeto': self.project.id})
        self.assertEqual(response.status_code, 200)
        self.assertGreaterEqual(len(response.data['results']), 1)

    def test_filter_tasks_by_status(self):
        """Teste de filtro de tarefas por status"""
        Tarefa.objects.create(
            titulo='Tarefa Em Andamento',
            descricao='Tarefa em andamento',
            data_inicio=date.today(),
            data_termino=date.today() + timedelta(days=5),
            projeto=self.project,
            status='EM_ANDAMENTO',
            criado_por=self.admin
        )
        
        url = reverse('tarefa-list')
        response = self.client.get(url, {'status': 'EM_ANDAMENTO'})
        self.assertEqual(response.status_code, 200)

    def test_filter_tasks_by_assigned_user(self):
        """Teste de filtro de tarefas por usuário atribuído"""
        tarefa = Tarefa.objects.create(
            titulo='Tarefa Atribuída',
            descricao='Tarefa atribuída ao usuário',
            data_inicio=date.today(),
            data_termino=date.today() + timedelta(days=5),
            projeto=self.project,
            criado_por=self.admin
        )
        
        AtribuicaoTarefa.objects.create(
            tarefa=tarefa,
            usuario=self.user,
            atribuido_por=self.admin
        )
        
        url = reverse('tarefa-list')
        response = self.client.get(url, {'atribuido_para': self.user.id})
        self.assertEqual(response.status_code, 200)

    def test_task_permissions(self):
        """Teste de permissões de tarefa"""
        # Teste sem autenticação
        self.client.logout()
        url = reverse('tarefa-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 401)

    def test_task_validation(self):
        """Teste de validação de dados da tarefa"""
        url = reverse('tarefa-list')
        data = {
            'titulo': '',  # Título vazio (inválido)
            'descricao': 'Descrição',
            'data_inicio': date.today().isoformat(),
            'data_termino': (date.today() - timedelta(days=1)).isoformat(),  # Data fim antes do início
            'prioridade': 'MEDIA',
            'status': 'A_FAZER',
            'projeto': self.project.id
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, 400)
