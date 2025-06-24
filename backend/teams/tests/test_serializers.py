"""
Testes para os serializers do módulo Teams.
"""
import pytest
from django.contrib.auth import get_user_model
from teams.models import Equipe, MembroEquipe, PermissaoEquipe
from teams.serializers import (
    EquipeSerializer, EquipeListSerializer, MembroEquipeSerializer, 
    PermissaoEquipeSerializer, UserMinimalSerializer
)

User = get_user_model()


@pytest.mark.django_db
class TestPermissaoEquipeSerializer:
    """Testes para PermissaoEquipeSerializer."""
    
    def test_serialization(self, permissao_equipe):
        """Testa serialização de permissão de equipe."""
        serializer = PermissaoEquipeSerializer(permissao_equipe)
        data = serializer.data
        
        assert data['papel'] == 'DEV'
        assert data['papel_display'] == 'Desenvolvedor'
        assert data['modulo'] == 'TAREFAS'
        assert data['modulo_display'] == 'Tarefas'
        assert data['permissao'] == 'CRIAR'
        assert data['permissao_display'] == 'Criar'
        assert data['equipe'] == permissao_equipe.equipe.id
    
    def test_deserialization(self, equipe1):
        """Testa deserialização de permissão de equipe."""
        data = {
            'papel': 'QA',
            'equipe': equipe1.id,
            'modulo': 'DOCUMENTOS',
            'permissao': 'VISUALIZAR'
        }
        
        serializer = PermissaoEquipeSerializer(data=data)
        assert serializer.is_valid()
        
        permissao = serializer.save()
        assert permissao.papel == 'QA'
        assert permissao.equipe == equipe1
        assert permissao.modulo == 'DOCUMENTOS'
        assert permissao.permissao == 'VISUALIZAR'
    
    def test_validation_papel_invalido(self, equipe1):
        """Testa validação com papel inválido."""
        data = {
            'papel': 'INVALID',
            'equipe': equipe1.id,
            'modulo': 'TAREFAS',
            'permissao': 'CRIAR'
        }
        
        serializer = PermissaoEquipeSerializer(data=data)
        assert not serializer.is_valid()
        assert 'papel' in serializer.errors


@pytest.mark.django_db
class TestMembroEquipeSerializer:
    """Testes para MembroEquipeSerializer."""
    
    def test_serialization(self, membro_equipe_user1):
        """Testa serialização de membro de equipe."""
        serializer = MembroEquipeSerializer(membro_equipe_user1)
        data = serializer.data
        
        assert data['usuario'] == membro_equipe_user1.usuario.id
        assert data['usuario_nome'] == membro_equipe_user1.usuario.full_name
        assert data['usuario_email'] == membro_equipe_user1.usuario.email
        assert data['papel'] == 'PO'
        assert data['papel_display'] == 'Product Owner'
        assert data['equipe'] == membro_equipe_user1.equipe.id
        assert 'adicionado_em' in data
    
    def test_serialization_com_adicionado_por(self, membro_equipe_user2):
        """Testa serialização com campo adicionado_por preenchido."""
        serializer = MembroEquipeSerializer(membro_equipe_user2)
        data = serializer.data
        
        assert data['adicionado_por'] == membro_equipe_user2.adicionado_por.id
        assert data['adicionado_por_nome'] == membro_equipe_user2.adicionado_por.full_name
    
    def test_deserialization(self, equipe1, user1):
        """Testa deserialização de membro de equipe."""
        data = {
            'equipe': equipe1.id,
            'usuario': user1.id,
            'papel': 'SM'
        }
        
        serializer = MembroEquipeSerializer(data=data)
        assert serializer.is_valid()
        
        membro = serializer.save()
        assert membro.equipe == equipe1
        assert membro.usuario == user1
        assert membro.papel == 'SM'
    
    def test_validation_papel_obrigatorio(self, equipe1, user1):
        """Testa validação com papel obrigatório."""
        data = {
            'equipe': equipe1.id,
            'usuario': user1.id
        }
        
        serializer = MembroEquipeSerializer(data=data)
        assert not serializer.is_valid()
        assert 'papel' in serializer.errors


