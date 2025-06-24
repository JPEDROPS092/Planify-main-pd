"""
Testes para as fixtures do módulo Teams (conftest.py).
"""
import pytest
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from teams.models import Equipe, MembroEquipe, PermissaoEquipe

User = get_user_model()


@pytest.mark.django_db
class TestFixtures:
    """Testes para validar as fixtures definidas em conftest.py."""
    
    def test_api_client_fixture(self, api_client):
        """Testa fixture api_client."""
        assert isinstance(api_client, APIClient)
        assert api_client._credentials == {}
    
    def test_user_fixtures(self, user1, user2, user3):
        """Testa fixtures de usuários."""
        # Verifica user1
        assert user1.username == 'user1'
        assert user1.email == 'user1@example.com'
        assert user1.full_name == 'User One'
        assert user1.check_password('testpass123')
        
        # Verifica user2
        assert user2.username == 'user2'
        assert user2.email == 'user2@example.com'
        assert user2.full_name == 'User Two'
        
        # Verifica user3
        assert user3.username == 'user3'
        assert user3.email == 'user3@example.com'
        assert user3.full_name == 'User Three'
        
        # Verifica que são objetos diferentes
        assert user1.id != user2.id != user3.id
    
    def test_authenticated_client_fixture(self, authenticated_client, user1):
        """Testa fixture authenticated_client."""
        assert isinstance(authenticated_client, APIClient)
        
        # Verifica que está autenticado com user1
        # O force_authenticate define o user mas não cria session/token
        assert authenticated_client.handler._force_user == user1
    
    def test_equipe_fixtures(self, equipe1, equipe2, user1, user2):
        """Testa fixtures de equipes."""
        # Verifica equipe1
        assert equipe1.nome == "Equipe 1"
        assert equipe1.descricao == "Primeira equipe de teste"
        assert equipe1.criado_por == user1
        
        # Verifica equipe2
        assert equipe2.nome == "Equipe 2"
        assert equipe2.descricao == "Segunda equipe de teste"
        assert equipe2.criado_por == user2
        
        # Verifica que são objetos diferentes
        assert equipe1.id != equipe2.id
    
    def test_equipe_teste_fixture(self, equipe_teste, user1):
        """Testa fixture equipe_teste."""
        assert equipe_teste.nome == "Equipe Teste"
        assert equipe_teste.criado_por == user1
        assert equipe_teste.descricao is None  # Não foi definida
    
    def test_membro_equipe_fixtures(self, membro_equipe_user1, membro_equipe_user2, equipe_teste, user1, user2):
        """Testa fixtures de membros de equipe."""
        # Verifica membro_equipe_user1
        assert membro_equipe_user1.equipe == equipe_teste
        assert membro_equipe_user1.usuario == user1
        assert membro_equipe_user1.papel == 'PO'
        assert membro_equipe_user1.adicionado_por == user1
        
        # Verifica membro_equipe_user2
        assert membro_equipe_user2.equipe == equipe_teste
        assert membro_equipe_user2.usuario == user2
        assert membro_equipe_user2.papel == 'DEV'
        assert membro_equipe_user2.adicionado_por == user1
        
        # Verifica que são objetos diferentes
        assert membro_equipe_user1.id != membro_equipe_user2.id
    
    def test_permissao_equipe_fixture(self, permissao_equipe, equipe_teste):
        """Testa fixture permissao_equipe."""
        assert permissao_equipe.papel == 'DEV'
        assert permissao_equipe.equipe == equipe_teste
        assert permissao_equipe.modulo == 'TAREFAS'
        assert permissao_equipe.permissao == 'CRIAR'


@pytest.mark.django_db
class TestFixturesDependencies:
    """Testa dependências entre fixtures."""
    
    def test_authenticated_client_depende_user1(self, authenticated_client, user1):
        """Testa que authenticated_client depende corretamente de user1."""
        # Quando user1 é usado com authenticated_client, deve estar autenticado
        assert authenticated_client.handler._force_user == user1
    
    def test_equipe_teste_com_membros(self, equipe_teste, membro_equipe_user1, membro_equipe_user2):
        """Testa que equipe_teste funciona com seus membros."""
        membros = MembroEquipe.objects.filter(equipe=equipe_teste)
        assert membros.count() == 2
        
        membros_usuarios = [m.usuario for m in membros]
        assert membro_equipe_user1.usuario in membros_usuarios
        assert membro_equipe_user2.usuario in membros_usuarios
    
    def test_permissao_equipe_depende_equipe_teste(self, permissao_equipe, equipe_teste):
        """Testa que permissao_equipe depende corretamente de equipe_teste."""
        assert permissao_equipe.equipe == equipe_teste
        
        permissoes = PermissaoEquipe.objects.filter(equipe=equipe_teste)
        assert permissoes.count() == 1
        assert permissao_equipe in permissoes


