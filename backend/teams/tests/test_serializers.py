"""
Testes para os serializers do módulo Teams.
"""
from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework.test import APIRequestFactory
from teams.models import Equipe, MembroEquipe, PermissaoEquipe
from teams.serializers import (
    EquipeSerializer, EquipeListSerializer, MembroEquipeSerializer,
    PermissaoEquipeSerializer, UserMinimalSerializer
)

User = get_user_model()  # type: ignore


class EquipeSerializerTest(TestCase):
    """Testes para o EquipeSerializer"""
    
    def setUp(self):
        """Configuração inicial para os testes"""
        self.user = User.objects.create_user(  # type: ignore
            username='testuser',
            email='test@example.com',
            password='testpass123',
            first_name='Test',
            last_name='User'
        )
        self.factory = APIRequestFactory()
        
    def test_serialize_equipe(self):
        """Testa a serialização de uma equipe"""
        equipe = Equipe.objects.create(
            nome="Equipe de Desenvolvimento",
            descricao="Equipe responsável pelo desenvolvimento",
            criado_por=self.user
        )
        
        serializer = EquipeSerializer(equipe)
        data = serializer.data
        
        self.assertEqual(data['nome'], "Equipe de Desenvolvimento")
        self.assertEqual(data['descricao'], "Equipe responsável pelo desenvolvimento")
        self.assertEqual(data['criado_por'], self.user.id)  # type: ignore
        self.assertEqual(data['criado_por_nome'], self.user.full_name)
        self.assertIn('total_membros', data)
        self.assertIn('membros', data)
        self.assertIn('permissoes', data)
        
    def test_create_equipe_with_serializer(self):
        """Testa a criação de equipe através do serializer"""
        request = self.factory.post('/')
        request.user = self.user
        
        data = {
            'nome': 'Nova Equipe',
            'descricao': 'Descrição da nova equipe'
        }
        
        serializer = EquipeSerializer(data=data, context={'request': request})
        self.assertTrue(serializer.is_valid())
        
        equipe = serializer.save(criado_por=self.user)
        self.assertEqual(equipe.nome, 'Nova Equipe')
        self.assertEqual(equipe.criado_por, self.user)
        
        # Verifica se o criador foi adicionado como membro PO
        membro = MembroEquipe.objects.filter(equipe=equipe, usuario=self.user).first()
        self.assertIsNotNone(membro)
        self.assertEqual(membro.papel, 'PO')  # type: ignore
        
    def test_get_total_membros(self):
        """Testa o campo total_membros"""
        equipe = Equipe.objects.create(
            nome="Equipe Teste",
            criado_por=self.user
        )
        
        # Adiciona alguns membros
        MembroEquipe.objects.create(
            equipe=equipe,
            usuario=self.user,
            papel='PO',
            adicionado_por=self.user
        )
        
        user2 = User.objects.create_user(  # type: ignore
            username='user2',
            email='user2@example.com',
            password='testpass123'
        )
        MembroEquipe.objects.create(
            equipe=equipe,
            usuario=user2,
            papel='DEV',
            adicionado_por=self.user
        )
        
        serializer = EquipeSerializer(equipe)
        self.assertEqual(serializer.data['total_membros'], 2)
        
    def test_read_only_fields(self):
        """Testa que campos read_only não podem ser alterados"""
        equipe = Equipe.objects.create(
            nome="Equipe Teste",
            criado_por=self.user
        )
        
        data = {
            'nome': 'Nome Atualizado',
            'criado_em': '2025-01-01T00:00:00Z',  # Tentativa de alterar campo read_only
            'atualizado_em': '2025-01-01T00:00:00Z'  # Tentativa de alterar campo read_only
        }
        
        serializer = EquipeSerializer(equipe, data=data, partial=True)
        self.assertTrue(serializer.is_valid())
        
        updated_equipe = serializer.save()
        self.assertEqual(updated_equipe.nome, 'Nome Atualizado')
        # criado_em e atualizado_em não devem ter sido alterados pelos dados fornecidos


