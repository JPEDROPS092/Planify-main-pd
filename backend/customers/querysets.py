from django.core.exceptions import FieldDoesNotExist
from django.db.models import Q


FULL_TENANT_READ_ROLES = {'owner', 'admin', 'manager', 'viewer'}
LIMITED_TENANT_READ_ROLES = {'member'}

_UNSET = object()


def get_request_membership(request):
    # R3: usa o cache populado por PermissionMiddleware._set_request_tenant
    # (request._tenant_membership) quando disponível, evitando reconsulta.
    cached = getattr(request, '_tenant_membership', _UNSET)
    if cached is not _UNSET:
        return cached

    tenant = getattr(request, 'tenant', None)
    if tenant is None:
        return None

    if not getattr(request, 'user', None) or not request.user.is_authenticated:
        return None

    from customers.models import TenantMembership

    return TenantMembership.objects.filter(
        user=request.user,
        tenant=tenant,
        is_active=True,
    ).first()


def tenant_users_queryset(request, base_queryset=None):
    """Usuários (model público) com vínculo ativo no tenant atual.

    Mantém o mesmo critério de ``apply_tenant_rls``:

    - sem tenant resolvido: nenhum usuário (``none()``).
    - com tenant: apenas usuários com ``TenantMembership`` ativa no tenant.

    Evita enumeração cross-tenant em endpoints que listam ou resolvem usuários,
    já que ``users.User`` é compartilhado (schema único).
    """
    from django.contrib.auth import get_user_model

    User = get_user_model()
    queryset = base_queryset if base_queryset is not None else User.objects.all()

    tenant = getattr(request, 'tenant', None)
    if tenant is None:
        return queryset.none()

    from customers.models import TenantMembership

    member_ids = TenantMembership.objects.filter(
        tenant=tenant,
        is_active=True,
    ).values_list('user_id', flat=True)
    return queryset.filter(id__in=member_ids)


def _has_tenant_field(model):
    try:
        model._meta.get_field('tenant')
        return True
    except FieldDoesNotExist:
        return False


def _scope_to_tenant(queryset, tenant):
    """Aplica o limite duro ``WHERE tenant_id = X`` quando o model tem ``tenant``.

    O ``TenantManager`` já escopa as queries montadas em runtime, mas os viewsets
    usam ``queryset = Model.objects.all()`` de nível de classe (avaliado no import,
    sem contexto) e o DRF apenas clona esse queryset por request — então o manager
    não re-filtra esse caminho. Aqui garantimos o filtro de tenant explicitamente.
    """
    if tenant is not None and _has_tenant_field(queryset.model):
        return queryset.filter(tenant=tenant)
    return queryset


def apply_tenant_rls(queryset, request):
    user = getattr(request, 'user', None)
    tenant = getattr(request, 'tenant', None)

    if tenant is None:
        return queryset.none()

    # Limite duro de tenant antes de qualquer narrowing por papel.
    queryset = _scope_to_tenant(queryset, tenant)

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
