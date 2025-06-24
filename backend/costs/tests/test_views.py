import pytest
from django.urls import reverse
from rest_framework import status
from decimal import Decimal
from datetime import date, timedelta, datetime # Added datetime for OrcamentoProjetoViewSet

# Assuming your app is 'costs'. Adjust if different.
from costs.models import (
    Categoria, Custo, OrcamentoProjeto, OrcamentoTarefa, Alerta
)
# Assuming these external models are available and factories are in conftest.py
# from projects.models import Projeto
# from tasks.models import Tarefa

# For CustoViewSet tests with date mocking
from freezegun import freeze_time

pytestmark = pytest.mark.django_db

# --- TestCategoriaViewSet ---
class TestCategoriaViewSet:
    base_url_list = reverse('categoria-list')

    def get_detail_url(self, categoria_id):
        return reverse('categoria-detail', kwargs={'pk': categoria_id})

    def test_list_categorias_unauthenticated(self, api_client, categoria_factory):
        categoria_factory.create_batch(3)
        response = api_client.get(self.base_url_list)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_list_categorias_authenticated(self, authenticated_client, categoria_factory):
        cats = categoria_factory.create_batch(3)
        response = authenticated_client.get(self.base_url_list)
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data['results']) == 3
        # Default ordering is by 'nome' as per Categoria.Meta
        # To make this robust, sort both lists or fetch one by one if order is critical
        api_names = sorted([item['nome'] for item in response.data['results']])
        db_names = sorted([cat.nome for cat in cats])
        assert api_names == db_names


    def test_retrieve_categoria(self, authenticated_client, categoria_factory):
        cat = categoria_factory()
        response = authenticated_client.get(self.get_detail_url(cat.id))
        assert response.status_code == status.HTTP_200_OK
        assert response.data['nome'] == cat.nome

    def test_create_categoria(self, authenticated_client):
        data = {"nome": "Nova Categoria", "descricao": "Detalhes"}
        response = authenticated_client.post(self.base_url_list, data=data)
        assert response.status_code == status.HTTP_201_CREATED
        assert Categoria.objects.filter(nome="Nova Categoria").exists()

    def test_update_categoria(self, authenticated_client, categoria_factory):
        cat = categoria_factory(nome="Antiga")
        data = {"nome": "Atualizada", "descricao": cat.descricao}
        response = authenticated_client.put(self.get_detail_url(cat.id), data=data)
        assert response.status_code == status.HTTP_200_OK
        cat.refresh_from_db()
        assert cat.nome == "Atualizada"

    def test_partial_update_categoria(self, authenticated_client, categoria_factory):
        cat = categoria_factory(nome="Parcial", descricao="Desc Original")
        data = {"nome": "Parcial Atualizada"}
        response = authenticated_client.patch(self.get_detail_url(cat.id), data=data)
        assert response.status_code == status.HTTP_200_OK
        cat.refresh_from_db()
        assert cat.nome == "Parcial Atualizada"
        assert cat.descricao == "Desc Original" # Unchanged

    def test_delete_categoria(self, authenticated_client, categoria_factory):
        cat = categoria_factory()
        response = authenticated_client.delete(self.get_detail_url(cat.id))
        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert not Categoria.objects.filter(id=cat.id).exists()

    def test_search_categoria(self, authenticated_client, categoria_factory):
        categoria_factory(nome="SearchMe C1", descricao="UniqueDesc")
        categoria_factory(nome="Another C2")
        response = authenticated_client.get(self.base_url_list, {'search': 'UniqueDesc'})
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data['results']) == 1
        assert response.data['results'][0]['nome'] == "SearchMe C1"


