"""Permissões DRF reutilizáveis para o contexto multi-tenant.

Centraliza a regra "o usuário precisa de um vínculo (``TenantMembership``)
ativo no tenant da requisição" numa ``BasePermission`` que pode ser
declarada em qualquer viewset via ``permission_classes``.

A mesma regra é aplicada globalmente por
``users.middleware.PermissionMiddleware.check_tenant_membership`` para os
prefixos em ``settings.TENANT_MEMBERSHIP_REQUIRED_PATH_PREFIXES``. Esta
permissão é a versão escopada por view: serve como defesa-em-profundidade,
deixa a intenção explícita no próprio viewset e protege rotas que por
ventura não estejam cobertas pela lista de prefixos do middleware.

Critério de bypass é idêntico ao de ``apply_tenant_rls``/``tenant_users_queryset``:

- ``is_superuser=True``: acesso liberado (bypass operacional global);
- schema público: sem escopo de tenant, acesso liberado;
- schema de tenant: exige ``TenantMembership`` ativa em (user, tenant).
"""
from django.conf import settings
from rest_framework.permissions import BasePermission

from customers.querysets import FULL_TENANT_READ_ROLES, get_request_membership


def _is_public_schema(request):
    tenant = getattr(request, 'tenant', None)
    schema_name = getattr(tenant, 'schema_name', settings.PUBLIC_SCHEMA_NAME)
    return schema_name == settings.PUBLIC_SCHEMA_NAME


class IsTenantMember(BasePermission):
    """Exige vínculo ativo do usuário com o tenant da requisição."""

    message = 'Usuário não possui acesso a este tenant.'

    def has_permission(self, request, view):
        user = getattr(request, 'user', None)
        if not user or not user.is_authenticated:
            return False
        if user.is_superuser:
            return True
        if _is_public_schema(request):
            return True
        return get_request_membership(request) is not None


class HasTenantRole(BasePermission):
    """Exige vínculo ativo *e* um dos papéis listados em ``required_roles``.

    Uso::

        class MinhaView(APIView):
            permission_classes = [HasTenantRole.with_roles('owner', 'admin')]

    Superuser e schema público mantêm o bypass de ``IsTenantMember``.
    """

    required_roles = frozenset()
    message = 'Papel do usuário não permite esta ação neste tenant.'

    @classmethod
    def with_roles(cls, *roles):
        return type(
            'HasTenantRole_' + '_'.join(sorted(roles)),
            (cls,),
            {'required_roles': frozenset(roles)},
        )

    def has_permission(self, request, view):
        user = getattr(request, 'user', None)
        if not user or not user.is_authenticated:
            return False
        if user.is_superuser:
            return True
        if _is_public_schema(request):
            return True
        membership = get_request_membership(request)
        if membership is None:
            return False
        return membership.role in self.required_roles


class IsTenantReader(HasTenantRole):
    """Papéis com leitura ampla do tenant (owner/admin/manager/viewer)."""

    required_roles = FULL_TENANT_READ_ROLES
