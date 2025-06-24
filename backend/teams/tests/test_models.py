"""
Testes para os modelos do módulo Teams.
"""
import pytest
from django.db import IntegrityError
from django.contrib.auth import get_user_model
from teams.models import Equipe, MembroEquipe, PermissaoEquipe

User = get_user_model()


@pytest.mark.django_db
class TestEquipeModel:
    """Testes para o modelo Equipe."""
    
    def test_criacao_equipe_valida(self, user1):
        """Testa criação de equipe com dados válidos."""
        equipe = Equipe.objects.create(
            nome="Equipe Teste",
            descricao="Descrição da equipe teste",
            criado_por=user1
        )
        
        assert equipe.nome == "Equipe Teste"
        assert equipe.descricao == "Descrição da equipe teste"
        assert equipe.criado_por == user1
        assert equipe.criado_em is not None
        assert equipe.atualizado_em is not None
    
    def test_str_equipe(self, equipe1):
        """Testa representação string da equipe."""
        assert str(equipe1) == "Equipe 1"
    
    def test_criacao_equipe_sem_descricao(self, user1):
        """Testa criação de equipe sem descrição."""
        equipe = Equipe.objects.create(
            nome="Equipe Sem Descrição",
            criado_por=user1
        )
        
        assert equipe.nome == "Equipe Sem Descrição"
        assert equipe.descricao is None
        assert equipe.criado_por == user1
    
    def test_criacao_equipe_sem_criador(self):
        """Testa criação de equipe sem criador."""
        equipe = Equipe.objects.create(
            nome="Equipe Órfã",
            descricao="Equipe sem criador"
        )
        
        assert equipe.nome == "Equipe Órfã"
        assert equipe.criado_por is None
    
    def test_relacionamento_membros(self, equipe1, user1, user2):
        """Testa relacionamento com membros."""
        membro1 = MembroEquipe.objects.create(
            equipe=equipe1,
            usuario=user1,
            papel='PO'
        )
        membro2 = MembroEquipe.objects.create(
            equipe=equipe1,
            usuario=user2,
            papel='DEV'
        )
        
        assert equipe1.membros.count() == 2
        assert membro1 in equipe1.membros.all()
        assert membro2 in equipe1.membros.all()
    
    def test_relacionamento_permissoes(self, equipe1):
        """Testa relacionamento com permissões."""
        permissao = PermissaoEquipe.objects.create(
            papel='DEV',
            equipe=equipe1,
            modulo='TAREFAS',
            permissao='CRIAR'
        )
        
        assert equipe1.permissoes.count() == 1
        assert permissao in equipe1.permissoes.all()


@pytest.mark.django_db
class TestMembroEquipeModel:
    """Testes para o modelo MembroEquipe."""
    
    def test_criacao_membro_equipe_valido(self, equipe1, user1, user2):
        """Testa criação de membro de equipe com dados válidos."""
        membro = MembroEquipe.objects.create(
            equipe=equipe1,
            usuario=user1,
            papel='PO',
            adicionado_por=user2
        )
        
        assert membro.equipe == equipe1
        assert membro.usuario == user1
        assert membro.papel == 'PO'
        assert membro.adicionado_por == user2
        assert membro.adicionado_em is not None
    
    def test_str_membro_equipe(self, membro_equipe_user1):
        """Testa representação string do membro de equipe."""
        expected = f"{membro_equipe_user1.usuario.username} - {membro_equipe_user1.equipe.nome} (Product Owner)"
        assert str(membro_equipe_user1) == expected
    
    def test_get_papel_display(self, membro_equipe_user1):
        """Testa método get_papel_display."""
        assert membro_equipe_user1.get_papel_display() == 'Product Owner'
        
        # Testa com papel DEV
        membro_equipe_user1.papel = 'DEV'
        assert membro_equipe_user1.get_papel_display() == 'Desenvolvedor'
    
    def test_unique_together_constraint(self, equipe1, user1):
        """Testa constraint unique_together para equipe e usuário."""
        # Cria primeiro membro
        MembroEquipe.objects.create(
            equipe=equipe1,
            usuario=user1,
            papel='PO'
        )
        
        # Tenta criar segundo membro com mesmo usuário e equipe
        with pytest.raises(IntegrityError):
            MembroEquipe.objects.create(
                equipe=equipe1,
                usuario=user1,
                papel='DEV'
            )
    
    def test_primeiro_membro_automatico_po(self, equipe1, user1):
        """Testa que primeiro membro sem papel definido vira PO automaticamente."""
        membro = MembroEquipe.objects.create(
            equipe=equipe1,
            usuario=user1
        )
        
        assert membro.papel == 'PO'
    
    def test_segundo_membro_nao_muda_papel(self, equipe1, user1, user2):
        """Testa que segundo membro deve especificar papel explicitamente."""
        # Primeiro membro
        MembroEquipe.objects.create(
            equipe=equipe1,
            usuario=user1,
            papel='PO'
        )
        
        # Segundo membro precisa especificar papel explicitamente
        # (não há lógica automática para segundo membro)
        membro2 = MembroEquipe.objects.create(
            equipe=equipe1,
            usuario=user2,
            papel='DEV'  # Precisa especificar explicitamente
        )
        
        # Verifica que foi criado com o papel especificado
        assert membro2.papel == 'DEV'
    
    def test_papeis_disponiveis(self):
        """Testa se todos os papéis esperados estão disponíveis."""
        papeis_esperados = ['PO', 'SM', 'DEV', 'QA', 'DESIGN', 'ANALISTA']
        papeis_modelo = [choice[0] for choice in MembroEquipe.PAPEL_CHOICES]
        
        for papel in papeis_esperados:
            assert papel in papeis_modelo
    
    def test_relacionamento_usuario_equipes(self, user1, equipe1, equipe2):
        """Testa relacionamento reverso usuario.equipes."""
        MembroEquipe.objects.create(equipe=equipe1, usuario=user1, papel='PO')
        MembroEquipe.objects.create(equipe=equipe2, usuario=user1, papel='DEV')
        
        assert user1.equipes.count() == 2


