# tests/conftest.py
import pytest
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from decimal import Decimal
from datetime import date, datetime, timezone


User = get_user_model()

@pytest.fixture
def api_client():
    return APIClient()

@pytest.fixture
def user_factory(db):
    def create_user(**kwargs):
        # return UserFactory(**kwargs) # If using factory_boy
        defaults = {"username": "testuser", "password": "password"}
        defaults.update(kwargs)
        return User.objects.create_user(**defaults)
    return create_user

@pytest.fixture
def authenticated_user(db, user_factory):
    return user_factory()

@pytest.fixture
def authenticated_client(api_client, authenticated_user):
    api_client.force_authenticate(user=authenticated_user)
    return api_client

# --- Model Factories (Illustrative - use factory_boy or mixer) ---
@pytest.fixture
def projeto_factory(db):
    from projects.models import Projeto # Assuming this path
    def create_projeto(**kwargs):
        defaults = {"name": "Test Project", "titulo": "Test Project Title"} # Adjust to your Projeto model
        defaults.update(kwargs)
        if "name" not in defaults and "titulo" in defaults: # Adapt based on your model's actual fields
             defaults["name"] = defaults["titulo"]
        elif "titulo" not in defaults and "name" in defaults:
             defaults["titulo"] = defaults["name"]

        # Ensure required fields are present
        if not defaults.get("name"): # or titulo
            raise ValueError("Projeto must have a name/titulo")
        return Projeto.objects.create(**defaults)
    return create_projeto

@pytest.fixture
def tarefa_factory(db, projeto_factory):
    from tasks.models import Tarefa # Assuming this path
    def create_tarefa(projeto=None, **kwargs):
        defaults = {"titulo": "Test Task"} # Adjust
        defaults.update(kwargs)
        if projeto is None:
            projeto = projeto_factory()
        defaults['projeto'] = projeto
        return Tarefa.objects.create(**defaults)
    return create_tarefa

@pytest.fixture
def categoria_factory(db):
    from costs.models import Categoria # Assuming your app is 'costs'
    def create_categoria(**kwargs):
        defaults = {"nome": "Test Categoria"}
        defaults.update(kwargs)
        return Categoria.objects.create(**defaults)
    return create_categoria

@pytest.fixture
def custo_factory(db, projeto_factory, authenticated_user, categoria_factory, tarefa_factory):
    from costs.models import Custo
    def create_custo(projeto=None, tarefa=None, categoria=None, criado_por=None, **kwargs):
        if projeto is None:
            projeto = projeto_factory()
        if criado_por is None:
            criado_por = authenticated_user

        defaults = {
            "projeto": projeto,
            "tarefa": tarefa, # Can be None
            "categoria": categoria, # Can be None
            "descricao": "Test Custo",
            "valor": Decimal("100.00"),
            "tipo": "FIXO",
            "data": date.today(),
            "criado_por": criado_por,
        }
        defaults.update(kwargs)
        return Custo.objects.create(**defaults)
    return create_custo

@pytest.fixture
def orcamento_projeto_factory(db, projeto_factory, authenticated_user):
    from costs.models import OrcamentoProjeto
    def create_orcamento_projeto(projeto=None, aprovado_por=None, **kwargs):
        if projeto is None:
            projeto = projeto_factory()
        if aprovado_por is None:
            aprovado_por = authenticated_user
        defaults = {
            "projeto": projeto,
            "valor_total": Decimal("1000.00"),
            "aprovado_por": aprovado_por,
            "data_aprovacao": date.today() # Note: model sets auto_now_add, might conflict
        }
        defaults.update(kwargs)
        # For auto_now_add, it's better to let the model handle it or override for testing
        op, created = OrcamentoProjeto.objects.update_or_create(
            projeto=defaults.pop('projeto'), # Ensure one-to-one
            defaults=defaults
        )
        if not created and 'data_aprovacao' in defaults : # if we provided one
            op.data_aprovacao = defaults['data_aprovacao']
            op.save()
        return op
    return create_orcamento_projeto

@pytest.fixture
def orcamento_tarefa_factory(db, tarefa_factory, authenticated_user):
    from costs.models import OrcamentoTarefa
    def create_orcamento_tarefa(tarefa=None, aprovado_por=None, **kwargs):
        if tarefa is None:
            tarefa = tarefa_factory()
        if aprovado_por is None:
            aprovado_por = authenticated_user
        defaults = {
            "tarefa": tarefa,
            "valor": Decimal("200.00"),
            "aprovado_por": aprovado_por,
            "data_aprovacao": date.today() # Note: model sets auto_now_add
        }
        defaults.update(kwargs)
        ot, created = OrcamentoTarefa.objects.update_or_create(
            tarefa=defaults.pop('tarefa'), # Ensure one-to-one
            defaults=defaults
        )
        if not created and 'data_aprovacao' in defaults:
            ot.data_aprovacao = defaults['data_aprovacao']
            ot.save()
        return ot
    return create_orcamento_tarefa

@pytest.fixture
def alerta_factory(db, projeto_factory, tarefa_factory, authenticated_user):
    from costs.models import Alerta
    def create_alerta(projeto=None, tarefa=None, resolvido_por=None, **kwargs):
        if projeto is None:
            projeto = projeto_factory()
        # tarefa can be None
        # resolvido_por can be None
        defaults = {
            "tipo": "PROJETO",
            "projeto": projeto,
            "tarefa": tarefa,
            "percentual": Decimal("85.00"),
            "mensagem": "Test Alerta Mensagem",
            "status": "ATIVO",
            "resolvido_por": resolvido_por,
        }
        defaults.update(kwargs)
        return Alerta.objects.create(**defaults)
    return create_alerta