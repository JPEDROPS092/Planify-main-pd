from rest_framework.test import APITestCase, APIClient
from django.urls import reverse
from users.models import User
from projects.models import Projeto, MembroProjeto, Sprint
from datetime import date, timedelta

class ProjectAPITests(APITestCase):
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

    def test_create_project(self):
        """Teste de criação de projeto"""
        url = reverse('projects-list')
        data = {
            'titulo': 'Projeto Teste',
            'descricao': 'Descrição do projeto teste',
            'data_inicio': date.today().isoformat(),
            'data_fim': (date.today() + timedelta(days=30)).isoformat(),
            'status': 'PLANEJADO',
            'prioridade': 'ALTA'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, 201)
        self.assertTrue(Projeto.objects.filter(titulo='Projeto Teste').exists())

    def test_list_projects(self):
        """Teste de listagem de projetos"""
        # Criar um projeto para teste
        Projeto.objects.create(
            titulo='Projeto Lista',
            descricao='Projeto para teste de listagem',
            data_inicio=date.today(),
            data_fim=date.today() + timedelta(days=30),
            criado_por=self.admin
        )
        
        url = reverse('projects-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertGreaterEqual(len(response.data['results']), 1)

    def test_get_project_detail(self):
        """Teste de detalhes do projeto"""
        projeto = Projeto.objects.create(
            titulo='Projeto Detalhes',
            descricao='Projeto para teste de detalhes',
            data_inicio=date.today(),
            data_fim=date.today() + timedelta(days=30),
            criado_por=self.admin
        )
        
        url = reverse('projects-detail', kwargs={'pk': projeto.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['titulo'], 'Projeto Detalhes')

    def test_update_project(self):
        """Teste de atualização de projeto"""
        projeto = Projeto.objects.create(
            titulo='Projeto Atualizar',
            descricao='Projeto para atualizar',
            data_inicio=date.today(),
            data_fim=date.today() + timedelta(days=30),
            criado_por=self.admin
        )
        
        url = reverse('projects-detail', kwargs={'pk': projeto.pk})
        data = {
            'titulo': 'Projeto Atualizado',
            'status': 'EM_ANDAMENTO'
        }
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, 200)
        projeto.refresh_from_db()
        self.assertEqual(projeto.titulo, 'Projeto Atualizado')
        self.assertEqual(projeto.status, 'EM_ANDAMENTO')

    def test_delete_project(self):
        """Teste de exclusão de projeto"""
        projeto = Projeto.objects.create(
            titulo='Projeto Deletar',
            descricao='Projeto para deletar',
            data_inicio=date.today(),
            data_fim=date.today() + timedelta(days=30),
            criado_por=self.admin
        )
        
        url = reverse('projects-detail', kwargs={'pk': projeto.pk})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, 204)
        self.assertFalse(Projeto.objects.filter(pk=projeto.pk).exists())

    def test_add_project_member(self):
        """Teste de adição de membro ao projeto"""
        projeto = Projeto.objects.create(
            titulo='Projeto Membro',
            descricao='Projeto para teste de membros',
            data_inicio=date.today(),
            data_fim=date.today() + timedelta(days=30),
            criado_por=self.admin
        )
        
        url = reverse('projects-adicionar-membro', kwargs={'pk': projeto.pk})
        data = {
            'usuario': self.user.pk,
            'papel': 'DESENVOLVEDOR'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, 201)
        self.assertTrue(MembroProjeto.objects.filter(
            projeto=projeto,
            usuario=self.user,
            papel='DESENVOLVEDOR'
        ).exists())

    def test_remove_project_member(self):
        """Teste de remoção de membro do projeto"""
        projeto = Projeto.objects.create(
            titulo='Projeto Remover Membro',
            descricao='Projeto para teste de remoção de membros',
            data_inicio=date.today(),
            data_fim=date.today() + timedelta(days=30),
            criado_por=self.admin
        )
        
        # Adicionar membro primeiro
        membro = MembroProjeto.objects.create(
            projeto=projeto,
            usuario=self.user,
            papel='DESENVOLVEDOR'
        )
        
        url = reverse('projects-remover-membro', kwargs={'pk': projeto.pk})
        data = {'usuario': self.user.pk}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, 200)
        self.assertFalse(MembroProjeto.objects.filter(pk=membro.pk).exists())

    def test_create_sprint(self):
        """Teste de criação de sprint"""
        projeto = Projeto.objects.create(
            titulo='Projeto Sprint',
            descricao='Projeto para teste de sprint',
            data_inicio=date.today(),
            data_fim=date.today() + timedelta(days=30),
            criado_por=self.admin
        )
        
        url = reverse('projects-criar-sprint', kwargs={'pk': projeto.pk})
        data = {
            'nome': 'Sprint 1',
            'descricao': 'Primeira sprint do projeto',
            'data_inicio': date.today().isoformat(),
            'data_fim': (date.today() + timedelta(days=14)).isoformat()
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, 201)
        self.assertTrue(Sprint.objects.filter(
            projeto=projeto,
            nome='Sprint 1'
        ).exists())

    def test_project_dashboard(self):
        """Teste do dashboard do projeto"""
        projeto = Projeto.objects.create(
            titulo='Projeto Dashboard',
            descricao='Projeto para teste de dashboard',
            data_inicio=date.today(),
            data_fim=date.today() + timedelta(days=30),
            criado_por=self.admin
        )
        
        url = reverse('projects-dashboard', kwargs={'projeto_id': projeto.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_project_kanban(self):
        """Teste da visualização Kanban"""
        projeto = Projeto.objects.create(
            titulo='Projeto Kanban',
            descricao='Projeto para teste de kanban',
            data_inicio=date.today(),
            data_fim=date.today() + timedelta(days=30),
            criado_por=self.admin
        )
        
        url = reverse('projects-kanban', kwargs={'projeto_id': projeto.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_project_gantt(self):
        """Teste da visualização Gantt"""
        projeto = Projeto.objects.create(
            titulo='Projeto Gantt',
            descricao='Projeto para teste de gantt',
            data_inicio=date.today(),
            data_fim=date.today() + timedelta(days=30),
            criado_por=self.admin
        )
        
        url = reverse('projects-gantt', kwargs={'projeto_id': projeto.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_project_export(self):
        """Teste de exportação do projeto"""
        projeto = Projeto.objects.create(
            titulo='Projeto Export',
            descricao='Projeto para teste de exportação',
            data_inicio=date.today(),
            data_fim=date.today() + timedelta(days=30),
            criado_por=self.admin
        )
        
        url = reverse('projects-exportar', kwargs={'projeto_id': projeto.pk})
        response = self.client.get(url, {'formato': 'csv'})
        self.assertEqual(response.status_code, 200)

    def test_project_permissions(self):
        """Teste de permissões de projeto"""
        # Teste sem autenticação
        self.client.logout()
        url = reverse('projects-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 401)

    def test_project_validation(self):
        """Teste de validação de dados do projeto"""
        url = reverse('projects-list')
        data = {
            'titulo': '',  # Título vazio (inválido)
            'descricao': 'Descrição',
            'data_inicio': date.today().isoformat(),
            'data_fim': (date.today() - timedelta(days=1)).isoformat(),  # Data fim antes do início
            'status': 'PLANEJADO',
            'prioridade': 'ALTA'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, 400)
