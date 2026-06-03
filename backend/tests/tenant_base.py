"""Base de testes de API para o stack multi-tenant **shared schema** (R8).

Re-arquitetura (2026-06-03): com o ``django-tenants`` removido (R1) não há mais
schema/host por tenant. O isolamento é por ``tenant_id`` (R2), o tenant da
request vem da ``TenantMembership`` ativa do usuário (R3) e o filtro é central
(``TenantManager`` + contexto de thread), dirigido pelo ``PermissionMiddleware``
(R4). Estas bases exercitam o caminho HTTP real — o mesmo de
``scripts/e2e_r4_tenant_isolation.py``:

    PermissionMiddleware (JWT Bearer + resolve tenant pela membership + ativa o
      contexto de tenant da thread)
      -> TenantDatabaseRLSMiddleware (SET LOCAL app.current_tenant)
        -> TenantManager + apply_tenant_rls (RLS por papel sobre o tenant)

Não há ``TenantTestCase``: usa-se a ``APITestCase`` padrão (cada método roda em
transação revertida). O tenant é uma linha ``customers.Client`` comum.

**Contexto de tenant no corpo do teste.** Fora de uma request o
``TenantManager`` não filtra (e o ``pre_save`` não carimba ``tenant_id``). Para
que os ``Model.objects.create(...)`` feitos diretamente no ``setUp``/teste sejam
carimbados com o tenant e as leituras fiquem escopadas, a base **mantém o
contexto ativo** no tenant durante todo o teste. Como cada request do
``self.client`` ativa/desativa o contexto no middleware, o cliente de teste
**restaura** o escopo do tenant após cada chamada — assim criar objetos antes ou
depois de uma request funciona igual.
"""
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient, APITestCase
from rest_framework_simplejwt.tokens import RefreshToken

from customers import context
from customers.models import Client, TenantMembership

User = get_user_model()


class _ContextRestoringClient(APIClient):
    """``APIClient`` que restaura o contexto de tenant da thread após cada request.

    O ``PermissionMiddleware`` desativa o contexto em ``process_response``; sem
    isto, criar objetos de negócio no corpo do teste *após* uma chamada HTTP
    cairia fora de escopo (sem carimbo de ``tenant_id``). Restaurando o escopo,
    o teste se comporta como se estivesse continuamente dentro do tenant.
    """

    ctx_tenant_id = None
    ctx_bypass = False

    def request(self, **kwargs):
        try:
            return super().request(**kwargs)
        finally:
            context.activate(tenant_id=self.ctx_tenant_id, bypass=self.ctx_bypass)


def bearer_client(user, *, tenant_id=None, bypass=False):
    """``APIClient`` autenticado via JWT Bearer de ``user`` (sem host por tenant)."""
    token = str(RefreshToken.for_user(user).access_token)
    client = _ContextRestoringClient()
    client.ctx_tenant_id = tenant_id
    client.ctx_bypass = bypass
    client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
    return client


class TenantAPITestCase(APITestCase):
    """Usuário comum com ``TenantMembership`` ativa no tenant de teste.

    Usar para endpoints de negócio (projetos, tarefas, equipes, etc.), onde se
    quer exercitar de fato o gate de membership e o RLS por papel.
    """

    #: Papel do vínculo do usuário de teste no tenant. ``owner`` enxerga todo o
    #: tenant (leitura ampla), o que mantém os smoke tests de listagem simples.
    membership_role = TenantMembership.ROLE_OWNER

    def setUp(self):
        super().setUp()
        self.tenant = Client.objects.create(name='Tenant de Teste')
        self.user = self.create_member(
            email='member@planify.test',
            username='member',
            full_name='Member Tester',
            role=self.membership_role,
        )
        # Mantém o contexto escopado ao tenant durante o teste (carimbo no create
        # e leitura filtrada para os .objects diretos do setUp/teste).
        context.activate(tenant_id=self.tenant.id, bypass=False)
        self.addCleanup(context.deactivate)
        self.client = bearer_client(self.user, tenant_id=self.tenant.id)

    def create_member(self, *, email, username, full_name, role=None, password='Senha-Teste-123'):
        """Cria um usuário (identidade global) com vínculo ativo no tenant de teste."""
        user = User.objects.create_user(
            email=email, username=username, full_name=full_name, password=password,
        )
        TenantMembership.objects.create(
            user=user,
            tenant=self.tenant,
            role=role or self.membership_role,
            is_active=True,
        )
        return user


class SuperuserAPITestCase(APITestCase):
    """Superusuário autenticado via JWT.

    Superuser é administrador SaaS, adequado a endpoints administrativos não
    escopados por tenant (ex.: ``/api/users/``) que exigem
    ``HasModulePermission``. Rotas de negócio tenant-scoped não têm bypass:
    exigem ``TenantMembership`` como qualquer outro usuário. Continua passando
    pelo middleware real (JWT obrigatório), diferente do antigo
    ``force_authenticate``.
    """

    def setUp(self):
        super().setUp()
        self.admin = User.objects.create_superuser(
            email='admin@planify.test',
            username='admin',
            full_name='Administrador',
            password='Senha-Teste-123',
        )
        # Para asserts diretos de endpoints/plataforma fora de tenant.
        context.activate(tenant_id=None, bypass=True)
        self.addCleanup(context.deactivate)
        self.client = bearer_client(self.admin, bypass=True)
