"""
Testes para as views do módulo Teams.
"""
import json
from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from rest_framework import status
from teams.models import Equipe, MembroEquipe, PermissaoEquipe

User = get_user_model()  # type: ignore


class EquipeViewSetTest(TestCase):
    """Testes para o EquipeViewSet"""
    
    def setUp(self):
        """Configuração inicial para os testes"""
        self.client = APIClient()
        self.user1 = User.objects.create_user(  # type: ignore
            username='user1',
            email='user1@example.com',
            password='testpass123',
            first_name='User',
            last_name='One'
        )
        self.user2 = User.objects.create_user(  # type: ignore
            username='user2',
            email='user2@example.com',
            password='testpass123',
            first_name='User',
            last_name='Two'
        )
        
        # Configura authentication
        self.client.force_authenticate(user=self.user1)
        
        # Cria equipes de teste
        self.equipe1 = Equipe.objects.create(
            nome="Equipe 1",
            descricao="Primeira equipe de teste",
            criado_por=self.user1
        )
        self.equipe2 = Equipe.objects.create(
            nome="Equipe 2",
            descricao="Segunda equipe de teste",
            criado_por=self.user2
        )
        
    def test_list_equipes(self):
        """Testa a listagem de equipes"""
        url = reverse('equipe-list')
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.json()
        
        # Deve retornar ambas as equipes
        self.assertEqual(len(data['results']), 2)
        
        # Verifica campos da listagem
        equipe_data = data['results'][0]
        expected_fields = ['id', 'nome', 'criado_por_nome', 'criado_em', 'total_membros']
        for field in expected_fields:
            self.assertIn(field, equipe_data)
            
    def test_retrieve_equipe(self):
        """Testa a recuperação de uma equipe específica"""
        url = reverse('equipe-detail', kwargs={'pk': self.equipe1.pk})
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.json()
        
        self.assertEqual(data['nome'], self.equipe1.nome)
        self.assertEqual(data['descricao'], self.equipe1.descricao)
        self.assertIn('membros', data)
        self.assertIn('permissoes', data)
        self.assertIn('total_membros', data)
        
    def test_create_equipe(self):
        """Testa a criação de uma nova equipe"""
        url = reverse('equipe-list')
        data = {
            'nome': 'Nova Equipe',
            'descricao': 'Descrição da nova equipe'
        }
        
        response = self.client.post(url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        
        # Verifica se a equipe foi criada
        nova_equipe = Equipe.objects.get(nome='Nova Equipe')
        self.assertEqual(nova_equipe.criado_por, self.user1)
        
        # Verifica se o criador foi adicionado como membro PO
        membro = MembroEquipe.objects.filter(
            equipe=nova_equipe,
            usuario=self.user1,
            papel='PO'
        ).first()
        self.assertIsNotNone(membro)
        
    def test_update_equipe(self):
        """Testa a atualização de uma equipe"""
        url = reverse('equipe-detail', kwargs={'pk': self.equipe1.pk})
        data = {
            'nome': 'Equipe Atualizada',
            'descricao': 'Descrição atualizada'
        }
        
        response = self.client.put(url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Verifica se a equipe foi atualizada
        self.equipe1.refresh_from_db()
        self.assertEqual(self.equipe1.nome, 'Equipe Atualizada')
        self.assertEqual(self.equipe1.descricao, 'Descrição atualizada')
        
    def test_partial_update_equipe(self):
        """Testa a atualização parcial de uma equipe"""
        url = reverse('equipe-detail', kwargs={'pk': self.equipe1.pk})
        data = {'nome': 'Nome Parcialmente Atualizado'}
        
        response = self.client.patch(url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Verifica se apenas o nome foi atualizado
        self.equipe1.refresh_from_db()
        self.assertEqual(self.equipe1.nome, 'Nome Parcialmente Atualizado')
        self.assertEqual(self.equipe1.descricao, 'Primeira equipe de teste')  # Não deve ter mudado
        
    def test_delete_equipe(self):
        """Testa a exclusão de uma equipe"""
        url = reverse('equipe-detail', kwargs={'pk': self.equipe1.pk})
        response = self.client.delete(url)
        
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        
        # Verifica se a equipe foi deletada
        self.assertFalse(Equipe.objects.filter(pk=self.equipe1.pk).exists())
        
    def test_filter_by_texto(self):
        """Testa o filtro por texto"""
        url = reverse('equipe-list')
        response = self.client.get(url, {'texto': 'Primeira'})
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.json()
        
        # Deve retornar apenas a equipe1 que contém "Primeira" na descrição
        self.assertEqual(len(data['results']), 1)
        self.assertEqual(data['results'][0]['nome'], self.equipe1.nome)
        
    def test_filter_by_usuario(self):
        """Testa o filtro por usuário membro"""
        # Adiciona user2 como membro da equipe1
        MembroEquipe.objects.create(
            equipe=self.equipe1,
            usuario=self.user2,
            papel='DEV',
            adicionado_por=self.user1
        )
        
        url = reverse('equipe-list')
        response = self.client.get(url, {'usuario': self.user2.pk})
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.json()
        
        # Deve retornar apenas a equipe1
        self.assertEqual(len(data['results']), 1)
        self.assertEqual(data['results'][0]['nome'], self.equipe1.nome)
        
    def test_filter_minhas_equipes(self):
        """Testa o filtro de minhas equipes"""
        # Adiciona user1 como membro da equipe2
        MembroEquipe.objects.create(
            equipe=self.equipe2,
            usuario=self.user1,
            papel='DEV',
            adicionado_por=self.user2
        )
        
        url = reverse('equipe-list')
        response = self.client.get(url, {'minhas_equipes': 'true'})
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.json()
        
        # Deve retornar apenas a equipe2 (user1 é membro)
        self.assertEqual(len(data['results']), 1)
        self.assertEqual(data['results'][0]['nome'], self.equipe2.nome)
        
    def test_authentication_required(self):
        """Testa que autenticação é obrigatória"""
        self.client.force_authenticate(user=None)  # type: ignore
        
        url = reverse('equipe-list')
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class EquipeActionTest(TestCase):
    """Testes para as actions customizadas do EquipeViewSet"""
    
    def setUp(self):
        """Configuração inicial para os testes"""
        self.client = APIClient()
        self.user1 = User.objects.create_user(  # type: ignore
            username='user1',
            email='user1@example.com',
            password='testpass123',
            first_name='User',
            last_name='One'
        )
        self.user2 = User.objects.create_user(  # type: ignore
            username='user2',
            email='user2@example.com',
            password='testpass123',
            first_name='User',
            last_name='Two'
        )
        self.user3 = User.objects.create_user(  # type: ignore
            username='user3',
            email='user3@example.com',
            password='testpass123',
            first_name='User',
            last_name='Three'
        )
        
        self.client.force_authenticate(user=self.user1)
        
        self.equipe = Equipe.objects.create(
            nome="Equipe Teste",
            criado_por=self.user1
        )
        
        # Adiciona alguns membros
        self.membro1 = MembroEquipe.objects.create(
            equipe=self.equipe,
            usuario=self.user1,
            papel='PO',
            adicionado_por=self.user1
        )
        self.membro2 = MembroEquipe.objects.create(
            equipe=self.equipe,
            usuario=self.user2,
            papel='DEV',
            adicionado_por=self.user1
        )
        
    def test_action_membros(self):
        """Testa a action membros"""
        url = reverse('equipe-membros', kwargs={'pk': self.equipe.pk})
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.json()
        
        self.assertEqual(len(data), 2)  # Dois membros
        
        # Verifica se os dados dos membros estão corretos
        membros_usuarios = [membro['usuario'] for membro in data]
        self.assertIn(self.user1.pk, membros_usuarios)
        self.assertIn(self.user2.pk, membros_usuarios)
        
    def test_action_adicionar_membro(self):
        """Testa a action adicionar_membro"""
        url = reverse('equipe-adicionar-membro', kwargs={'pk': self.equipe.pk})
        data = {
            'usuario': self.user3.pk,
            'papel': 'QA'
        }
        
        response = self.client.post(url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        
        # Verifica se o membro foi adicionado
        novo_membro = MembroEquipe.objects.filter(
            equipe=self.equipe,
            usuario=self.user3,
            papel='QA'
        ).first()
        self.assertIsNotNone(novo_membro)
        
    def test_action_atualizar_papel_membro(self):
        """Testa a action atualizar_papel_membro"""
        url = reverse('equipe-atualizar-papel-membro', kwargs={'pk': self.equipe.pk})
        data = {
            'usuario': self.user2.pk,
            'papel': 'SM'
        }
        
        response = self.client.post(url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Verifica se o papel foi atualizado
        self.membro2.refresh_from_db()
        self.assertEqual(self.membro2.papel, 'SM')
        
    def test_action_remover_membro(self):
        """Testa a action remover_membro"""
        url = reverse('equipe-remover-membro', kwargs={'pk': self.equipe.pk})
        data = {'usuario': self.user2.pk}
        
        response = self.client.post(url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        
        # Verifica se o membro foi removido
        self.assertFalse(
            MembroEquipe.objects.filter(
                equipe=self.equipe,
                usuario=self.user2
            ).exists()
        )
        
    def test_action_usuarios_disponiveis(self):
        """Testa a action usuarios_disponiveis"""
        url = reverse('equipe-usuarios-disponiveis')
        response = self.client.get(url, {'equipe': self.equipe.pk})
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.json()
        
        # Deve retornar apenas user3 (user1 e user2 já são membros)
        self.assertEqual(len(data), 1)
        self.assertEqual(data[0]['id'], self.user3.pk)
        
    def test_action_adicionar_membro_usuario_ja_membro(self):
        """Testa adicionar membro que já é membro da equipe"""
        url = reverse('equipe-adicionar-membro', kwargs={'pk': self.equipe.pk})
        data = {
            'usuario': self.user2.pk,  # user2 já é membro
            'papel': 'QA'
        }
        
        response = self.client.post(url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        
    def test_action_atualizar_papel_membro_inexistente(self):
        """Testa atualizar papel de membro que não existe"""
        url = reverse('equipe-atualizar-papel-membro', kwargs={'pk': self.equipe.pk})
        data = {
            'usuario': self.user3.pk,  # user3 não é membro
            'papel': 'SM'
        }
        
        response = self.client.post(url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        
    def test_action_remover_membro_inexistente(self):
        """Testa remover membro que não existe"""
        url = reverse('equipe-remover-membro', kwargs={'pk': self.equipe.pk})
        data = {'usuario': self.user3.pk}  # user3 não é membro
        
        response = self.client.post(url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class PermissaoEquipeViewSetTest(TestCase):
    """Testes para o PermissaoEquipeViewSet"""
    
    def setUp(self):
        """Configuração inicial para os testes"""
        self.client = APIClient()
        self.user = User.objects.create_user(  # type: ignore
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        
        self.client.force_authenticate(user=self.user)
        
        self.equipe = Equipe.objects.create(
            nome="Equipe Teste",
            criado_por=self.user
        )
        
        self.permissao = PermissaoEquipe.objects.create(
            papel='DEV',
            equipe=self.equipe,
            modulo='TASKS',
            permissao='CREATE'
        )
        
    def test_list_permissoes(self):
        """Testa a listagem de permissões"""
        url = reverse('permissao-equipe-list')
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.json()
        
        self.assertEqual(len(data['results']), 1)
        permissao_data = data['results'][0]
        
        self.assertEqual(permissao_data['papel'], 'DEV')
        self.assertEqual(permissao_data['papel_display'], 'Desenvolvedor')
        self.assertEqual(permissao_data['modulo'], 'TASKS')
        self.assertEqual(permissao_data['modulo_display'], 'Tarefas')
        self.assertEqual(permissao_data['permissao'], 'CREATE')
        self.assertEqual(permissao_data['permissao_display'], 'Criar')
        
    def test_retrieve_permissao(self):
        """Testa a recuperação de uma permissão específica"""
        url = reverse('permissao-equipe-detail', kwargs={'pk': self.permissao.pk})
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.json()
        
        self.assertEqual(data['papel'], 'DEV')
        self.assertEqual(data['equipe'], self.equipe.pk)
        self.assertEqual(data['modulo'], 'TASKS')
        self.assertEqual(data['permissao'], 'CREATE')
        
    def test_create_permissao(self):
        """Testa a criação de uma nova permissão"""
        url = reverse('permissao-equipe-list')
        data = {
            'papel': 'PO',
            'equipe': self.equipe.pk,
            'modulo': 'PROJECTS',
            'permissao': 'UPDATE'
        }
        
        response = self.client.post(url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        
        # Verifica se a permissão foi criada
        nova_permissao = PermissaoEquipe.objects.get(
            papel='PO',
            equipe=self.equipe,
            modulo='PROJECTS',
            permissao='UPDATE'
        )
        self.assertIsNotNone(nova_permissao)
        
    def test_update_permissao(self):
        """Testa a atualização de uma permissão"""
        url = reverse('permissao-equipe-detail', kwargs={'pk': self.permissao.pk})
        data = {
            'papel': 'QA',
            'equipe': self.equipe.pk,
            'modulo': 'TASKS',
            'permissao': 'READ'
        }
        
        response = self.client.put(url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Verifica se a permissão foi atualizada
        self.permissao.refresh_from_db()
        self.assertEqual(self.permissao.papel, 'QA')
        self.assertEqual(self.permissao.permissao, 'READ')
        
    def test_partial_update_permissao(self):
        """Testa a atualização parcial de uma permissão"""
        url = reverse('permissao-equipe-detail', kwargs={'pk': self.permissao.pk})
        data = {'permissao': 'DELETE'}
        
        response = self.client.patch(url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Verifica se apenas a permissão foi atualizada
        self.permissao.refresh_from_db()
        self.assertEqual(self.permissao.permissao, 'DELETE')
        self.assertEqual(self.permissao.papel, 'DEV')  # Não deve ter mudado
        
    def test_delete_permissao(self):
        """Testa a exclusão de uma permissão"""
        url = reverse('permissao-equipe-detail', kwargs={'pk': self.permissao.pk})
        response = self.client.delete(url)
        
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        
        # Verifica se a permissão foi deletada
        self.assertFalse(PermissaoEquipe.objects.filter(pk=self.permissao.pk).exists())
        
    def test_create_permissao_duplicada(self):
        """Testa que não é possível criar permissões duplicadas"""
        url = reverse('permissao-equipe-list')
        data = {
            'papel': 'DEV',
            'equipe': self.equipe.pk,
            'modulo': 'TASKS',
            'permissao': 'CREATE'  # Mesma combinação da permissão existente
        }
        
        response = self.client.post(url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        
    def test_authentication_required(self):
        """Testa que autenticação é obrigatória"""
        self.client.force_authenticate(user=None)  # type: ignore
        
        url = reverse('permissao-equipe-list')
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class SearchAndFilterTest(TestCase):
    """Testes para funcionalidades de busca e filtro"""
    
    def setUp(self):
        """Configuração inicial para os testes"""
        self.client = APIClient()
        self.user = User.objects.create_user(  # type: ignore
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        
        self.client.force_authenticate(user=self.user)
        
        # Cria várias equipes para testar filtros
        self.equipe_dev = Equipe.objects.create(
            nome="Equipe de Desenvolvimento",
            descricao="Equipe responsável pelo desenvolvimento do sistema",
            criado_por=self.user
        )
        self.equipe_qa = Equipe.objects.create(
            nome="Equipe de QA",
            descricao="Equipe responsável pela qualidade",
            criado_por=self.user
        )
        self.equipe_design = Equipe.objects.create(
            nome="Equipe de Design",
            descricao="Equipe responsável pelo design do produto",
            criado_por=self.user
        )
        
    def test_search_by_nome(self):
        """Testa busca por nome da equipe"""
        url = reverse('equipe-list')
        response = self.client.get(url, {'search': 'Desenvolvimento'})
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.json()
        
        self.assertEqual(len(data['results']), 1)
        self.assertEqual(data['results'][0]['nome'], self.equipe_dev.nome)
        
    def test_search_by_descricao(self):
        """Testa busca por descrição da equipe"""
        url = reverse('equipe-list')
        response = self.client.get(url, {'search': 'qualidade'})
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.json()
        
        self.assertEqual(len(data['results']), 1)
        self.assertEqual(data['results'][0]['nome'], self.equipe_qa.nome)
        
    def test_ordering_by_nome(self):
        """Testa ordenação por nome"""
        url = reverse('equipe-list')
        response = self.client.get(url, {'ordering': 'nome'})
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.json()
        
        nomes = [equipe['nome'] for equipe in data['results']]
        self.assertEqual(nomes, sorted(nomes))
        
    def test_ordering_by_criado_em_desc(self):
        """Testa ordenação por data de criação (decrescente)"""
        url = reverse('equipe-list')
        response = self.client.get(url, {'ordering': '-criado_em'})
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.json()
        
        # A equipe mais recente deve ser a primeira
        self.assertEqual(data['results'][0]['nome'], self.equipe_design.nome)
        
    def test_combined_search_and_ordering(self):
        """Testa busca combinada com ordenação"""
        url = reverse('equipe-list')
        response = self.client.get(url, {
            'search': 'Equipe',
            'ordering': 'nome'
        })
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.json()
        
        # Deve retornar todas as equipes (todas contêm "Equipe" no nome)
        self.assertEqual(len(data['results']), 3)
        
        # Deve estar ordenado por nome
        nomes = [equipe['nome'] for equipe in data['results']]
        self.assertEqual(nomes, sorted(nomes))
