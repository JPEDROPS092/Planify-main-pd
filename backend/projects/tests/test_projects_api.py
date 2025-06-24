from rest_framework.test import APITestCase, APIClient
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.utils import timezone
from users.models import User, UserManager
from projects.models import Projeto, MembroProjeto, Sprint
from datetime import date, timedelta, datetime
from typing import cast
import json

User = get_user_model()

class ProjectAPITests(APITestCase):
    def setUp(self):
        # Create admin user
        user_manager = cast(UserManager, User.objects)
        self.admin = user_manager.create_superuser(
            email='admin@planify.com',
            username='admin',
            full_name='Administrador',
            password='admin123',
        )
        
        # Create regular user
        self.user = user_manager.create_user(
            email='user@planify.com',
            username='user',
            full_name='Usuário Regular',
            password='user123',
        )
        
        # Create test project
        self.project = Projeto.objects.create(
            titulo='Projeto Existente',
            descricao='Descrição do projeto existente',
            data_inicio=date.today(),
            data_fim=date.today() + timedelta(days=30),
            status='PLANEJADO',
            prioridade='MEDIA',
            criado_por=self.admin
        )
        
        # Add member to project
        self.member = MembroProjeto.objects.create(
            projeto=self.project,
            usuario=self.user,
            papel='DESENVOLVEDOR'
        )
        
        # Create sprint for the project
        self.sprint = Sprint.objects.create(
            projeto=self.project,
            nome='Sprint 1',
            descricao='Primeira sprint',
            data_inicio=date.today(),
            data_fim=date.today() + timedelta(days=14),
            status='PLANEJADO',
            criado_por=self.admin
        )
        
        self.client = APIClient()
        self.client.force_authenticate(user=self.admin)
    
    # Project Creation Tests
    def test_create_project_success(self):
        """Test creating a new project with valid data"""
        url = reverse('project-list')
        data = {
            'titulo': 'Novo Projeto',
            'descricao': 'Descrição do novo projeto',
            'data_inicio': date.today().isoformat(),
            'data_fim': (date.today() + timedelta(days=30)).isoformat(),
            'status': 'PLANEJADO',
            'prioridade': 'ALTA',
            'criado_por': self.admin.id
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, 201)
        self.assertEqual(Projeto.objects.count(), 2)  # 1 from setUp + 1 new
        self.assertEqual(Projeto.objects.latest('id').titulo, 'Novo Projeto')
    
    def test_create_project_invalid_dates(self):
        """Test creating a project with invalid date range"""
        url = reverse('project-list')
        data = {
            'titulo': 'Projeto Datas Inválidas',
            'descricao': 'Projeto com datas inválidas',
            'data_inicio': date.today().isoformat(),
            'data_fim': (date.today() - timedelta(days=1)).isoformat(),  # End date before start date
            'status': 'PLANEJADO',
            'prioridade': 'BAIXA',
            'criado_por': self.admin.id
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, 400)
        self.assertIn('data_fim', response.data)
    
    def test_create_project_missing_required_fields(self):
        """Test creating a project with missing required fields"""
        url = reverse('project-list')
        data = {
            'titulo': 'Projeto Incompleto',
            # Missing required fields
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, 400)
        self.assertIn('descricao', response.data)
        self.assertIn('data_inicio', response.data)
        self.assertIn('data_fim', response.data)
    
    # Project Retrieval Tests
    def test_list_projects(self):
        """Test listing all projects"""
        url = reverse('project-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)  # Should have the project from setUp
        self.assertEqual(response.data[0]['titulo'], self.project.titulo)
    
    def test_retrieve_project(self):
        """Test retrieving a single project"""
        url = reverse('project-detail', args=[self.project.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['titulo'], self.project.titulo)
    
    def test_retrieve_nonexistent_project(self):
        """Test retrieving a project that doesn't exist"""
        url = reverse('project-detail', args=[9999])  # Non-existent ID
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)
    
    # Project Update Tests
    def test_update_project(self):
        """Test updating a project"""
        url = reverse('project-detail', args=[self.project.id])
        data = {
            'titulo': 'Projeto Atualizado',
            'descricao': self.project.descricao,
            'data_inicio': self.project.data_inicio.isoformat(),
            'data_fim': (self.project.data_fim + timedelta(days=7)).isoformat(),
            'status': 'EM_ANDAMENTO',
            'prioridade': 'ALTA',
            'criado_por': self.admin.id
        }
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, 200)
        self.project.refresh_from_db()
        self.assertEqual(self.project.titulo, 'Projeto Atualizado')
        self.assertEqual(self.project.status, 'EM_ANDAMENTO')
    
    def test_partial_update_project(self):
        """Test partially updating a project"""
        url = reverse('project-detail', args=[self.project.id])
        data = {'status': 'PAUSADO'}
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, 200)
        self.project.refresh_from_db()
        self.assertEqual(self.project.status, 'PAUSADO')
    
    # Project Deletion Tests
    def test_delete_project(self):
        """Test deleting a project"""
        url = reverse('project-detail', args=[self.project.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, 204)
        self.assertEqual(Projeto.objects.count(), 0)
    
    # Project Members Tests
    def test_list_project_members(self):
        """Test listing project members"""
        url = reverse('project-members', args=[self.project.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)  # Should have 1 member from setUp
    
    def test_add_project_member(self):
        """Test adding a member to a project"""
        # Create a new user to add as member
        new_user = User.objects.create_user(
            email='newuser@planify.com',
            username='newuser',
            full_name='Novo Usuário',
            password='test123'
        )
        
        url = reverse('project-members', args=[self.project.id])
        data = {
            'usuario': new_user.id,
            'papel': 'ANALISTA'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, 201)
        self.assertTrue(MembroProjeto.objects.filter(projeto=self.project, usuario=new_user).exists())
    
    # Project Sprints Tests
    def test_list_project_sprints(self):
        """Test listing project sprints"""
        url = reverse('project-sprints', args=[self.project.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)  # Should have 1 sprint from setUp
    
    def test_create_project_sprint(self):
        """Test creating a new sprint for a project"""
        url = reverse('project-sprints', args=[self.project.id])
        data = {
            'nome': 'Sprint 2',
            'descricao': 'Segunda sprint do projeto',
            'data_inicio': (date.today() + timedelta(days=15)).isoformat(),
            'data_fim': (date.today() + timedelta(days=28)).isoformat(),
            'status': 'PLANEJADO'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, 201)
        self.assertEqual(self.project.sprints.count(), 2)  # 1 from setUp + 1 new
    
    # Authentication & Permissions Tests
    def test_unauthenticated_access(self):
        """Test that unauthenticated users can't access protected endpoints"""
        self.client.logout()
        
        # Test list projects
        url = reverse('project-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 401)  # Unauthorized
        
        # Test retrieve project
        url = reverse('project-detail', args=[self.project.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 401)  # Unauthorized
    
    def test_regular_user_permissions(self):
        """Test that regular users have appropriate permissions"""
        self.client.force_authenticate(user=self.user)
        
        # Regular user can view projects they're a member of
        url = reverse('project-detail', args=[self.project.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        
        # Regular user can't create projects
        url = reverse('project-list')
        data = {
            'titulo': 'Projeto não autorizado',
            'descricao': 'Este usuário não deveria poder criar projetos',
            'data_inicio': date.today().isoformat(),
            'data_fim': (date.today() + timedelta(days=30)).isoformat(),
            'status': 'PLANEJADO',
            'prioridade': 'BAIXA',
            'criado_por': self.user.id
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, 403)  # Forbidden
    
    # Project Status History Tests
    def test_project_status_history(self):
        """Test that status changes are tracked in history"""
        # Initial status is PLANEJADO (from setUp)
        self.assertEqual(self.project.status, 'PLANEJADO')
        
        # Change status to EM_ANDAMENTO
        url = reverse('project-detail', args=[self.project.id])
        data = {'status': 'EM_ANDAMENTO'}
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, 200)
        
        # Check history
        history_url = reverse('project-history', args=[self.project.id])
        response = self.client.get(history_url)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(len(response.data) > 0)  # Should have at least one history entry
        self.assertEqual(response.data[0]['status_anterior'], 'PLANEJADO')
        # Note: The new status would be in the next history entry if we were tracking it
        
    # Project Archival Tests
    def test_archive_project(self):
        """Test archiving a project"""
        self.assertFalse(self.project.arquivado)
        
        url = reverse('project-archive', args=[self.project.id])
        response = self.client.post(url)
        self.assertEqual(response.status_code, 200)
        
        self.project.refresh_from_db()
        self.assertTrue(self.project.arquivado)
    
    def test_unarchive_project(self):
        """Test unarchiving a project"""
        self.project.arquivado = True
        self.project.save()
        
        url = reverse('project-unarchive', args=[self.project.id])
        response = self.client.post(url)
        self.assertEqual(response.status_code, 200)
        
        self.project.refresh_from_db()
        self.assertFalse(self.project.arquivado)
    
    # Project Filtering Tests
    def test_filter_projects_by_status(self):
        """Test filtering projects by status"""
        # Create projects with different statuses
        Projeto.objects.create(
            titulo='Projeto em Andamento',
            descricao='Projeto em andamento',
            data_inicio=date.today(),
            data_fim=date.today() + timedelta(days=30),
            status='EM_ANDAMENTO',
            prioridade='MEDIA',
            criado_por=self.admin
        )
        
        url = f"{reverse('project-list')}?status=EM_ANDAMENTO"
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['titulo'], 'Projeto em Andamento')
    
    def test_search_projects(self):
        """Test searching projects by title"""
        # Create a project with a unique title
        Projeto.objects.create(
            titulo='Projeto de Pesquisa',
            descricao='Projeto de pesquisa acadêmica',
            data_inicio=date.today(),
            data_fim=date.today() + timedelta(days=60),
            status='PLANEJADO',
            prioridade='BAIXA',
            criado_por=self.admin
        )
        
        url = f"{reverse('project-list')}?search=pesquisa"
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['titulo'], 'Projeto de Pesquisa')