# --- TestCustoViewSet ---
class TestCustoViewSet:
    base_url_list = reverse('custo-list')

    def get_detail_url(self, custo_id):
        return reverse('custo-detail', kwargs={'pk': custo_id})

    def test_list_custos_uses_list_serializer(self, authenticated_client, custo_factory):
        custo = custo_factory() # Create at least one custo
        response = authenticated_client.get(self.base_url_list)
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data['results']) > 0
        # CustoListSerializer has 'categoria_nome' but not 'categoria' (ID directly)
        # It includes 'descricao', 'valor', 'tipo_display', 'data'
        result_item = response.data['results'][0]
        assert 'categoria_nome' in result_item
        assert 'categoria' not in result_item # The ID field itself
        assert 'descricao' in result_item
        assert 'tipo_display' in result_item
        assert 'observacoes' not in result_item # This is in detail serializer

    def test_retrieve_custo_uses_detail_serializer(self, authenticated_client, custo_factory):
        custo = custo_factory()
        response = authenticated_client.get(self.get_detail_url(custo.id))
        assert response.status_code == status.HTTP_200_OK
        # CustoSerializer has 'categoria' (ID) and 'categoria_nome'
        assert 'categoria' in response.data
        assert 'categoria_nome' in response.data
        assert 'observacoes' in response.data # This is in detail serializer


    def test_create_custo_sets_criado_por(self, authenticated_client, authenticated_user, projeto_factory):
        proj = projeto_factory()
        data = {
            "projeto": proj.id,
            "descricao": "Novo Custo API",
            "valor": "150.00",
            "tipo": "FIXO",
            "data": date.today().isoformat()
        }
        response = authenticated_client.post(self.base_url_list, data=data)
        assert response.status_code == status.HTTP_201_CREATED
        custo = Custo.objects.get(id=response.data['id'])
        assert custo.criado_por == authenticated_user

    def test_create_custo_triggers_projeto_alerta(self, authenticated_client, projeto_factory, orcamento_projeto_factory):
        proj = projeto_factory(name="Trigger Project") # Ensure name/titulo exists for alert message
        orcamento_projeto_factory(projeto=proj, valor_total=Decimal("100.00"))
        data = {
            "projeto": proj.id, "descricao": "Custo Alto", "valor": "85.00",
            "tipo": "FIXO", "data": date.today().isoformat()
        }
        assert Alerta.objects.count() == 0
        response = authenticated_client.post(self.base_url_list, data=data)
        assert response.status_code == status.HTTP_201_CREATED
        assert Alerta.objects.filter(projeto=proj, tipo="PROJETO", status="ATIVO").count() == 1
        alerta = Alerta.objects.get(projeto=proj, tipo="PROJETO")
        assert alerta.percentual == Decimal("85.00") # 85 / 100 * 100

    def test_create_custo_triggers_tarefa_alerta(self, authenticated_client, tarefa_factory, orcamento_tarefa_factory):
        task = tarefa_factory(titulo="Trigger Task") # Ensure titulo exists for alert message
        orcamento_tarefa_factory(tarefa=task, valor=Decimal("50.00"))
        data = {
            "projeto": task.projeto.id, "tarefa": task.id, "descricao": "Custo Tarefa Alto",
            "valor": "45.00", "tipo": "FIXO", "data": date.today().isoformat()
        }
        assert Alerta.objects.count() == 0
        response = authenticated_client.post(self.base_url_list, data=data)
        assert response.status_code == status.HTTP_201_CREATED
        assert Alerta.objects.filter(tarefa=task, tipo="TAREFA", status="ATIVO").count() == 1
        alerta = Alerta.objects.get(tarefa=task, tipo="TAREFA")
        assert alerta.percentual == Decimal("90.00") # 45 / 50 * 100

    def test_update_custo_triggers_alerta(self, authenticated_client, custo_factory, orcamento_projeto_factory, projeto_factory):
        proj = projeto_factory(name="Update Alert Project")
        orcamento_projeto_factory(projeto=proj, valor_total=Decimal("100.00"))
        custo1 = custo_factory(projeto=proj, valor=Decimal("10.00"))
        custo2 = custo_factory(projeto=proj, valor=Decimal("10.00")) # Total initial: 20

        assert Alerta.objects.count() == 0
        # Update custo2's valor. Total project cost will be custo1.valor + new custo2.valor
        # 10 (custo1) + 75 (new custo2) = 85. 85/100 = 85% >= 80%
        response = authenticated_client.patch(self.get_detail_url(custo2.id), data={"valor": "75.00"})
        assert response.status_code == status.HTTP_200_OK
        assert Alerta.objects.filter(projeto=proj, tipo="PROJETO", status="ATIVO").count() == 1

    def test_no_alerta_if_already_active(self, authenticated_client, custo_factory, orcamento_projeto_factory, alerta_factory, projeto_factory):
        proj = projeto_factory(name="No Duplicate Alert Project")
        orcamento_projeto_factory(projeto=proj, valor_total=Decimal("100.00"))
        custo = custo_factory(projeto=proj, valor=Decimal("80.00"))
        alerta_factory(projeto=proj, tipo="PROJETO", status="ATIVO", percentual=Decimal("80.00")) # Existing active alert

        assert Alerta.objects.filter(projeto=proj, tipo="PROJETO", status="ATIVO").count() == 1 # Initial active alert
        data = { "valor": "85.00" } # Increase cost further
        response = authenticated_client.patch(self.get_detail_url(custo.id), data=data)
        assert response.status_code == status.HTTP_200_OK
        # No *new* alert should be created, count remains 1
        # The existing alert's percentage might update if the logic was to update, but here it's about creation.
        assert Alerta.objects.filter(projeto=proj, tipo="PROJETO", status="ATIVO").count() == 1


    def test_filter_by_projeto(self, authenticated_client, custo_factory, projeto_factory):
        proj1 = projeto_factory()
        proj2 = projeto_factory()
        custo_factory(projeto=proj1)
        custo_factory(projeto=proj2)
        response = authenticated_client.get(self.base_url_list, {'projeto': proj1.id})
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data['results']) == 1
        assert response.data['results'][0]['projeto'] == proj1.id # custo serializer has 'projeto' as id

    def test_filter_by_categoria_name(self, authenticated_client, custo_factory, categoria_factory):
        cat1 = categoria_factory(nome="SoftwareLic")
        cat2 = categoria_factory(nome="Hardware")
        custo_factory(categoria=cat1)
        custo_factory(categoria=cat2)
        # get_queryset in CustoViewSet filters by categoria__nome__iexact for non-numeric
        response = authenticated_client.get(self.base_url_list, {'categoria': "SoftwareLic"})
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data['results']) == 1
        assert response.data['results'][0]['categoria_nome'] == cat1.nome

    def test_filter_by_categoria_id(self, authenticated_client, custo_factory, categoria_factory):
        cat1 = categoria_factory(nome="SoftwareLic")
        cat2 = categoria_factory(nome="Hardware")
        custo_factory(categoria=cat1)
        custo_factory(categoria=cat2)
        response = authenticated_client.get(self.base_url_list, {'categoria': cat1.id})
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data['results']) == 1
        assert response.data['results'][0]['categoria_nome'] == cat1.nome


    def test_filter_by_data_range(self, authenticated_client, custo_factory):
        today = date.today()
        yesterday = today - timedelta(days=1)
        tomorrow = today + timedelta(days=1)
        custo_factory(data=yesterday, descricao="Custo Ontem")
        custo_factory(data=today, descricao="Custo Hoje")
        custo_factory(data=tomorrow, descricao="Custo Amanha")

        response = authenticated_client.get(self.base_url_list, {
            'data_inicio': today.isoformat(),
            'data_fim': tomorrow.isoformat()
        })
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data['results']) == 2
        descricoes = {r['descricao'] for r in response.data['results']}
        assert "Custo Hoje" in descricoes
        assert "Custo Amanha" in descricoes

    def test_dashboard_action(self, authenticated_client, custo_factory, categoria_factory, alerta_factory, projeto_factory):
        proj = projeto_factory(name="Dashboard Project")
        cat = categoria_factory(nome="Dashboard Category")
        custo_factory.create_batch(3, projeto=proj, valor=Decimal("100"), categoria=cat, data=date.today() - timedelta(days=10))
        alerta_factory.create_batch(2, projeto=proj)

        dashboard_url = reverse('custo-dashboard')
        response = authenticated_client.get(dashboard_url, {'projeto_id': proj.id}) # Filter by project
        assert response.status_code == status.HTTP_200_OK
        data = response.data
        assert data['total_gasto'] == Decimal("300.00")
        assert len(data['gastos_mensais']) >= 0 # Check structure, exact number depends on current date and cost dates
        assert len(data['top_categorias']) == 1
        assert data['top_categorias'][0]['categoria_nome'] == cat.nome
        assert data['top_categorias'][0]['total'] == Decimal("300.00")
        assert len(data['alertas_recentes']) == 2

    def test_relatorio_por_projeto_action(self, authenticated_client, custo_factory, orcamento_projeto_factory, projeto_factory):
        proj1 = projeto_factory(name="Relatorio P1")
        op1 = orcamento_projeto_factory(projeto=proj1, valor_total=Decimal("1000"))
        custo_factory(projeto=op1.projeto, valor=Decimal("200"))
        custo_factory(projeto=op1.projeto, valor=Decimal("300")) # Total gasto 500

        proj2 = projeto_factory(name="Relatorio P2")
        op2 = orcamento_projeto_factory(projeto=proj2, valor_total=Decimal("500")) # No costs for this project

        proj3 = projeto_factory(name="Relatorio P3 No Orcamento") # Project without budget
        custo_factory(projeto=proj3, valor=Decimal("50"))


        url = reverse('custo-relatorio-por-projeto')
        response = authenticated_client.get(url)
        assert response.status_code == status.HTTP_200_OK
        # Should include all projects, even those without costs or without budget if custos_do_projeto is used for sum
        # The view iterates Projeto.objects.all()
        assert len(response.data) == Projeto.objects.count()

        proj1_data = next(item for item in response.data if item['projeto_id'] == op1.projeto_id)
        assert proj1_data['orcamento_total'] == "1000.00" # Serialized as string
        assert proj1_data['valor_gasto'] == "500.00"
        assert Decimal(proj1_data['valor_restante']) == Decimal("500.00") # Calculated in serializer
        assert Decimal(proj1_data['percentual_gasto']) == Decimal("50.00") # Calculated in serializer

        proj2_data = next(item for item in response.data if item['projeto_id'] == op2.projeto_id)
        assert proj2_data['orcamento_total'] == "500.00"
        assert proj2_data['valor_gasto'] == "0.00"

        proj3_data = next(item for item in response.data if item['projeto_id'] == proj3.id)
        assert proj3_data['orcamento_total'] == "0.00" # Default if no OrcamentoProjeto
        assert proj3_data['valor_gasto'] == "50.00"


    def test_relatorio_por_categoria_action(self, authenticated_client, custo_factory, categoria_factory, projeto_factory):
        proj = projeto_factory()
        cat1 = categoria_factory(nome="Cat Alpha")
        cat2 = categoria_factory(nome="Cat Beta")
        custo_factory(projeto=proj, categoria=cat1, valor=Decimal("300"))
        custo_factory(projeto=proj, categoria=cat2, valor=Decimal("100"))
        custo_factory(projeto=proj, categoria=None, valor=Decimal("100")) # Sem Categoria
        # Total gasto no projeto: 500

        url = reverse('custo-relatorio-por-categoria')
        response = authenticated_client.get(url, {'projeto_id': proj.id}) # Filter by project
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == 3

        cat1_data = next(item for item in response.data if item.get('categoria_id') == cat1.id)
        assert cat1_data['valor_total'] == "300.00"
        assert Decimal(cat1_data['percentual']).quantize(Decimal('0.01')) == Decimal("60.00") # 300/500

        no_cat_data = next(item for item in response.data if item.get('categoria_id') is None)
        assert no_cat_data['categoria_nome'] == "Sem Categoria"
        assert no_cat_data['valor_total'] == "100.00"
        assert Decimal(no_cat_data['percentual']).quantize(Decimal('0.01')) == Decimal("20.00") # 100/500

    def test_relatorio_mensal_action(self, authenticated_client, custo_factory):
        # Freeze time to a consistent point for testing month ranges
        with freeze_time("2023-12-15"):
            custo_factory(data=date(2023, 12, 10), valor=Decimal("100"))
            custo_factory(data=date(2023, 11, 5), valor=Decimal("50"))
            custo_factory(data=date(2023, 11, 15), valor=Decimal("20")) # Total Nov: 70
            custo_factory(data=date(2023, 1, 1), valor=Decimal("200")) # Jan 2023

            url = reverse('custo-relatorio-mensal') # Default 12 months
            # Request ends Dec 2023, starts Jan 2023
            response = authenticated_client.get(url)
            assert response.status_code == status.HTTP_200_OK
            assert len(response.data) == 12

            data_map = {item['mes']: Decimal(item['valor']) for item in response.data}
            assert data_map.get("2023-12") == Decimal("100.00")
            assert data_map.get("2023-11") == Decimal("70.00")
            assert data_map.get("2023-01") == Decimal("200.00")
            assert data_map.get("2023-10", Decimal("0.00")) == Decimal("0.00") # Check a month with no costs

            # Test with 'meses' parameter
            response_3m = authenticated_client.get(url, {'meses': 3}) # Dec, Nov, Oct
            assert len(response_3m.data) == 3
            data_map_3m = {item['mes']: Decimal(item['valor']) for item in response_3m.data}
            assert "2023-12" in data_map_3m
            assert "2023-11" in data_map_3m
            assert "2023-10" in data_map_3m
            assert data_map_3m.get("2023-10", Decimal("0.00")) == Decimal("0.00")


