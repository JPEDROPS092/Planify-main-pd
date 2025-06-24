"""
Testes para as views do módulo Teams usando pytest.
"""
import pytest
from django.urls import reverse
from django.contrib.auth import get_user_model
from rest_framework import status
from teams.models import Equipe, MembroEquipe, PermissaoEquipe

User = get_user_model()


@pytest.mark.django_db
class TestEquipeViewSet:
    """Testes para o EquipeViewSet"""
    
    def test_list_equipes_unauthenticated(self, api_client):
        """Testa acesso não autenticado à listagem de equipes."""
        url = reverse('equipe-list')
        response = api_client.get(url)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
    
    def test_list_equipes(self, authenticated_client, equipe1, equipe2):
        """Testa a listagem de equipes"""
        url = reverse('equipe-list')
        response = authenticated_client.get(url)
        
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        
        # Deve retornar ambas as equipes
        assert len(data['results']) == 2
        
        # Verifica campos da listagem
        equipe_data = data['results'][0]
        expected_fields = ['id', 'nome', 'criado_por_nome', 'criado_em', 'total_membros']
        for field in expected_fields:
            assert field in equipe_data
    
    def test_list_equipes_filtro_texto(self, authenticated_client, equipe1, equipe2):
        """Testa filtro por texto na listagem de equipes."""
        url = reverse('equipe-list')
        response = authenticated_client.get(url, {'texto': 'Equipe 1'})
        
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert len(data['results']) == 1
        assert data['results'][0]['nome'] == 'Equipe 1'
    
    def test_list_equipes_filtro_minhas_equipes(self, authenticated_client, equipe_teste, membro_equipe_user1):
        """Testa filtro de minhas equipes."""
        url = reverse('equipe-list')
        response = authenticated_client.get(url, {'minhas_equipes': 'true'})
        
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert len(data['results']) == 1
        assert data['results'][0]['nome'] == 'Equipe Teste'
    
    def test_list_equipes_filtro_usuario(self, authenticated_client, equipe_teste, membro_equipe_user1, user1):
        """Testa filtro por usuário específico."""
        url = reverse('equipe-list')
        response = authenticated_client.get(url, {'usuario': user1.id})
        
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert len(data['results']) == 1
        assert data['results'][0]['nome'] == 'Equipe Teste'
            
    def test_retrieve_equipe(self, authenticated_client, equipe1):
        """Testa a recuperação de uma equipe específica"""
        url = reverse('equipe-detail', kwargs={'pk': equipe1.pk})
        response = authenticated_client.get(url)
        
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        
        assert data['nome'] == equipe1.nome
        assert data['descricao'] == equipe1.descricao
        assert 'membros' in data
        assert 'permissoes' in data
        assert 'total_membros' in data
    
    def test_retrieve_equipe_inexistente(self, authenticated_client):
        """Testa recuperação de equipe inexistente."""
        url = reverse('equipe-detail', kwargs={'pk': 99999})
        response = authenticated_client.get(url)
        assert response.status_code == status.HTTP_404_NOT_FOUND
        
    def test_create_equipe(self, authenticated_client, user1):
        """Testa a criação de uma nova equipe"""
        url = reverse('equipe-list')
        data = {
            'nome': 'Nova Equipe',
            'descricao': 'Descrição da nova equipe'
        }
        
        response = authenticated_client.post(url, data, format='json')
        
        assert response.status_code == status.HTTP_201_CREATED
        data = response.json()
        
        assert data['nome'] == 'Nova Equipe'
        assert data['descricao'] == 'Descrição da nova equipe'
        assert data['criado_por'] == user1.id
        
        # Verifica se a equipe foi criada no banco
        equipe = Equipe.objects.get(id=data['id'])
        assert equipe.nome == 'Nova Equipe'
        assert equipe.criado_por == user1
    
    def test_create_equipe_sem_nome(self, authenticated_client):
        """Testa criação de equipe sem nome."""
        url = reverse('equipe-list')
        data = {
            'descricao': 'Equipe sem nome'
        }
        
        response = authenticated_client.post(url, data, format='json')
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert 'nome' in response.json()
    
    def test_update_equipe(self, authenticated_client, equipe1):
        """Testa atualização de equipe."""
        url = reverse('equipe-detail', kwargs={'pk': equipe1.pk})
        data = {
            'nome': 'Nome Atualizado',
            'descricao': 'Descrição atualizada'
        }
        
        response = authenticated_client.put(url, data, format='json')
        
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data['nome'] == 'Nome Atualizado'
        assert data['descricao'] == 'Descrição atualizada'
        
        # Verifica no banco
        equipe1.refresh_from_db()
        assert equipe1.nome == 'Nome Atualizado'
    
    def test_partial_update_equipe(self, authenticated_client, equipe1):
        """Testa atualização parcial de equipe."""
        url = reverse('equipe-detail', kwargs={'pk': equipe1.pk})
        data = {'nome': 'Novo Nome'}
        
        response = authenticated_client.patch(url, data, format='json')
        
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data['nome'] == 'Novo Nome'
        assert data['descricao'] == equipe1.descricao  # Não deve mudar
    
    def test_delete_equipe(self, authenticated_client, equipe1):
        """Testa exclusão de equipe."""
        url = reverse('equipe-detail', kwargs={'pk': equipe1.pk})
        equipe_id = equipe1.id
        
        response = authenticated_client.delete(url)
        
        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert not Equipe.objects.filter(id=equipe_id).exists()


