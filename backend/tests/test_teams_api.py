from rest_framework.test import APITestCase, APIClient
from django.urls import reverse
from users.models import User
from teams.models import Equipe, MembroEquipe, PermissaoEquipe

class TeamAPITests(APITestCase):
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

    def test_create_team(self):
        """Teste de criação de equipe"""
        url = reverse('equipe-list')
        data = {
            'nome': 'Equipe Teste',
            'descricao': 'Descrição da equipe teste'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, 201)
        self.assertTrue(Equipe.objects.filter(nome='Equipe Teste').exists())

    def test_list_teams(self):
        """Teste de listagem de equipes"""
        Equipe.objects.create(
            nome='Equipe Lista',
            descricao='Equipe para teste de listagem',
            criado_por=self.admin
        )
        
        url = reverse('equipe-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertGreaterEqual(len(response.data['results']), 1)

    def test_get_team_detail(self):
        """Teste de detalhes da equipe"""
        equipe = Equipe.objects.create(
            nome='Equipe Detalhes',
            descricao='Equipe para teste de detalhes',
            criado_por=self.admin
        )
        
        url = reverse('equipe-detail', kwargs={'pk': equipe.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['nome'], 'Equipe Detalhes')

    def test_update_team(self):
        """Teste de atualização de equipe"""
        equipe = Equipe.objects.create(
            nome='Equipe Atualizar',
            descricao='Equipe para atualizar',
            criado_por=self.admin
        )
        
        url = reverse('equipe-detail', kwargs={'pk': equipe.pk})
        data = {
            'nome': 'Equipe Atualizada',
            'descricao': 'Descrição atualizada'
        }
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, 200)
        equipe.refresh_from_db()
        self.assertEqual(equipe.nome, 'Equipe Atualizada')

    def test_delete_team(self):
        """Teste de exclusão de equipe"""
        equipe = Equipe.objects.create(
            nome='Equipe Deletar',
            descricao='Equipe para deletar',
            criado_por=self.admin
        )
        
        url = reverse('equipe-detail', kwargs={'pk': equipe.pk})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, 204)
        self.assertFalse(Equipe.objects.filter(pk=equipe.pk).exists())

    def test_add_team_member(self):
        """Teste de adição de membro à equipe"""
        equipe = Equipe.objects.create(
            nome='Equipe Membro',
            descricao='Equipe para teste de membros',
            criado_por=self.admin
        )
        
        url = reverse('equipe-adicionar-membro', kwargs={'pk': equipe.pk})
        data = {
            'usuario': self.user.pk,
            'papel': 'DEV'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, 201)
        self.assertTrue(MembroEquipe.objects.filter(
            equipe=equipe,
            usuario=self.user,
            papel='DEV'
        ).exists())

    def test_remove_team_member(self):
        """Teste de remoção de membro da equipe"""
        equipe = Equipe.objects.create(
            nome='Equipe Remover',
            descricao='Equipe para teste de remoção',
            criado_por=self.admin
        )
        
        # Adicionar membro primeiro
        membro = MembroEquipe.objects.create(
            equipe=equipe,
            usuario=self.user,
            papel='DEV',
            adicionado_por=self.admin
        )
        
        url = reverse('equipe-remover-membro', kwargs={'pk': equipe.pk})
        data = {'usuario': self.user.pk}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, 200)
        self.assertFalse(MembroEquipe.objects.filter(pk=membro.pk).exists())

    def test_team_permissions(self):
        """Teste de permissões da equipe"""
        equipe = Equipe.objects.create(
            nome='Equipe Permissões',
            descricao='Equipe para teste de permissões',
            criado_por=self.admin
        )
        
        url = reverse('equipe-gerenciar-permissoes', kwargs={'pk': equipe.pk})
        data = {
            'papel': 'DEV',
            'modulo': 'TASKS',
            'permissao': 'CREATE'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, 201)
        self.assertTrue(PermissaoEquipe.objects.filter(
            equipe=equipe,
            papel='DEV',
            modulo='TASKS',
            permissao='CREATE'
        ).exists())

    def test_list_team_members(self):
        """Teste de listagem de membros da equipe"""
        equipe = Equipe.objects.create(
            nome='Equipe Membros',
            descricao='Equipe para teste de listagem de membros',
            criado_por=self.admin
        )
        
        MembroEquipe.objects.create(
            equipe=equipe,
            usuario=self.user,
            papel='DEV',
            adicionado_por=self.admin
        )
        
        url = reverse('equipe-membros', kwargs={'pk': equipe.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertGreaterEqual(len(response.data), 1)

    def test_team_search(self):
        """Teste de busca de equipes"""
        Equipe.objects.create(
            nome='Equipe Python',
            descricao='Equipe de desenvolvimento Python',
            criado_por=self.admin
        )
        
        url = reverse('equipe-list')
        response = self.client.get(url, {'search': 'Python'})
        self.assertEqual(response.status_code, 200)
        self.assertGreaterEqual(len(response.data['results']), 1)

    def test_team_validation(self):
        """Teste de validação de dados da equipe"""
        url = reverse('equipe-list')
        data = {
            'nome': '',  # Nome vazio (inválido)
            'descricao': 'Descrição'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, 400)

    def test_team_permissions_unauthorized(self):
        """Teste de permissões sem autenticação"""
        self.client.logout()
        url = reverse('equipe-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 401)