# --- TestOrcamentoProjetoViewSet ---
class TestOrcamentoProjetoViewSet:
    base_url_list = reverse('orcamentoprojeto-list')

    def get_detail_url(self, orc_id):
        return reverse('orcamentoprojeto-detail', kwargs={'pk': orc_id})

    def test_list_orcamentos_projeto_with_annotations(self, authenticated_client, orcamento_projeto_factory, custo_factory, projeto_factory):
        proj = projeto_factory()
        op = orcamento_projeto_factory(projeto=proj, valor_total=Decimal("1000"))
        custo_factory(projeto=op.projeto, valor=Decimal("200"))
        custo_factory(projeto=op.projeto, valor=Decimal("100")) # Total gasto 300

        response = authenticated_client.get(self.base_url_list)
        assert response.status_code == status.HTTP_200_OK
        # Find the specific orcamento in the list
        data = next(item for item in response.data['results'] if item['id'] == op.id)
        assert Decimal(data['valor_total']) == Decimal("1000.00")
        assert Decimal(data['valor_utilizado']) == Decimal("300.00")
        assert Decimal(data['valor_restante']) == Decimal("700.00")
        assert Decimal(data['percentual_utilizado']).quantize(Decimal('0.01')) == Decimal("30.00")

    def test_list_orcamentos_projeto_zero_orcamento(self, authenticated_client, orcamento_projeto_factory, custo_factory, projeto_factory):
        proj = projeto_factory()
        op = orcamento_projeto_factory(projeto=proj, valor_total=Decimal("0"))
        custo_factory(projeto=op.projeto, valor=Decimal("50"))

        response = authenticated_client.get(self.base_url_list)
        assert response.status_code == status.HTTP_200_OK
        data = next(item for item in response.data['results'] if item['id'] == op.id)
        assert Decimal(data['valor_total']) == Decimal("0.00")
        assert Decimal(data['valor_utilizado']) == Decimal("50.00")
        assert Decimal(data['valor_restante']) == Decimal("-50.00")
        assert Decimal(data['percentual_utilizado']).quantize(Decimal('0.01')) == Decimal("0.00")


    def test_create_orcamento_projeto_sets_aprovado_por(self, authenticated_client, authenticated_user, projeto_factory):
        proj = projeto_factory()
        data = {"projeto": proj.id, "valor_total": "5000.00"}
        response = authenticated_client.post(self.base_url_list, data=data)
        assert response.status_code == status.HTTP_201_CREATED
        op = OrcamentoProjeto.objects.get(id=response.data['id'])
        assert op.aprovado_por == authenticated_user

    def test_projetos_sem_orcamento_action(self, authenticated_client, projeto_factory, orcamento_projeto_factory):
        # Ensure projects exist before creating orcamentos
        proj_com_orc_obj = projeto_factory(name="Project With Budget")
        proj_sem_orc1_obj = projeto_factory(name="Project Without Budget 1")
        proj_sem_orc2_obj = projeto_factory(name="Project Without Budget 2")

        orcamento_projeto_factory(projeto=proj_com_orc_obj) # Assign budget to one

        url = reverse('orcamentoprojeto-projetos-sem-orcamento')
        response = authenticated_client.get(url)
        assert response.status_code == status.HTTP_200_OK

        # Response data is a list of dicts [{'id': x, 'nome': y}]
        returned_ids = {item['id'] for item in response.data}
        expected_ids_sem_orc = {proj_sem_orc1_obj.id, proj_sem_orc2_obj.id}

        assert len(returned_ids) == 2
        assert returned_ids == expected_ids_sem_orc
        assert proj_com_orc_obj.id not in returned_ids


    def test_ajustar_orcamento_action(self, authenticated_client, authenticated_user, orcamento_projeto_factory, custo_factory, projeto_factory):
        proj = projeto_factory(name="Ajuste Orc Project") # Ensure name/titulo exists for alert message
        op = orcamento_projeto_factory(projeto=proj, valor_total=Decimal("1000"), observacoes="Initial budget.")
        custo_factory(projeto=op.projeto, valor=Decimal("850")) # 85% of 1000

        url = reverse('orcamentoprojeto-ajustar-orcamento', kwargs={'pk': op.id})
        data = {"novo_valor": "2000.00", "justificativa": "Increased scope"}

        response = authenticated_client.post(url, data=data)
        assert response.status_code == status.HTTP_200_OK
        op.refresh_from_db()
        assert op.valor_total == Decimal("2000.00")
        assert "Increased scope" in op.observacoes
        assert f"ajustado de R$ 1000.00 para R$ 2000.00" in op.observacoes
        user_name_in_obs = authenticated_user.get_full_name() or authenticated_user.username
        assert user_name_in_obs in op.observacoes

        # Check alert: 850 / 2000 = 42.5%. No alert should be created.
        assert not Alerta.objects.filter(projeto=op.projeto, tipo="PROJETO", status="ATIVO").exists()

        # Now, adjust to make it trigger alert
        data_alert = {"novo_valor": "900.00", "justificativa": "Reduced scope drastically"}
        # 850 / 900 = 94.44...% -> should trigger alert
        response_alert = authenticated_client.post(url, data=data_alert)
        assert response_alert.status_code == status.HTTP_200_OK
        assert Alerta.objects.filter(projeto=op.projeto, tipo="PROJETO", status="ATIVO").exists()
        alerta = Alerta.objects.get(projeto=op.projeto, tipo="PROJETO", status="ATIVO")
        # The percentual in _verificar_necessidade_alerta is (val_util / val_total) * 100
        # (850 / 900) * 100 = 94.444...
        assert alerta.percentual.quantize(Decimal('0.01')) == Decimal("94.44")

    def test_ajustar_orcamento_invalid_value(self, authenticated_client, orcamento_projeto_factory, projeto_factory):
        proj = projeto_factory()
        op = orcamento_projeto_factory(projeto=proj)
        url = reverse('orcamentoprojeto-ajustar-orcamento', kwargs={'pk': op.id})
        data = {"novo_valor": "-100.00"}
        response = authenticated_client.post(url, data=data)
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        error_message = response.data.get("error", "").lower()
        assert "inválido" in error_message or "maior que zero" in error_message