@pytest.mark.django_db
class TestEquipeViewSetActions:
    """Testes para as actions customizadas do EquipeViewSet."""
    
    def test_action_membros(self, authenticated_client, equipe_teste, membro_equipe_user1, membro_equipe_user2):
        """Testa action para listar membros da equipe."""
        url = reverse('equipe-membros', kwargs={'pk': equipe_teste.pk})
        response = authenticated_client.get(url)
        
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        
        assert len(data) == 2
        assert all('usuario_nome' in membro for membro in data)
        assert all('papel_display' in membro for membro in data)
    
    def test_action_adicionar_membro(self, authenticated_client, equipe_teste, user3):
        """Testa action para adicionar membro à equipe."""
        url = reverse('equipe-adicionar-membro', kwargs={'pk': equipe_teste.pk})
        data = {
            'usuario': user3.id,
            'papel': 'QA'
        }
        
        response = authenticated_client.post(url, data, format='json')
        
        assert response.status_code == status.HTTP_201_CREATED
        data = response.json()
        
        assert data['usuario'] == user3.id
        assert data['papel'] == 'QA'
        assert data['equipe'] == equipe_teste.id
        
        # Verifica no banco
        assert MembroEquipe.objects.filter(equipe=equipe_teste, usuario=user3).exists()
    
    def test_action_adicionar_membro_duplicado(self, authenticated_client, equipe_teste, membro_equipe_user1, user1):
        """Testa adicionar membro já existente na equipe."""
        url = reverse('equipe-adicionar-membro', kwargs={'pk': equipe_teste.pk})
        data = {
            'usuario': user1.id,
            'papel': 'DEV'
        }
        
        response = authenticated_client.post(url, data, format='json')
        assert response.status_code == status.HTTP_400_BAD_REQUEST
    
    def test_action_atualizar_papel_membro(self, authenticated_client, equipe_teste, membro_equipe_user2, user2):
        """Testa action para atualizar papel do membro."""
        url = reverse('equipe-atualizar-papel-membro', kwargs={'pk': equipe_teste.pk})
        data = {
            'usuario': user2.id,
            'papel': 'SM'
        }
        
        response = authenticated_client.post(url, data, format='json')
        
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data['papel'] == 'SM'
        
        # Verifica no banco
        membro_equipe_user2.refresh_from_db()
        assert membro_equipe_user2.papel == 'SM'
    
    def test_action_remover_membro(self, authenticated_client, equipe_teste, membro_equipe_user2, user2):
        """Testa action para remover membro da equipe."""
        url = reverse('equipe-remover-membro', kwargs={'pk': equipe_teste.pk})
        data = {'usuario': user2.id}
        
        response = authenticated_client.post(url, data, format='json')
        
        assert response.status_code == status.HTTP_204_NO_CONTENT
        
        # Verifica no banco
        assert not MembroEquipe.objects.filter(equipe=equipe_teste, usuario=user2).exists()
    
    def test_action_usuarios_disponiveis(self, authenticated_client, equipe_teste, membro_equipe_user1, user2, user3):
        """Testa action para listar usuários disponíveis."""
        url = reverse('equipe-usuarios-disponiveis')
        response = authenticated_client.get(url, {'equipe': equipe_teste.id})
        
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        
        # user1 é membro, então não deve aparecer
        # user2 e user3 devem aparecer
        user_ids = [user['id'] for user in data]
        assert membro_equipe_user1.usuario.id not in user_ids
        assert user2.id in user_ids
        assert user3.id in user_ids


