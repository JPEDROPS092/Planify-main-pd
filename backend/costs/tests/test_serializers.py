# tests/test_serializers.py
import pytest
from decimal import Decimal
from costs.models import Categoria, Custo, OrcamentoProjeto, OrcamentoTarefa, Alerta
from costs.serializers import (
    CategoriaSerializer, CustoSerializer, CustoListSerializer,
    OrcamentoProjetoSerializer, OrcamentoTarefaSerializer, AlertaSerializer,
    RelatorioGastoProjetoSerializer, RelatorioGastoCategoriasSerializer
)

pytestmark = pytest.mark.django_db

class TestCategoriaSerializer:
    def test_serialize_categoria(self, categoria_factory):
        cat = categoria_factory(nome="Equipamentos", descricao="Desc Equip")
        serializer = CategoriaSerializer(cat)
        data = serializer.data
        assert data['id'] == cat.id
        assert data['nome'] == "Equipamentos"
        assert data['descricao'] == "Desc Equip"

    def test_deserialize_categoria_valid(self):
        data = {"nome": "Software", "descricao": "Licenças de Software"}
        serializer = CategoriaSerializer(data=data)
        assert serializer.is_valid()
        cat = serializer.save()
        assert cat.nome == "Software"

    def test_deserialize_categoria_invalid(self):
        data = {"descricao": "Missing nome"} # nome is required
        serializer = CategoriaSerializer(data=data)
        assert not serializer.is_valid()
        assert 'nome' in serializer.errors

class TestCustoSerializer:
    def test_serialize_custo_detail(self, custo_factory, authenticated_user, projeto_factory, tarefa_factory, categoria_factory):
        user = authenticated_user
        user.full_name = "Test User Full" # Assuming User model has full_name
        user.save()

        proj = projeto_factory(name="Projeto Alpha")
        task = tarefa_factory(titulo="Tarefa Alpha", projeto=proj)
        cat = categoria_factory(nome="Viagens")
        custo = custo_factory(
            projeto=proj, tarefa=task, categoria=cat, criado_por=user,
            descricao="Passagem aérea", valor=Decimal("1250.75"), tipo="VARIAVEL"
        )
        serializer = CustoSerializer(custo)
        data = serializer.data
        assert data['id'] == custo.id
        assert data['projeto'] == proj.id
        assert data['projeto_nome'] == "Projeto Alpha" # or proj.titulo
        assert data['tarefa'] == task.id
        assert data['tarefa_titulo'] == "Tarefa Alpha"
        assert data['categoria'] == cat.id
        assert data['categoria_nome'] == "Viagens"
        assert data['descricao'] == "Passagem aérea"
        assert Decimal(data['valor']) == Decimal("1250.75")
        assert data['tipo'] == "VARIAVEL"
        assert data['tipo_display'] == "Custo Variável"
        assert data['criado_por'] == user.id
        # assert data['criado_por_nome'] == "Test User Full" # This depends on how full_name is populated

    def test_serialize_custo_list(self, custo_factory, projeto_factory):
        proj = projeto_factory(name="Projeto Beta")
        custo = custo_factory(projeto=proj, descricao="Almoço", valor=Decimal("35.00"))
        serializer = CustoListSerializer(custo)
        data = serializer.data
        assert data['id'] == custo.id
        assert data['projeto_nome'] == "Projeto Beta"
        assert 'observacoes' not in data # Check for simplified fields

class TestOrcamentoProjetoSerializer:
    def test_serialize_orcamento_projeto(self, orcamento_projeto_factory, projeto_factory, authenticated_user):
        user = authenticated_user
        # user.full_name = "Approver Full"
        # user.save()
        proj = projeto_factory(name="Projeto Gamma")
        op = orcamento_projeto_factory(projeto=proj, aprovado_por=user, valor_total=Decimal("10000.00"))

        # Mock annotated fields for serializer testing if not hitting the DB directly
        op.valor_utilizado = Decimal("2000.00")
        op.valor_restante = Decimal("8000.00")
        op.percentual_utilizado = Decimal("20.00")

        serializer = OrcamentoProjetoSerializer(op)
        data = serializer.data
        assert data['projeto_nome'] == "Projeto Gamma"
        assert Decimal(data['valor_total']) == Decimal("10000.00")
        # assert data['aprovado_por_nome'] == "Approver Full"
        assert Decimal(data['valor_utilizado']) == Decimal("2000.00")
        assert Decimal(data['valor_restante']) == Decimal("8000.00")
        assert Decimal(data['percentual_utilizado']) == Decimal("20.00")