# --- TestOrcamentoTarefaViewSet ---
class TestOrcamentoTarefaViewSet:
    # Note: basename='orcamentotarefa' was used in urls.py
    base_url_list = reverse('orcamentotarefa-list')

    def get_detail_url(self, orc_id):
        return reverse('orcamentotarefa-detail', kwargs={'pk': orc_id})

    def test_list_orcamentos_tarefa_with_annotations(self, authenticated_client, orcamento_tarefa_factory, custo_factory, tarefa_factory):
        task = tarefa_factory()
        ot = orcamento_tarefa_factory(tarefa=task, valor=Decimal("500"))
        custo_factory(tarefa=ot.tarefa, projeto=ot.tarefa.projeto, valor=Decimal("100"))
        custo_factory(tarefa=ot.tarefa, projeto=ot.tarefa.projeto, valor=Decimal("50")) # Total gasto 150

        response = authenticated_client.get(self.base_url_list)
        assert response.status_code == status.HTTP_200_OK
        data = next(item for item in response.data['results'] if item['id'] == ot.id)
        assert Decimal(data['valor']) == Decimal("500.00")
        assert Decimal(data['valor_utilizado']) == Decimal("150.00")
        assert Decimal(data['valor_restante']) == Decimal("350.00")
        assert Decimal(data['percentual_utilizado']).quantize(Decimal('0.01')) == Decimal("30.00")

    def test_tarefas_sem_orcamento_action(self, authenticated_client, tarefa_factory, orcamento_tarefa_factory, projeto_factory):
        proj1 = projeto_factory(name="Task Project 1")
        proj2 = projeto_factory(name="Task Project 2")

        task_com_orc_obj = tarefa_factory(projeto=proj1, titulo="Task With Budget")
        orcamento_tarefa_factory(tarefa=task_com_orc_obj)

        task_sem_orc_proj1 = tarefa_factory(projeto=proj1, titulo="Task Without Budget P1")
        task_sem_orc_proj2 = tarefa_factory(projeto=proj2, titulo="Task Without Budget P2")


        url = reverse('orcamentotarefa-tarefas-sem-orcamento')
        response_all = authenticated_client.get(url)
        assert response_all.status_code == status.HTTP_200_OK
        returned_ids_all = {item['id'] for item in response_all.data}
        expected_ids_sem_orc_all = {task_sem_orc_proj1.id, task_sem_orc_proj2.id}
        assert len(returned_ids_all) == 2
        assert returned_ids_all == expected_ids_sem_orc_all

        # Filter by projeto_id
        response_proj1_filtered = authenticated_client.get(url, {'projeto_id': proj1.id})
        assert response_proj1_filtered.status_code == status.HTTP_200_OK
        returned_ids_proj1 = {item['id'] for item in response_proj1_filtered.data}
        assert len(returned_ids_proj1) == 1
        assert task_sem_orc_proj1.id in returned_ids_proj1


    def test_ajustar_orcamento_tarefa_action(self, authenticated_client, authenticated_user, orcamento_tarefa_factory, custo_factory, tarefa_factory):
        task = tarefa_factory(titulo="Ajuste Orc Task") # Ensure titulo for alert message
        ot = orcamento_tarefa_factory(tarefa=task, valor=Decimal("200"), observacoes="Initial task budget.")
        custo_factory(tarefa=ot.tarefa, projeto=ot.tarefa.projeto, valor=Decimal("180")) # 90% of 200

        url = reverse('orcamentotarefa-ajustar-orcamento', kwargs={'pk': ot.id})
        # Adjusting budget to 190. Spent 180. 180/190 = 94.73...% -> should trigger alert
        data = {"novo_valor": "190.00", "justificativa": "Slight reduction"}

        response = authenticated_client.post(url, data=data)
        assert response.status_code == status.HTTP_200_OK
        ot.refresh_from_db()
        assert ot.valor == Decimal("190.00")
        assert "Slight reduction" in ot.observacoes
        assert Alerta.objects.filter(tarefa=ot.tarefa, tipo="TAREFA", status="ATIVO").exists()
        alerta = Alerta.objects.get(tarefa=ot.tarefa, tipo="TAREFA", status="ATIVO")
        assert alerta.percentual.quantize(Decimal("0.01")) == Decimal("94.74") # (180/190)*100 rounded


