"""Base de testes de API para o stack multi-tenant real.

Em vez de ``force_authenticate`` (que ignora o ``PermissionMiddleware`` e o
roteamento por host), estas bases exercitam o caminho HTTP completo — o mesmo
de ``scripts/e2e_cross_tenant.py``:

    TenantMainMiddleware (resolve tenant pelo HTTP_HOST/domínio)
      -> PermissionMiddleware (exige JWT Bearer + TenantMembership ativa)
        -> RLS por papel/queryset

``TenantTestCase`` (do django_tenants) cria, uma vez por classe, um schema de
tenant próprio com domínio e migra os apps tenant nele. Cada método de teste
roda em transação revertida ao final, então usuários/memberships/dados criados
no ``setUp`` não vazam entre testes.
"""
from django.contrib.auth import get_user_model
from django_tenants.test.cases import TenantTestCase
from rest_framework.test import APIClient
from rest_framework_simplejwt.tokens import RefreshToken

from customers.models import TenantMembership

User = get_user_model()


def bearer_client(user, host):
    """APIClient roteado para ``host`` e autenticado via JWT Bearer de ``user``."""
    token = str(RefreshToken.for_user(user).access_token)
    client = APIClient(SERVER_NAME=host)
    client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
    return client


class TenantAPITestCase(TenantTestCase):
    """Usuário comum com ``TenantMembership`` ativa no tenant de teste.

    Usar para endpoints de negócio (projetos, tarefas, equipes, etc.), onde se
    quer exercitar de fato o gate de membership e o RLS por papel.
    """

    #: Papel do vínculo do usuário de teste no tenant. ``owner`` enxerga todo o
    #: tenant (leitura ampla), o que mantém os smoke tests de listagem simples.
    membership_role = TenantMembership.ROLE_OWNER

    def setUp(self):
        super().setUp()
        self.user = self.create_member(
            email='member@planify.test',
            username='member',
            full_name='Member Tester',
            role=self.membership_role,
        )
        self.client = bearer_client(self.user, self.get_test_tenant_domain())

    def create_member(self, *, email, username, full_name, role=None, password='Senha-Teste-123'):
        """Cria um usuário (schema público) com vínculo ativo no tenant atual."""
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


class SuperuserAPITestCase(TenantTestCase):
    """Superusuário autenticado via JWT.

    Superuser tem bypass do gate de tenant (mesmo critério do RLS), adequado a
    endpoints administrativos não escopados por tenant (ex.: ``/api/users/``)
    que exigem ``HasModulePermission``. Continua passando pelo middleware real
    (JWT obrigatório), diferente do antigo ``force_authenticate``.
    """

    def setUp(self):
        super().setUp()
        self.admin = User.objects.create_superuser(
            email='admin@planify.test',
            username='admin',
            full_name='Administrador',
            password='Senha-Teste-123',
        )
        self.client = bearer_client(self.admin, self.get_test_tenant_domain())