class TestOrcamentoTarefaSerializer:
     def test_serialize_orcamento_tarefa(self, orcamento_tarefa_factory, tarefa_factory, authenticated_user, projeto_factory):
        user = authenticated_user
        # user.full_name = "Task Approver Full"
        # user.save()
        proj = projeto_factory(name="Projeto Delta")
        task = tarefa_factory(titulo="Tarefa Delta", projeto=proj)
        ot = orcamento_tarefa_factory(tarefa=task, aprovado_por=user, valor=Decimal("500.00"))

        ot.valor_utilizado = Decimal("100.00")
        ot.valor_restante = Decimal("400.00")
        ot.percentual_utilizado = Decimal("20.00")

        serializer = OrcamentoTarefaSerializer(ot)
        data = serializer.data
        assert data['tarefa_titulo'] == "Tarefa Delta"
        assert data['projeto_nome'] == "Projeto Delta"
        assert Decimal(data['valor']) == Decimal("500.00")
        # assert data['aprovado_por_nome'] == "Task Approver Full"
        assert Decimal(data['valor_utilizado']) == Decimal("100.00")


class TestAlertaSerializer:
    def test_serialize_alerta(self, alerta_factory, projeto_factory, authenticated_user):
        user = authenticated_user
        # user.full_name = "Resolver Full"
        # user.save()
        proj = projeto_factory(name="Projeto Epsilon")
        alerta = alerta_factory(
            projeto=proj, tipo="PROJETO", status="RESOLVIDO",
            resolvido_por=user, percentual=Decimal("95.50")
        )
        serializer = AlertaSerializer(alerta)
        data = serializer.data
        assert data['projeto_nome'] == "Projeto Epsilon"
        assert data['tipo_display'] == "Projeto"
        assert data['status_display'] == "Resolvido"
        # assert data['resolvido_por_nome'] == "Resolver Full"
        assert Decimal(data['percentual']) == Decimal("95.50")

class TestRelatorioGastoProjetoSerializer:
    def test_to_representation(self):
        raw_data = {
            'projeto_id': 1,
            'projeto_nome': 'Relatório Proj',
            'orcamento_total': Decimal('1000.00'),
            'valor_gasto': Decimal('500.00')
        }
        serializer = RelatorioGastoProjetoSerializer(instance=raw_data)
        data = serializer.data
        assert data['projeto_nome'] == 'Relatório Proj'
        assert data['orcamento_total'] == Decimal('1000.00')
        assert data['valor_gasto'] == Decimal('500.00')
        assert data['valor_restante'] == Decimal('500.00')
        assert data['percentual_gasto'] == Decimal('50.00')

    def test_to_representation_zero_orcamento(self):
        raw_data = {
            'projeto_id': 2,
            'projeto_nome': 'Zero Orc Proj',
            'orcamento_total': Decimal('0.00'),
            'valor_gasto': Decimal('50.00')
        }
        serializer = RelatorioGastoProjetoSerializer(instance=raw_data)
        data = serializer.data
        assert data['valor_restante'] == Decimal('-50.00')
        assert data['percentual_gasto'] == Decimal('0.00')

    def test_to_representation_none_values(self):
        raw_data = {
            'projeto_id': 3,
            'projeto_nome': 'None Val Proj',
            'orcamento_total': None,
            'valor_gasto': None
        }
        serializer = RelatorioGastoProjetoSerializer(instance=raw_data)
        data = serializer.data
        assert data['orcamento_total'] == Decimal('0.00')
        assert data['valor_gasto'] == Decimal('0.00')
        assert data['valor_restante'] == Decimal('0.00')
        assert data['percentual_gasto'] == Decimal('0.00')

class TestRelatorioGastoCategoriasSerializer:
    def test_to_representation(self):
        raw_data = {
            'categoria_id': 1,
            'categoria_nome': 'Infra',
            'valor_total': Decimal('300.00'),
            'percentual': Decimal('30.00')
        }
        serializer = RelatorioGastoCategoriasSerializer(instance=raw_data)
        data = serializer.data
        assert data['categoria_nome'] == 'Infra'
        assert data['valor_total'] == Decimal('300.00')
        assert data['percentual'] == Decimal('30.00')

    def test_to_representation_no_categoria(self):
        raw_data = {
            'categoria_id': None,
            'categoria_nome': None,
            'valor_total': Decimal('50.00'),
            'percentual': Decimal('5.00')
        }
        serializer = RelatorioGastoCategoriasSerializer(instance=raw_data)
        data = serializer.data
        assert data['categoria_nome'] == 'Sem Categoria'
        assert data['valor_total'] == Decimal('50.00')