@pytest.mark.django_db
class TestEquipeSerializer:
    """Testes para EquipeSerializer."""
    
    def test_serialization_equipe_completa(self, equipe_teste, membro_equipe_user1, membro_equipe_user2, permissao_equipe):
        """Testa serialização de equipe com membros e permissões."""
        serializer = EquipeSerializer(equipe_teste)
        data = serializer.data
        
        assert data['nome'] == equipe_teste.nome
        assert data['criado_por'] == equipe_teste.criado_por.id
        assert data['criado_por_nome'] == equipe_teste.criado_por.full_name
        assert len(data['membros']) == 2
        assert len(data['permissoes']) == 1
        assert data['total_membros'] == 2
        assert 'criado_em' in data
        assert 'atualizado_em' in data
    
    def test_serialization_equipe_vazia(self, equipe1):
        """Testa serialização de equipe sem membros nem permissões."""
        serializer = EquipeSerializer(equipe1)
        data = serializer.data
        
        assert data['nome'] == equipe1.nome
        assert data['descricao'] == equipe1.descricao
        assert len(data['membros']) == 0
        assert len(data['permissoes']) == 0
        assert data['total_membros'] == 0
    
    def test_deserialization_criacao(self, user1):
        """Testa deserialização para criação de equipe."""
        data = {
            'nome': 'Nova Equipe',
            'descricao': 'Descrição da nova equipe',
            'criado_por': user1.id
        }
        
        serializer = EquipeSerializer(data=data)
        assert serializer.is_valid()
        
        equipe = serializer.save()
        assert equipe.nome == 'Nova Equipe'
        assert equipe.descricao == 'Descrição da nova equipe'
        assert equipe.criado_por == user1
    
    def test_deserialization_atualizacao(self, equipe1):
        """Testa deserialização para atualização de equipe."""
        data = {
            'nome': 'Nome Atualizado',
            'descricao': 'Descrição atualizada'
        }
        
        serializer = EquipeSerializer(equipe1, data=data, partial=True)
        assert serializer.is_valid()
        
        equipe_atualizada = serializer.save()
        assert equipe_atualizada.nome == 'Nome Atualizado'
        assert equipe_atualizada.descricao == 'Descrição atualizada'
    
    def test_validation_nome_obrigatorio(self):
        """Testa validação com nome obrigatório."""
        data = {
            'descricao': 'Equipe sem nome'
        }
        
        serializer = EquipeSerializer(data=data)
        assert not serializer.is_valid()
        assert 'nome' in serializer.errors
    
    def test_validation_nome_max_length(self, user1):
        """Testa validação de tamanho máximo do nome."""
        data = {
            'nome': 'x' * 101,  # Excede o limite de 100 caracteres
            'criado_por': user1.id
        }
        
        serializer = EquipeSerializer(data=data)
        assert not serializer.is_valid()
        assert 'nome' in serializer.errors
    
    def test_campos_readonly(self, equipe1):
        """Testa que campos readonly não são alterados."""
        data = {
            'nome': 'Nome Novo',
            'criado_em': '2023-01-01T00:00:00Z',
            'atualizado_em': '2023-01-01T00:00:00Z'
        }
        
        serializer = EquipeSerializer(equipe1, data=data, partial=True)
        assert serializer.is_valid()
        
        equipe_original_criado_em = equipe1.criado_em
        equipe_original_atualizado_em = equipe1.atualizado_em
        
        equipe_atualizada = serializer.save()
        
        # Campos readonly não devem mudar
        assert equipe_atualizada.criado_em == equipe_original_criado_em
        # atualizado_em pode mudar automaticamente
        assert equipe_atualizada.nome == 'Nome Novo'


@pytest.mark.django_db
class TestEquipeListSerializer:
    """Testes para EquipeListSerializer."""
    
    def test_serialization_lista(self, equipe1, equipe2):
        """Testa serialização de lista de equipes."""
        equipes = [equipe1, equipe2]
        serializer = EquipeListSerializer(equipes, many=True)
        data = serializer.data
        
        assert len(data) == 2
        
        # Verifica primeiro item
        primeiro_item = data[0]
        assert primeiro_item['nome'] == equipe1.nome
        assert primeiro_item['criado_por_nome'] == equipe1.criado_por.full_name
        
        # EquipeListSerializer deve ter campos reduzidos comparado ao EquipeSerializer
        assert 'membros' not in primeiro_item  # Assumindo que não tem membros na lista
        assert 'permissoes' not in primeiro_item  # Assumindo que não tem permissões na lista


@pytest.mark.django_db
class TestUserMinimalSerializer:
    """Testes para UserMinimalSerializer."""
    
    def test_serialization(self, user1):
        """Testa serialização de usuário minimal."""
        serializer = UserMinimalSerializer(user1)
        data = serializer.data
        
        # Verifica campos básicos do usuário
        assert data['id'] == user1.id
        assert data['username'] == user1.username
        assert data['email'] == user1.email
        assert data['full_name'] == user1.full_name
    
    def test_serialization_lista_usuarios(self, user1, user2, user3):
        """Testa serialização de lista de usuários."""
        usuarios = [user1, user2, user3]
        serializer = UserMinimalSerializer(usuarios, many=True)
        data = serializer.data
        
        assert len(data) == 3
        assert all('id' in item for item in data)
        assert all('username' in item for item in data)


@pytest.mark.django_db
class TestSerializersIntegration:
    """Testes de integração entre serializers."""
    
    def test_equipe_com_membros_nested(self, equipe_teste, user1, user2):
        """Testa serialização de equipe com membros aninhados."""
        # Cria membros
        MembroEquipe.objects.create(equipe=equipe_teste, usuario=user1, papel='PO')
        MembroEquipe.objects.create(equipe=equipe_teste, usuario=user2, papel='DEV')
        
        serializer = EquipeSerializer(equipe_teste)
        data = serializer.data
        
        # Verifica dados dos membros aninhados
        membros = data['membros']
        assert len(membros) == 2
        
        # Verifica primeiro membro
        primeiro_membro = membros[0]
        assert 'usuario_nome' in primeiro_membro
        assert 'usuario_email' in primeiro_membro
        assert 'papel_display' in primeiro_membro
    
    def test_equipe_com_permissoes_nested(self, equipe_teste):
        """Testa serialização de equipe com permissões aninhadas."""
        # Cria permissões
        PermissaoEquipe.objects.create(
            papel='DEV', equipe=equipe_teste, modulo='TAREFAS', permissao='CRIAR'
        )
        PermissaoEquipe.objects.create(
            papel='QA', equipe=equipe_teste, modulo='DOCUMENTOS', permissao='VISUALIZAR'
        )
        
        serializer = EquipeSerializer(equipe_teste)
        data = serializer.data
        
        # Verifica dados das permissões aninhadas
        permissoes = data['permissoes']
        assert len(permissoes) == 2
        
        # Verifica primeira permissão
        primeira_permissao = permissoes[0]
        assert 'papel_display' in primeira_permissao
        assert 'modulo_display' in primeira_permissao
        assert 'permissao_display' in primeira_permissao