@pytest.mark.django_db
class TestFixturesIsolation:
    """Testa isolamento entre fixtures."""
    
    def test_fixtures_nao_interferem_entre_testes(self, user1, equipe1):
        """Testa que fixtures são isoladas entre testes."""
        # Modifica dados
        user1.full_name = "Nome Modificado"
        user1.save()
        
        equipe1.nome = "Nome Modificado"
        equipe1.save()
        
        # Em outro teste, as fixtures devem ter valores originais
        # (este teste garante que não há vazamento entre testes)
        assert True  # Se chegou aqui, as fixtures foram criadas corretamente
    
    def test_fixtures_nao_interferem_entre_testes_2(self, user1, equipe1):
        """Segundo teste para verificar isolamento."""
        # Valores devem estar como originalmente definidos nas fixtures
        assert user1.full_name == "User One"
        assert equipe1.nome == "Equipe 1"


@pytest.mark.django_db
class TestFixturesUsagePatterns:
    """Testa padrões de uso das fixtures."""
    
    def test_uso_multiplas_fixtures_usuarios(self, user1, user2, user3):
        """Testa uso de múltiplas fixtures de usuários."""
        usuarios = [user1, user2, user3]
        
        # Todos devem ser únicos
        user_ids = [u.id for u in usuarios]
        assert len(set(user_ids)) == 3
        
        # Todos devem estar no banco
        assert User.objects.filter(id__in=user_ids).count() == 3
    
    def test_uso_multiplas_fixtures_equipes(self, equipe1, equipe2, equipe_teste):
        """Testa uso de múltiplas fixtures de equipes."""
        equipes = [equipe1, equipe2, equipe_teste]
        
        # Todas devem ser únicas
        equipe_ids = [e.id for e in equipes]
        assert len(set(equipe_ids)) == 3
        
        # Todas devem estar no banco
        assert Equipe.objects.filter(id__in=equipe_ids).count() == 3
    
    def test_fixtures_combinadas_cenario_completo(self, 
                                                  authenticated_client, 
                                                  equipe_teste, 
                                                  membro_equipe_user1, 
                                                  membro_equipe_user2, 
                                                  permissao_equipe):
        """Testa cenário completo usando múltiplas fixtures."""
        # Cliente autenticado
        assert authenticated_client.handler._force_user is not None
        
        # Equipe com dados
        assert equipe_teste.nome == "Equipe Teste"
        
        # Membros da equipe
        membros = MembroEquipe.objects.filter(equipe=equipe_teste)
        assert membros.count() == 2
        
        # Permissões da equipe
        permissoes = PermissaoEquipe.objects.filter(equipe=equipe_teste)
        assert permissoes.count() == 1
        
        # Tudo integrado
        assert membro_equipe_user1 in membros
        assert membro_equipe_user2 in membros
        assert permissao_equipe in permissoes


@pytest.mark.django_db
class TestFixturesPerformance:
    """Testa performance das fixtures."""
    
    def test_fixtures_nao_criam_dados_desnecessarios(self, user1):
        """Testa que fixture só cria user1 quando solicitado."""
        # Só deve existir user1
        assert User.objects.count() == 1
        assert User.objects.first() == user1
    
    def test_fixtures_incrementais(self, user1, user2):
        """Testa que fixtures são criadas incrementalmente."""
        # Agora devem existir user1 e user2
        assert User.objects.count() == 2
        assert user1 in User.objects.all()
        assert user2 in User.objects.all()
    
    def test_fixtures_reutilizacao(self, user1, equipe1, equipe2):
        """Testa que user1 é reutilizado entre fixtures."""
        # user1 é usado por equipe1 e pode ser usado em outras fixtures
        assert equipe1.criado_por == user1
        # equipe2 usa user2, mas user1 ainda deve existir
        assert User.objects.filter(id=user1.id).exists()
        
        # Deve ter user1, user2 (de equipe2) 
        assert User.objects.count() == 2