@pytest.mark.django_db
class TestPermissaoEquipeModel:
    """Testes para o modelo PermissaoEquipe."""
    
    def test_criacao_permissao_valida(self, equipe1):
        """Testa criação de permissão com dados válidos."""
        permissao = PermissaoEquipe.objects.create(
            papel='DEV',
            equipe=equipe1,
            modulo='TAREFAS',
            permissao='CRIAR'
        )
        
        assert permissao.papel == 'DEV'
        assert permissao.equipe == equipe1
        assert permissao.modulo == 'TAREFAS'
        assert permissao.permissao == 'CRIAR'
    
    def test_str_permissao_equipe(self, permissao_equipe):
        """Testa representação string da permissão."""
        expected = f"{permissao_equipe.equipe.nome} - Desenvolvedor - Tarefas - Criar"
        assert str(permissao_equipe) == expected
    
    def test_get_papel_display(self, permissao_equipe):
        """Testa método get_papel_display."""
        assert permissao_equipe.get_papel_display() == 'Desenvolvedor'
    
    def test_get_modulo_display(self, permissao_equipe):
        """Testa método get_modulo_display."""
        assert permissao_equipe.get_modulo_display() == 'Tarefas'
    
    def test_unique_together_constraint(self, equipe1):
        """Testa constraint unique_together."""
        # Cria primeira permissão
        PermissaoEquipe.objects.create(
            papel='DEV',
            equipe=equipe1,
            modulo='TAREFAS',
            permissao='CRIAR'
        )
        
        # Tenta criar permissão duplicada
        with pytest.raises(IntegrityError):
            PermissaoEquipe.objects.create(
                papel='DEV',
                equipe=equipe1,
                modulo='TAREFAS',
                permissao='CRIAR'
            )
    
    def test_multiplas_permissoes_mesmo_papel(self, equipe1):
        """Testa múltiplas permissões para mesmo papel."""
        PermissaoEquipe.objects.create(
            papel='DEV',
            equipe=equipe1,
            modulo='TAREFAS',
            permissao='CRIAR'
        )
        
        PermissaoEquipe.objects.create(
            papel='DEV',
            equipe=equipe1,
            modulo='TAREFAS',
            permissao='EDITAR'
        )
        
        assert PermissaoEquipe.objects.filter(papel='DEV', equipe=equipe1).count() == 2
    
    def test_permissoes_disponiveis(self):
        """Testa se todas as permissões esperadas estão disponíveis."""
        permissoes_esperadas = ['VISUALIZAR', 'CRIAR', 'EDITAR', 'EXCLUIR']
        permissoes_modelo = [choice[0] for choice in PermissaoEquipe.PERMISSAO_CHOICES]
        
        for permissao in permissoes_esperadas:
            assert permissao in permissoes_modelo
    
    def test_modulos_disponiveis(self):
        """Testa se todos os módulos esperados estão disponíveis."""
        modulos_esperados = ['TAREFAS', 'SPRINTS', 'DOCUMENTOS', 'RISCOS', 'CUSTOS']
        modulos_modelo = [choice[0] for choice in PermissaoEquipe.MODULO_CHOICES]
        
        for modulo in modulos_esperados:
            assert modulo in modulos_modelo


@pytest.mark.django_db
class TestRelacionamentosModelos:
    """Testes para relacionamentos entre modelos."""
    
    def test_cascade_delete_equipe(self, equipe1, user1):
        """Testa cascata ao deletar equipe."""
        membro = MembroEquipe.objects.create(
            equipe=equipe1,
            usuario=user1,
            papel='PO'
        )
        
        permissao = PermissaoEquipe.objects.create(
            papel='PO',
            equipe=equipe1,
            modulo='TAREFAS',
            permissao='CRIAR'
        )
        
        membro_id = membro.id
        permissao_id = permissao.id
        
        # Deleta equipe
        equipe1.delete()
        
        # Verifica se membros e permissões foram deletados
        assert not MembroEquipe.objects.filter(id=membro_id).exists()
        assert not PermissaoEquipe.objects.filter(id=permissao_id).exists()
    
    def test_set_null_delete_user(self, equipe1, user1, user2):
        """Testa SET_NULL ao deletar usuário criador."""
        equipe1.criado_por = user1
        equipe1.save()
        
        membro = MembroEquipe.objects.create(
            equipe=equipe1,
            usuario=user2,
            papel='DEV',
            adicionado_por=user1
        )
        
        # Deleta usuário criador
        user1.delete()
        
        # Recarrega objetos
        equipe1.refresh_from_db()
        membro.refresh_from_db()
        
        # Verifica SET_NULL
        assert equipe1.criado_por is None
        assert membro.adicionado_por is None
        assert membro.usuario == user2  # Membro não deve ser deletado
    
    def test_cascade_delete_membro_usuario(self, equipe1, user1):
        """Testa cascata ao deletar usuário membro."""
        membro = MembroEquipe.objects.create(
            equipe=equipe1,
            usuario=user1,
            papel='PO'
        )
        
        membro_id = membro.id
        
        # Deleta usuário
        user1.delete()
        
        # Verifica se membro foi deletado
        assert not MembroEquipe.objects.filter(id=membro_id).exists()
