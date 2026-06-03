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

Critério é idêntico ao de ``apply_tenant_rls``/``tenant_users_queryset``:

- usuários exigem ``TenantMembership`` ativa no tenant da request (R3:
  o tenant é resolvido pela membership ativa do usuário);
- superuser não tem bypass nas rotas de negócio tenant-scoped. A administração
  de plataforma fica em `/admin/` e comandos de gestão.
"""
from rest_framework.permissions import BasePermission

from customers.querysets import FULL_TENANT_READ_ROLES, get_request_membership


class IsTenantMember(BasePermission):
    """Exige vínculo ativo do usuário com o tenant da requisição."""

    message = 'Usuário não possui acesso a este tenant.'

    def has_permission(self, request, view):
        user = getattr(request, 'user', None)
        if not user or not user.is_authenticated:
            return False
        return get_request_membership(request) is not None


class HasTenantRole(BasePermission):
    """Exige vínculo ativo *e* um dos papéis listados em ``required_roles``.

    Uso::

        class MinhaView(APIView):
            permission_classes = [HasTenantRole.with_roles('owner', 'admin')]

    Superuser segue a mesma regra: precisa de membership e papel no tenant.
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
        membership = get_request_membership(request)
        if membership is None:
            return False
        return membership.role in self.required_roles


class IsTenantReader(HasTenantRole):
    """Papéis com leitura ampla do tenant (owner/admin/manager/viewer)."""

    required_roles = FULL_TENANT_READ_ROLES