@pytest.mark.django_db
class TestPermissaoEquipeViewSet:
    """Testes para o PermissaoEquipeViewSet."""
    
    def test_list_permissoes(self, authenticated_client, permissao_equipe):
        """Testa listagem de permissões."""
        url = reverse('permissaoequipe-list')
        response = authenticated_client.get(url)
        
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        
        assert len(data['results']) == 1
        permissao_data = data['results'][0]
        assert permissao_data['papel'] == 'DEV'
        assert permissao_data['modulo'] == 'TAREFAS'
        assert permissao_data['permissao'] == 'CRIAR'
    
    def test_retrieve_permissao(self, authenticated_client, permissao_equipe):
        """Testa recuperação de permissão específica."""
        url = reverse('permissaoequipe-detail', kwargs={'pk': permissao_equipe.pk})
        response = authenticated_client.get(url)
        
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        
        assert data['papel_display'] == 'Desenvolvedor'
        assert data['modulo_display'] == 'Tarefas'
        assert data['permissao_display'] == 'Criar'
    
    def test_create_permissao(self, authenticated_client, equipe_teste):
        """Testa criação de nova permissão."""
        url = reverse('permissaoequipe-list')
        data = {
            'papel': 'QA',
            'equipe': equipe_teste.id,
            'modulo': 'DOCUMENTOS',
            'permissao': 'VISUALIZAR'
        }
        
        response = authenticated_client.post(url, data, format='json')
        
        assert response.status_code == status.HTTP_201_CREATED
        data = response.json()
        
        assert data['papel'] == 'QA'
        assert data['modulo'] == 'DOCUMENTOS'
        assert data['permissao'] == 'VISUALIZAR'
        
        # Verifica no banco
        assert PermissaoEquipe.objects.filter(
            papel='QA', 
            equipe=equipe_teste, 
            modulo='DOCUMENTOS', 
            permissao='VISUALIZAR'
        ).exists()
    
    def test_create_permissao_duplicada(self, authenticated_client, permissao_equipe):
        """Testa criação de permissão duplicada."""
        url = reverse('permissaoequipe-list')
        data = {
            'papel': permissao_equipe.papel,
            'equipe': permissao_equipe.equipe.id,
            'modulo': permissao_equipe.modulo,
            'permissao': permissao_equipe.permissao
        }
        
        response = authenticated_client.post(url, data, format='json')
        assert response.status_code == status.HTTP_400_BAD_REQUEST
    
    def test_update_permissao(self, authenticated_client, permissao_equipe):
        """Testa atualização de permissão."""
        url = reverse('permissaoequipe-detail', kwargs={'pk': permissao_equipe.pk})
        data = {
            'papel': 'SM',
            'equipe': permissao_equipe.equipe.id,
            'modulo': 'SPRINTS',
            'permissao': 'EDITAR'
        }
        
        response = authenticated_client.put(url, data, format='json')
        
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data['papel'] == 'SM'
        assert data['modulo'] == 'SPRINTS'
        assert data['permissao'] == 'EDITAR'
    
    def test_delete_permissao(self, authenticated_client, permissao_equipe):
        """Testa exclusão de permissão."""
        url = reverse('permissaoequipe-detail', kwargs={'pk': permissao_equipe.pk})
        permissao_id = permissao_equipe.id
        
        response = authenticated_client.delete(url)
        
        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert not PermissaoEquipe.objects.filter(id=permissao_id).exists()


