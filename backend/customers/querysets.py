from django.conf import settings
from django.db.models import Q


FULL_TENANT_READ_ROLES = {'owner', 'admin', 'manager', 'viewer'}
LIMITED_TENANT_READ_ROLES = {'member'}


def get_request_membership(request):
    tenant = getattr(request, 'tenant', None)
    schema_name = getattr(tenant, 'schema_name', settings.PUBLIC_SCHEMA_NAME)

    if schema_name == settings.PUBLIC_SCHEMA_NAME:
        return None

    if not request.user or not request.user.is_authenticated:
        return None

    from customers.models import TenantMembership

    return TenantMembership.objects.filter(
        user=request.user,
        tenant=tenant,
        is_active=True,
    ).first()


def tenant_users_queryset(request, base_queryset=None):
    """Usuários (model público) com vínculo ativo no tenant atual.

    Mantém o mesmo critério de bypass de ``apply_tenant_rls``:

    - ``is_superuser=True``: todos os usuários (bypass operacional global).
    - schema público: todos os usuários (sem escopo de tenant).
    - schema tenant: apenas usuários com ``TenantMembership`` ativa no tenant.

    Evita enumeração cross-tenant em endpoints que listam ou resolvem usuários,
    já que ``users.User`` vive no schema ``public`` e é compartilhado.
    """
    from django.contrib.auth import get_user_model

    User = get_user_model()
    queryset = base_queryset if base_queryset is not None else User.objects.all()

    if getattr(request, 'user', None) and request.user.is_superuser:
        return queryset

    tenant = getattr(request, 'tenant', None)
    schema_name = getattr(tenant, 'schema_name', settings.PUBLIC_SCHEMA_NAME)
    if schema_name == settings.PUBLIC_SCHEMA_NAME:
        return queryset

    from customers.models import TenantMembership

    member_ids = TenantMembership.objects.filter(
        tenant=tenant,
        is_active=True,
    ).values_list('user_id', flat=True)
    return queryset.filter(id__in=member_ids)


def apply_tenant_rls(queryset, request):
    if getattr(request, 'user', None) and request.user.is_superuser:
        return queryset

    tenant = getattr(request, 'tenant', None)
    schema_name = getattr(tenant, 'schema_name', settings.PUBLIC_SCHEMA_NAME)
    if schema_name == settings.PUBLIC_SCHEMA_NAME:
        return queryset

    membership = get_request_membership(request)
    if membership is None:
        return queryset.none()

    if membership.role in FULL_TENANT_READ_ROLES:
        return queryset

    if membership.role not in LIMITED_TENANT_READ_ROLES:
        return queryset.none()

    return apply_member_rls(queryset, request.user)


def apply_member_rls(queryset, user):
    model_label = queryset.model._meta.label_lower

    filters = {
        'projects.projeto': Q(criado_por=user) | Q(membros__usuario=user),
        'projects.membroprojeto': Q(usuario=user) | Q(projeto__membros__usuario=user),
        'projects.historicostatusprojeto': Q(projeto__criado_por=user) | Q(projeto__membros__usuario=user),
        'projects.sprint': Q(criado_por=user) | Q(projeto__membros__usuario=user),

        'tasks.tarefa': Q(criado_por=user) | Q(atualizado_por=user) | Q(atribuicoes__usuario=user) | Q(projeto__membros__usuario=user),
        'tasks.atribuicaotarefa': Q(usuario=user) | Q(atribuido_por=user) | Q(tarefa__projeto__membros__usuario=user),
        'tasks.comentariotarefa': Q(autor=user) | Q(tarefa__projeto__membros__usuario=user),
        'tasks.historicostatustarefa': Q(alterado_por=user) | Q(tarefa__projeto__membros__usuario=user),

        'teams.equipe': Q(criado_por=user) | Q(membros__usuario=user),
        'teams.membroequipe': Q(usuario=user) | Q(equipe__membros__usuario=user),
        'teams.permissaoequipe': Q(equipe__membros__usuario=user),

        'risks.risco': Q(criado_por=user) | Q(responsavel_mitigacao=user) | Q(projeto__membros__usuario=user),
        'risks.historicorisco': Q(alterado_por=user) | Q(risco__projeto__membros__usuario=user),

        'costs.categoria': Q(),
        'costs.custo': Q(criado_por=user) | Q(projeto__membros__usuario=user) | Q(tarefa__atribuicoes__usuario=user),
        'costs.orcamentoprojeto': Q(aprovado_por=user) | Q(projeto__membros__usuario=user),
        'costs.orcamentotarefa': Q(aprovado_por=user) | Q(tarefa__projeto__membros__usuario=user) | Q(tarefa__atribuicoes__usuario=user),
        'costs.alerta': Q(resolvido_por=user) | Q(projeto__membros__usuario=user) | Q(tarefa__atribuicoes__usuario=user),

        'documents.documento': Q(enviado_por=user) | Q(projeto__membros__usuario=user) | Q(tarefa__atribuicoes__usuario=user),
        'documents.historicodocumento': Q(alterado_por=user) | Q(documento__projeto__membros__usuario=user),
        'documents.comentario': Q(autor=user) | Q(documento__projeto__membros__usuario=user),

        'communications.chatmensagem': Q(autor=user) | Q(projeto__membros__usuario=user),
        'communications.chatmensagemleitura': Q(usuario=user) | Q(mensagem__projeto__membros__usuario=user),
        'communications.notificacao': Q(usuario=user),
        'communications.configuracaonotificacao': Q(usuario=user),
        'communications.comunicacao': Q(remetente=user) | Q(destinatarios=user) | Q(projeto__membros__usuario=user),
    }

    rls_filter = filters.get(model_label)
    if rls_filter is None:
        return queryset.none()

    return queryset.filter(rls_filter).distinct()


class TenantRLSQuerysetMixin:
    def apply_rls(self, queryset):
        return apply_tenant_rls(queryset, self.request)

    def get_queryset(self):
        return self.apply_rls(super().get_queryset())
