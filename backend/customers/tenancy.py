"""Resolução do tenant da request (shared schema, sem subdomínio).

R3 (2026-06-03): com o ``django-tenants`` removido (R1), não há mais
``TenantMainMiddleware`` setando ``request.tenant`` por host/schema. O tenant da
request passa a vir da ``TenantMembership`` **ativa** do usuário autenticado.

- Usuário normal: tenant = ``Client`` da sua membership ativa (ou ``None``).
- Superuser: informa o tenant **explicitamente** via header ``X-Tenant-ID``
  (ou query param ``tenant``) para operação escopada; sem isso, opera global
  (sem tenant — o bypass de superuser em ``apply_tenant_rls`` libera tudo).
- Anônimo: sem tenant.
"""
from customers.models import Client, TenantMembership

# Header HTTP (forma WSGI/META) usado pelo superuser para escopar a operação.
TENANT_ID_META_KEY = 'HTTP_X_TENANT_ID'


def resolve_request_tenant(request):
    """Resolve ``(tenant, membership)`` para uma request já autenticada.

    Retorna uma tupla ``(Client | None, TenantMembership | None)``. A membership
    só é devolvida para usuário normal (superuser não tem vínculo); serve de
    cache para ``customers.querysets.get_request_membership``.
    """
    user = getattr(request, 'user', None)
    if not user or not user.is_authenticated:
        return None, None

    if user.is_superuser:
        return _explicit_tenant(request), None

    membership = (
        TenantMembership.objects
        .select_related('tenant')
        .filter(user=user, is_active=True)
        .first()
    )
    if membership is None:
        return None, None
    return membership.tenant, membership


def _explicit_tenant(request):
    """Tenant informado explicitamente pelo superuser (header ou query param)."""
    raw = request.META.get(TENANT_ID_META_KEY) or request.GET.get('tenant')
    if not raw:
        return None
    try:
        tenant_id = int(raw)
    except (TypeError, ValueError):
        return None
    return Client.objects.filter(pk=tenant_id).first()