@pytest.mark.django_db
class TestSearchAndOrdering:
    """Testes para busca e ordenação."""
    
    def test_search_equipes_por_nome(self, authenticated_client, equipe1, equipe2):
        """Testa busca de equipes por nome."""
        url = reverse('equipe-list')
        response = authenticated_client.get(url, {'search': 'Equipe 1'})
        
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert len(data['results']) == 1
        assert data['results'][0]['nome'] == 'Equipe 1'
    
    def test_search_equipes_por_descricao(self, authenticated_client, equipe1, equipe2):
        """Testa busca de equipes por descrição."""
        url = reverse('equipe-list')
        response = authenticated_client.get(url, {'search': 'Primeira equipe'})
        
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert len(data['results']) == 1
        assert data['results'][0]['nome'] == 'Equipe 1'
    
    def test_ordering_equipes_por_nome(self, authenticated_client, equipe1, equipe2):
        """Testa ordenação de equipes por nome."""
        url = reverse('equipe-list')
        response = authenticated_client.get(url, {'ordering': 'nome'})
        
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        
        nomes = [equipe['nome'] for equipe in data['results']]
        assert nomes == sorted(nomes)
    
    def test_ordering_equipes_por_criacao_desc(self, authenticated_client, equipe1, equipe2):
        """Testa ordenação de equipes por data de criação descendente."""
        url = reverse('equipe-list')
        response = authenticated_client.get(url, {'ordering': '-criado_em'})
        
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        
        # Primeira equipe deve ser a mais recente
        assert data['results'][0]['nome'] == equipe2.nome


@pytest.mark.django_db
class TestPermissions:
    """Testes para permissões de acesso."""
    
    def test_acesso_nao_autenticado(self, api_client, equipe1):
        """Testa que endpoints requerem autenticação."""
        endpoints = [
            reverse('equipe-list'),
            reverse('equipe-detail', kwargs={'pk': equipe1.pk}),
            reverse('permissaoequipe-list'),
        ]
        
        for url in endpoints:
            response = api_client.get(url)
            assert response.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.mark.django_db
class TestIntegrationFlows:
    """Testes de fluxos de integração."""
    
    def test_fluxo_completo_criacao_equipe_com_membros(self, authenticated_client, user1, user2, user3):
        """Testa fluxo completo: criar equipe, adicionar membros e permissões."""
        
        # 1. Criar equipe
        url = reverse('equipe-list')
        data = {
            'nome': 'Equipe Integração',
            'descricao': 'Teste de integração completo'
        }
        response = authenticated_client.post(url, data, format='json')
        assert response.status_code == status.HTTP_201_CREATED
        equipe_data = response.json()
        equipe_id = equipe_data['id']
        
        # 2. Adicionar membros
        url_membro = reverse('equipe-adicionar-membro', kwargs={'pk': equipe_id})
        
        # Adicionar user2 como DEV
        response = authenticated_client.post(url_membro, {
            'usuario': user2.id,
            'papel': 'DEV'
        }, format='json')
        assert response.status_code == status.HTTP_201_CREATED
        
        # Adicionar user3 como QA
        response = authenticated_client.post(url_membro, {
            'usuario': user3.id,
            'papel': 'QA'
        }, format='json')
        assert response.status_code == status.HTTP_201_CREATED
        
        # 3. Criar permissões
        url_permissao = reverse('permissaoequipe-list')
        
        # Permissão para DEV
        response = authenticated_client.post(url_permissao, {
            'papel': 'DEV',
            'equipe': equipe_id,
            'modulo': 'TAREFAS',
            'permissao': 'CRIAR'
        }, format='json')
        assert response.status_code == status.HTTP_201_CREATED
        
        # 4. Verificar estado final
        url_equipe = reverse('equipe-detail', kwargs={'pk': equipe_id})
        response = authenticated_client.get(url_equipe)
        assert response.status_code == status.HTTP_200_OK
        
        data = response.json()
        # Pode incluir o criador automaticamente, então verificamos se tem pelo menos 2
        assert data['total_membros'] >= 2  # user2 + user3 (+ possivelmente criador)
        assert len(data['membros']) >= 2
        assert len(data['permissoes']) == 1
        
        # Verificar no banco
        equipe = Equipe.objects.get(id=equipe_id)
        assert equipe.nome == 'Equipe Integração'