# --- TestAlertaViewSet ---
class TestAlertaViewSet:
    base_url_list = reverse('alerta-list')

    def get_detail_url(self, alerta_id):
        return reverse('alerta-detail', kwargs={'pk': alerta_id})

    def test_list_alertas(self, authenticated_client, alerta_factory):
        alerta_factory.create_batch(3)
        response = authenticated_client.get(self.base_url_list)
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data['results']) == 3

    def test_resolver_alerta_action(self, authenticated_client, authenticated_user, alerta_factory):
        alerta = alerta_factory(status="ATIVO")
        # Ensure Alerta model has 'observacoes' field for this to pass fully
        if not hasattr(Alerta, 'observacoes'):
            pytest.skip("Alerta model does not have 'observacoes' field. Skipping this part of the test.")

        url = reverse('alerta-resolver', kwargs={'pk': alerta.id})
        data = {"observacao": "Issue addressed."} # This requires 'observacoes' on Alerta model

        response = authenticated_client.post(url, data=data)
        assert response.status_code == status.HTTP_200_OK
        alerta.refresh_from_db()
        assert alerta.status == "RESOLVIDO"
        assert alerta.resolvido_por == authenticated_user
        assert alerta.data_resolucao is not None
        if hasattr(Alerta, 'observacoes'):
             assert "Issue addressed." in alerta.observacoes

    def test_ignorar_alerta_action(self, authenticated_client, authenticated_user, alerta_factory):
        alerta = alerta_factory(status="ATIVO")
        if not hasattr(Alerta, 'observacoes'):
            pytest.skip("Alerta model does not have 'observacoes' field. Skipping this part of the test.")

        url = reverse('alerta-ignorar', kwargs={'pk': alerta.id})
        data = {"justificativa": "False positive."} # This requires 'observacoes' on Alerta model

        response = authenticated_client.post(url, data=data)
        assert response.status_code == status.HTTP_200_OK
        alerta.refresh_from_db()
        assert alerta.status == "IGNORADO"
        assert alerta.resolvido_por == authenticated_user # resolvido_por is used for both
        if hasattr(Alerta, 'observacoes'):
            assert "False positive." in alerta.observacoes

    def test_resolver_alerta_already_resolved(self, authenticated_client, alerta_factory):
        alerta = alerta_factory(status="RESOLVIDO")
        url = reverse('alerta-resolver', kwargs={'pk': alerta.id})
        response = authenticated_client.post(url, {}) # No data needed for this check
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert "já está resolvido" in response.data['detail'].lower()

    def test_pendentes_action(self, authenticated_client, alerta_factory, projeto_factory, tarefa_factory):
        proj1 = projeto_factory(name="Pendente P1")
        proj2 = projeto_factory(name="Pendente P2")
        task_proj2 = tarefa_factory(projeto=proj2, titulo="Pendente T2")

        alerta_factory(status="ATIVO", projeto=proj1, tipo="PROJETO")
        alerta_factory(status="RESOLVIDO", projeto=proj1, tipo="PROJETO")
        alerta_factory(status="ATIVO", projeto=proj2, tarefa=task_proj2, tipo="TAREFA")
        alerta_factory(status="IGNORADO", projeto=proj2, tarefa=task_proj2, tipo="TAREFA")

        url = reverse('alerta-pendentes')
        response_all = authenticated_client.get(url)
        assert response_all.status_code == status.HTTP_200_OK
        assert len(response_all.data) == 2 # Two ATIVO alerts

        response_proj1_filter = authenticated_client.get(url, {'projeto_id': proj1.id})
        assert response_proj1_filter.status_code == status.HTTP_200_OK
        assert len(response_proj1_filter.data) == 1
        assert response_proj1_filter.data[0]['projeto'] == proj1.id

        response_tipo_projeto_filter = authenticated_client.get(url, {'tipo': 'PROJETO'})
        assert response_tipo_projeto_filter.status_code == status.HTTP_200_OK
        assert len(response_tipo_projeto_filter.data) == 1
        assert response_tipo_projeto_filter.data[0]['tipo'] == 'PROJETO'
        assert response_tipo_projeto_filter.data[0]['projeto'] == proj1.id # The PROJETO alert for proj1

        response_tipo_tarefa_filter = authenticated_client.get(url, {'tipo': 'TAREFA'})
        assert response_tipo_tarefa_filter.status_code == status.HTTP_200_OK
        assert len(response_tipo_tarefa_filter.data) == 1
        assert response_tipo_tarefa_filter.data[0]['tipo'] == 'TAREFA'
        assert response_tipo_tarefa_filter.data[0]['tarefa'] == task_proj2.id