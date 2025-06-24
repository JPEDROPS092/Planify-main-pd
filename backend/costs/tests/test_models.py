# tests/test_models.py
import pytest
from decimal import Decimal
from django.utils import timezone
from costs.models import Categoria, Custo, OrcamentoProjeto, OrcamentoTarefa, Alerta

pytestmark = pytest.mark.django_db

class TestCategoriaModel:
    def test_categoria_creation(self, categoria_factory):
        cat = categoria_factory(nome="Serviços", descricao="Serviços de terceiros")
        assert cat.nome == "Serviços"
        assert str(cat) == "Serviços"
        assert Categoria.objects.count() == 1

class TestCustoModel:
    def test_custo_creation(self, custo_factory, projeto_factory, tarefa_factory, categoria_factory):
        proj = projeto_factory(name="Projeto X")
        cat = categoria_factory(nome="Material")
        custo = custo_factory(
            projeto=proj,
            categoria=cat,
            descricao="Compra de parafusos",
            valor=Decimal("50.25")
        )
        assert custo.descricao == "Compra de parafusos"
        assert custo.valor == Decimal("50.25")
        assert str(custo) == "Compra de parafusos - R$ 50.25"
        assert Custo.objects.count() == 1
        assert custo.projeto.name == "Projeto X" # Test related_name access
        assert proj.custos_do_projeto.count() == 1 # Test related_name access

class TestOrcamentoProjetoModel:
    def test_orcamento_projeto_creation(self, orcamento_projeto_factory, projeto_factory):
        proj = projeto_factory(name="Orçamento P1")
        op = orcamento_projeto_factory(projeto=proj, valor_total=Decimal("5000.00"))
        assert op.valor_total == Decimal("5000.00")
        assert str(op) == f"Orçamento de {proj.titulo} - R$ 5000.00" # Check proj.titulo or proj.name
        assert OrcamentoProjeto.objects.count() == 1
        assert proj.orcamento == op # Test one-to-one reverse access

class TestOrcamentoTarefaModel:
    def test_orcamento_tarefa_creation(self, orcamento_tarefa_factory, tarefa_factory):
        task = tarefa_factory(titulo="Orçamento T1")
        ot = orcamento_tarefa_factory(tarefa=task, valor=Decimal("300.00"))
        assert ot.valor == Decimal("300.00")
        assert str(ot) == f"Orçamento para {task.titulo} - R$ 300.00"
        assert OrcamentoTarefa.objects.count() == 1
        assert task.orcamento == ot

class TestAlertaModel:
    def test_alerta_projeto_creation(self, alerta_factory, projeto_factory):
        proj = projeto_factory(name="Alerta Proj")
        alerta = alerta_factory(projeto=proj, tipo="PROJETO", percentual=Decimal("90.00"))
        assert alerta.tipo == "PROJETO"
        assert str(alerta) == f"Alerta de 90.00% para {proj.titulo}"
        assert Alerta.objects.count() == 1

    def test_alerta_tarefa_creation(self, alerta_factory, tarefa_factory):
        task = tarefa_factory(titulo="Alerta Task")
        alerta = alerta_factory(projeto=task.projeto, tarefa=task, tipo="TAREFA", percentual=Decimal("80.00"))
        assert alerta.tipo == "TAREFA"
        assert str(alerta) == f"Alerta de 80.00% para {task.titulo}"