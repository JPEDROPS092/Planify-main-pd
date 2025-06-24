"""
Testes para os modelos do módulo Teams.
"""
import pytest
from django.core.exceptions import ValidationError
from django.db import IntegrityError
from django.test import TestCase
from django.contrib.auth import get_user_model
from teams.models import Equipe, MembroEquipe, PermissaoEquipe

User = get_user_model()  # type: ignore


class EquipeModelTest(TestCase):
    """Testes para o modelo Equipe"""
    
    def setUp(self):
        """Configuração inicial para os testes"""
        self.user = User.objects.create_user(  # type: ignore
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        
    def test_create_equipe(self):
        """Testa a criação de uma equipe"""
        equipe = Equipe.objects.create(
            nome="Equipe de Desenvolvimento",
            descricao="Equipe responsável pelo desenvolvimento do sistema",
            criado_por=self.user
        )
        
        self.assertEqual(equipe.nome, "Equipe de Desenvolvimento")
        self.assertEqual(equipe.descricao, "Equipe responsável pelo desenvolvimento do sistema")
        self.assertEqual(equipe.criado_por, self.user)
        self.assertTrue(equipe.criado_em)
        self.assertTrue(equipe.atualizado_em)
        
    def test_equipe_str_representation(self):
        """Testa a representação string da equipe"""
        equipe = Equipe.objects.create(
            nome="Equipe de Testes",
            criado_por=self.user
        )
        self.assertEqual(str(equipe), "Equipe de Testes")
        
    def test_equipe_nome_max_length(self):
        """Testa o comprimento máximo do nome da equipe"""
        long_name = 'A' * 256  # Mais que o máximo permitido (200)
        with self.assertRaises(ValidationError):
            equipe = Equipe(
                nome=long_name,
                criado_por=self.user
            )
            equipe.full_clean()
            
    def test_equipe_nome_required(self):
        """Testa que o nome da equipe é obrigatório"""
        with self.assertRaises(ValidationError):
            equipe = Equipe(
                nome="",
                criado_por=self.user
            )
            equipe.full_clean()
            
    def test_equipe_criado_por_required(self):
        """Testa que criado_por é obrigatório"""
        with self.assertRaises(IntegrityError):
            Equipe.objects.create(
                nome="Equipe Teste",
                criado_por=None
            )


class MembroEquipeModelTest(TestCase):
    """Testes para o modelo MembroEquipe"""
    
    def setUp(self):
        """Configuração inicial para os testes"""
        self.user1 = User.objects.create_user(  # type: ignore
            username='user1',
            email='user1@example.com',
            password='testpass123'
        )
        self.user2 = User.objects.create_user(  # type: ignore
            username='user2',
            email='user2@example.com',
            password='testpass123'
        )
        self.equipe = Equipe.objects.create(
            nome="Equipe Teste",
            criado_por=self.user1
        )
        
    def test_create_membro_equipe(self):
        """Testa a criação de um membro de equipe"""
        membro = MembroEquipe.objects.create(
            equipe=self.equipe,
            usuario=self.user2,
            papel='DEV',
            adicionado_por=self.user1
        )
        
        self.assertEqual(membro.equipe, self.equipe)
        self.assertEqual(membro.usuario, self.user2)
        self.assertEqual(membro.papel, 'DEV')
        self.assertEqual(membro.adicionado_por, self.user1)
        self.assertTrue(membro.adicionado_em)
        
    def test_membro_equipe_str_representation(self):
        """Testa a representação string do membro de equipe"""
        membro = MembroEquipe.objects.create(
            equipe=self.equipe,
            usuario=self.user2,
            papel='DEV',
            adicionado_por=self.user1
        )
        expected = f"{self.user2.full_name} - {self.equipe.nome} (DEV)"
        self.assertEqual(str(membro), expected)
        
    def test_get_papel_display(self):
        """Testa o método get_papel_display"""
        membro = MembroEquipe.objects.create(
            equipe=self.equipe,
            usuario=self.user2,
            papel='PO',
            adicionado_por=self.user1
        )
        self.assertEqual(membro.get_papel_display(), 'Product Owner')
        
    def test_unique_constraint_usuario_equipe(self):
        """Testa que um usuário não pode ser adicionado duas vezes na mesma equipe"""
        MembroEquipe.objects.create(
            equipe=self.equipe,
            usuario=self.user2,
            papel='DEV',
            adicionado_por=self.user1
        )
        
        with self.assertRaises(IntegrityError):
            MembroEquipe.objects.create(
                equipe=self.equipe,
                usuario=self.user2,
                papel='PO',
                adicionado_por=self.user1
            )
            
    def test_papel_choices(self):
        """Testa as opções de papel disponíveis"""
        papeis_validos = ['PO', 'SM', 'DEV', 'QA', 'DESIGN', 'STAKEHOLDER']
        
        for papel in papeis_validos:
            membro = MembroEquipe(
                equipe=self.equipe,
                usuario=self.user2,
                papel=papel,
                adicionado_por=self.user1
            )
            # Não deve levantar exceção
            membro.full_clean()
            
    def test_papel_invalid_choice(self):
        """Testa papel inválido"""
        with self.assertRaises(ValidationError):
            membro = MembroEquipe(
                equipe=self.equipe,
                usuario=self.user2,
                papel='INVALID',
                adicionado_por=self.user1
            )
            membro.full_clean()


class PermissaoEquipeModelTest(TestCase):
    """Testes para o modelo PermissaoEquipe"""
    
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
        
    def test_create_permissao_equipe(self):
        """Testa a criação de uma permissão de equipe"""
        permissao = PermissaoEquipe.objects.create(
            papel='DEV',
            equipe=self.equipe,
            modulo='TASKS',
            permissao='CREATE'
        )
        
        self.assertEqual(permissao.papel, 'DEV')
        self.assertEqual(permissao.equipe, self.equipe)
        self.assertEqual(permissao.modulo, 'TASKS')
        self.assertEqual(permissao.permissao, 'CREATE')
        
    def test_permissao_equipe_str_representation(self):
        """Testa a representação string da permissão de equipe"""
        permissao = PermissaoEquipe.objects.create(
            papel='DEV',
            equipe=self.equipe,
            modulo='TASKS',
            permissao='CREATE'
        )
        expected = f"{self.equipe.nome} - DEV - TASKS - CREATE"
        self.assertEqual(str(permissao), expected)
        
    def test_get_display_methods(self):
        """Testa os métodos get_display"""
        permissao = PermissaoEquipe.objects.create(
            papel='PO',
            equipe=self.equipe,
            modulo='PROJECTS',
            permissao='READ'
        )
        
        self.assertEqual(permissao.get_papel_display(), 'Product Owner')
        self.assertEqual(permissao.get_modulo_display(), 'Projetos')
        self.assertEqual(permissao.get_permissao_display(), 'Visualizar')
        
    def test_unique_constraint_papel_equipe_modulo_permissao(self):
        """Testa que não pode haver permissões duplicadas"""
        PermissaoEquipe.objects.create(
            papel='DEV',
            equipe=self.equipe,
            modulo='TASKS',
            permissao='CREATE'
        )
        
        with self.assertRaises(IntegrityError):
            PermissaoEquipe.objects.create(
                papel='DEV',
                equipe=self.equipe,
                modulo='TASKS',
                permissao='CREATE'
            )
            
    def test_papel_choices(self):
        """Testa as opções de papel disponíveis"""
        papeis_validos = ['PO', 'SM', 'DEV', 'QA', 'DESIGN', 'STAKEHOLDER']
        
        for papel in papeis_validos:
            permissao = PermissaoEquipe(
                papel=papel,
                equipe=self.equipe,
                modulo='TASKS',
                permissao='READ'
            )
            # Não deve levantar exceção
            permissao.full_clean()
            
    def test_modulo_choices(self):
        """Testa as opções de módulo disponíveis"""
        modulos_validos = ['PROJECTS', 'TASKS', 'RISKS', 'COSTS', 'DOCUMENTS', 'COMMUNICATIONS']
        
        for modulo in modulos_validos:
            permissao = PermissaoEquipe(
                papel='DEV',
                equipe=self.equipe,
                modulo=modulo,
                permissao='READ'
            )
            # Não deve levantar exceção
            permissao.full_clean()
            
    def test_permissao_choices(self):
        """Testa as opções de permissão disponíveis"""
        permissoes_validas = ['CREATE', 'READ', 'UPDATE', 'DELETE']
        
        for perm in permissoes_validas:
            permissao = PermissaoEquipe(
                papel='DEV',
                equipe=self.equipe,
                modulo='TASKS',
                permissao=perm
            )
            # Não deve levantar exceção
            permissao.full_clean()


class EquipeRelationshipsTest(TestCase):
    """Testes para relacionamentos entre modelos"""
    
    def setUp(self):
        """Configuração inicial para os testes"""
        self.user1 = User.objects.create_user(  # type: ignore
            username='user1',
            email='user1@example.com',
            password='testpass123'
        )
        self.user2 = User.objects.create_user(  # type: ignore
            username='user2',
            email='user2@example.com',
            password='testpass123'
        )
        self.equipe = Equipe.objects.create(
            nome="Equipe Teste",
            criado_por=self.user1
        )
        
    def test_equipe_membros_relationship(self):
        """Testa o relacionamento entre equipe e membros"""
        membro1 = MembroEquipe.objects.create(
            equipe=self.equipe,
            usuario=self.user1,
            papel='PO',
            adicionado_por=self.user1
        )
        membro2 = MembroEquipe.objects.create(
            equipe=self.equipe,
            usuario=self.user2,
            papel='DEV',
            adicionado_por=self.user1
        )
        
        membros = self.equipe.membros.all()  # type: ignore
        self.assertEqual(membros.count(), 2)
        self.assertIn(membro1, membros)
        self.assertIn(membro2, membros)
        
    def test_equipe_permissoes_relationship(self):
        """Testa o relacionamento entre equipe e permissões"""
        permissao1 = PermissaoEquipe.objects.create(
            papel='DEV',
            equipe=self.equipe,
            modulo='TASKS',
            permissao='CREATE'
        )
        permissao2 = PermissaoEquipe.objects.create(
            papel='PO',
            equipe=self.equipe,
            modulo='PROJECTS',
            permissao='UPDATE'
        )
        
        permissoes = self.equipe.permissoes.all()  # type: ignore
        self.assertEqual(permissoes.count(), 2)
        self.assertIn(permissao1, permissoes)
        self.assertIn(permissao2, permissoes)
        
    def test_delete_equipe_cascade(self):
        """Testa que ao deletar equipe, membros e permissões são deletados"""
        MembroEquipe.objects.create(
            equipe=self.equipe,
            usuario=self.user2,
            papel='DEV',
            adicionado_por=self.user1
        )
        PermissaoEquipe.objects.create(
            papel='DEV',
            equipe=self.equipe,
            modulo='TASKS',
            permissao='CREATE'
        )
        
        equipe_id = self.equipe.id  # type: ignore
        self.equipe.delete()
        
        # Verifica que membros e permissões foram deletados
        self.assertEqual(MembroEquipe.objects.filter(equipe_id=equipe_id).count(), 0)
        self.assertEqual(PermissaoEquipe.objects.filter(equipe_id=equipe_id).count(), 0)