class EquipeListSerializerTest(TestCase):
    """Testes para o EquipeListSerializer"""
    
    def setUp(self):
        """Configuração inicial para os testes"""
        self.user = User.objects.create_user(  # type: ignore
            username='testuser',
            email='test@example.com',
            password='testpass123',
            first_name='Test',
            last_name='User'
        )
        
    def test_serialize_equipe_list(self):
        """Testa a serialização simplificada para listagem"""
        equipe = Equipe.objects.create(
            nome="Equipe Teste",
            descricao="Uma descrição longa que não deve aparecer na listagem",
            criado_por=self.user
        )
        
        serializer = EquipeListSerializer(equipe)
        data = serializer.data
        
        expected_fields = ['id', 'nome', 'criado_por_nome', 'criado_em', 'total_membros']
        self.assertEqual(set(data.keys()), set(expected_fields))
        
        # Verifica que campos detalhados não estão presentes
        self.assertNotIn('descricao', data)
        self.assertNotIn('membros', data)
        self.assertNotIn('permissoes', data)


class MembroEquipeSerializerTest(TestCase):
    """Testes para o MembroEquipeSerializer"""
    
    def setUp(self):
        """Configuração inicial para os testes"""
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
        self.equipe = Equipe.objects.create(
            nome="Equipe Teste",
            criado_por=self.user1
        )
        
    def test_serialize_membro_equipe(self):
        """Testa a serialização de um membro de equipe"""
        membro = MembroEquipe.objects.create(
            equipe=self.equipe,
            usuario=self.user2,
            papel='DEV',
            adicionado_por=self.user1
        )
        
        serializer = MembroEquipeSerializer(membro)
        data = serializer.data
        
        self.assertEqual(data['usuario'], self.user2.id)  # type: ignore
        self.assertEqual(data['usuario_nome'], self.user2.full_name)
        self.assertEqual(data['usuario_email'], self.user2.email)
        self.assertEqual(data['papel'], 'DEV')
        self.assertEqual(data['papel_display'], 'Desenvolvedor')
        self.assertEqual(data['adicionado_por'], self.user1.id)  # type: ignore
        self.assertEqual(data['adicionado_por_nome'], self.user1.full_name)
        
    def test_create_membro_equipe_with_serializer(self):
        """Testa a criação de membro através do serializer"""
        data = {
            'usuario': self.user2.id,  # type: ignore
            'papel': 'QA'
        }
        
        serializer = MembroEquipeSerializer(data=data)
        self.assertTrue(serializer.is_valid())
        
        membro = serializer.save(equipe=self.equipe, adicionado_por=self.user1)
        self.assertEqual(membro.usuario, self.user2)
        self.assertEqual(membro.papel, 'QA')
        self.assertEqual(membro.equipe, self.equipe)
        self.assertEqual(membro.adicionado_por, self.user1)
        
    def test_read_only_fields(self):
        """Testa que adicionado_em é read_only"""
        membro = MembroEquipe.objects.create(
            equipe=self.equipe,
            usuario=self.user2,
            papel='DEV',
            adicionado_por=self.user1
        )
        
        data = {
            'papel': 'QA',
            'adicionado_em': '2025-01-01T00:00:00Z'  # Tentativa de alterar campo read_only
        }
        
        serializer = MembroEquipeSerializer(membro, data=data, partial=True)
        self.assertTrue(serializer.is_valid())
        
        updated_membro = serializer.save()
        self.assertEqual(updated_membro.papel, 'QA')
        # adicionado_em não deve ter sido alterado pelos dados fornecidos


