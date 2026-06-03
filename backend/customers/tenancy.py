"""Resolução do tenant da request (shared schema, sem subdomínio).

R3 (2026-06-03): com o ``django-tenants`` removido (R1), não há mais
``TenantMainMiddleware`` setando ``request.tenant`` por host/schema. O tenant da
request passa a vir da ``TenantMembership`` **ativa** do usuário autenticado.

- Usuário autenticado: tenant = ``Client`` da sua membership ativa (ou ``None``).
  Superuser não ganha tenant implícito nem bypass em rotas de negócio; a conta
  de plataforma administra o SaaS, não os dados internos dos tenants.
- Anônimo: sem tenant.
"""
from customers.models import TenantMembership

# Header legado. Mantido como constante para compatibilidade de imports, mas não
# concede mais acesso a dados de negócio de tenants.
TENANT_ID_META_KEY = 'HTTP_X_TENANT_ID'


def resolve_request_tenant(request):
    """Resolve ``(tenant, membership)`` para uma request já autenticada.

    Retorna uma tupla ``(Client | None, TenantMembership | None)``. A membership
    é devolvida para qualquer usuário autenticado com vínculo ativo; serve de
    cache para ``customers.querysets.get_request_membership``.
    """
    user = getattr(request, 'user', None)
    if not user or not user.is_authenticated:
        return None, None

    membership = (
        TenantMembership.objects
        .select_related('tenant')
        .filter(user=user, is_active=True)
        .first()
    )
    if membership is None:
        return None, None
    return membership.tenant, membership