class PermissaoEquipeSerializerTest(TestCase):
    """Testes para o PermissaoEquipeSerializer"""
    
    def setUp(self):
        """Configuração inicial para os testes"""
        self.user = User.objects.create_user(  # type: ignore
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        self.equipe = Equipe.objects.create(
            nome="Equipe Teste",
            criado_por=self.user
        )
        
    def test_serialize_permissao_equipe(self):
        """Testa a serialização de uma permissão de equipe"""
        permissao = PermissaoEquipe.objects.create(
            papel='DEV',
            equipe=self.equipe,
            modulo='TASKS',
            permissao='CREATE'
        )
        
        serializer = PermissaoEquipeSerializer(permissao)
        data = serializer.data
        
        self.assertEqual(data['papel'], 'DEV')
        self.assertEqual(data['papel_display'], 'Desenvolvedor')
        self.assertEqual(data['modulo'], 'TASKS')
        self.assertEqual(data['modulo_display'], 'Tarefas')
        self.assertEqual(data['permissao'], 'CREATE')
        self.assertEqual(data['permissao_display'], 'Criar')
        self.assertEqual(data['equipe'], self.equipe.id)  # type: ignore
        
    def test_create_permissao_equipe_with_serializer(self):
        """Testa a criação de permissão através do serializer"""
        data = {
            'papel': 'PO',
            'equipe': self.equipe.id,  # type: ignore
            'modulo': 'PROJECTS',
            'permissao': 'UPDATE'
        }
        
        serializer = PermissaoEquipeSerializer(data=data)
        self.assertTrue(serializer.is_valid())
        
        permissao = serializer.save()
        self.assertEqual(permissao.papel, 'PO')
        self.assertEqual(permissao.equipe, self.equipe)
        self.assertEqual(permissao.modulo, 'PROJECTS')
        self.assertEqual(permissao.permissao, 'UPDATE')


class UserMinimalSerializerTest(TestCase):
    """Testes para o UserMinimalSerializer"""
    
    def setUp(self):
        """Configuração inicial para os testes"""
        self.user = User.objects.create_user(  # type: ignore
            username='testuser',
            email='test@example.com',
            password='testpass123',
            first_name='Test',
            last_name='User'
        )
        
    def test_serialize_user_minimal(self):
        """Testa a serialização mínima de usuário"""
        serializer = UserMinimalSerializer(self.user)
        data = serializer.data
        
        expected_fields = ['id', 'username', 'full_name', 'email']
        self.assertEqual(set(data.keys()), set(expected_fields))
        
        self.assertEqual(data['username'], 'testuser')
        self.assertEqual(data['email'], 'test@example.com')
        self.assertEqual(data['full_name'], 'Test User')
        
    def test_minimal_fields_only(self):
        """Testa que apenas campos essenciais são incluídos"""
        serializer = UserMinimalSerializer(self.user)
        data = serializer.data
        
        # Verifica que campos sensíveis não estão presentes
        self.assertNotIn('password', data)
        self.assertNotIn('is_staff', data)
        self.assertNotIn('is_superuser', data)
        self.assertNotIn('last_login', data)


class SerializerContextTest(TestCase):
    """Testes relacionados ao contexto dos serializers"""
    
    def setUp(self):
        """Configuração inicial para os testes"""
        self.user = User.objects.create_user(  # type: ignore
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        self.factory = APIRequestFactory()
        
    def test_equipe_serializer_with_request_context(self):
        """Testa o EquipeSerializer com contexto de request"""
        request = self.factory.post('/')
        request.user = self.user
        
        data = {
            'nome': 'Equipe com Contexto',
            'descricao': 'Teste de contexto'
        }
        
        serializer = EquipeSerializer(data=data, context={'request': request})
        self.assertTrue(serializer.is_valid())
        
        equipe = serializer.save(criado_por=self.user)
        
        # Verifica que o membro foi criado automaticamente
        self.assertTrue(
            MembroEquipe.objects.filter(
                equipe=equipe,
                usuario=self.user,
                papel='PO'
            ).exists()
        )
        
    def test_equipe_serializer_without_request_context(self):
        """Testa o EquipeSerializer sem contexto de request"""
        data = {
            'nome': 'Equipe sem Contexto',
            'descricao': 'Teste sem contexto'
        }
        
        serializer = EquipeSerializer(data=data)
        self.assertTrue(serializer.is_valid())
        
        equipe = serializer.save(criado_por=self.user)
        
        # Verifica que nenhum membro foi criado automaticamente
        self.assertFalse(
            MembroEquipe.objects.filter(equipe=equipe).exists()
        )
