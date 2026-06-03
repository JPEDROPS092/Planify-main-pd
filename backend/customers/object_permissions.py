"""Autorização a nível de objeto (escrita) sobre a base de isolamento por tenant.

A **leitura** já é escopada por papel em ``apply_tenant_rls``/``apply_member_rls``
(``customers.querysets``): o queryset de cada viewset só devolve o que o papel pode
ver. Este módulo trata a **escrita por objeto** — quem pode *modificar/excluir* uma
instância específica que já passou pelo filtro de tenant e de leitura:

- ``owner``/``admin``/``manager``: escrita plena dentro do tenant.
- ``viewer``: somente leitura (nenhuma escrita, nem create).
- ``member``: escreve apenas os **próprios recursos** (criados/atribuídos a ele),
  não qualquer objeto do projeto que ele consegue *ler*.

Motivação: hoje ``get_object()`` usa o queryset de leitura, então um ``member``
conseguiria editar/excluir qualquer objeto que ele *enxerga* — por exemplo, uma
tarefa do projeto que não foi atribuída a ele. A leitura é ampla de propósito
(colaboração); a escrita precisa ser estreita (responsabilidade).

Plugado centralmente em ``TenantRLSQuerysetMixin.get_permissions`` — todo viewset
de negócio ganha a checagem sem alteração caso a caso. O DRF chama
``check_object_permissions`` dentro de ``get_object()``, então ``retrieve``,
``update``, ``partial_update``, ``destroy`` e as ``@action`` de detalhe (que chamam
``self.get_object()``) ficam cobertos. ``has_permission`` corta create/update/delete
de ``viewer`` já na coleção, antes de tocar o banco.

Os lookups de "recurso próprio" abaixo são um subconjunto estreito dos já usados em
``apply_member_rls`` para leitura — reaproveitam os mesmos nomes de campo/relacão,
então permanecem válidos junto com aquele mapa (única fonte das relações por model).
"""
from rest_framework.permissions import SAFE_METHODS, BasePermission

from customers.querysets import get_request_membership

# Papéis com escrita plena dentro do tenant (o objeto já vem escopado por tenant).
FULL_TENANT_WRITE_ROLES = frozenset({'owner', 'admin', 'manager'})
MEMBER_ROLE = 'member'


def _member_write_filters(user):
    """``model_label -> Q`` que define os objetos que um ``member`` pode escrever.

    Estreito por design: apenas recursos de que o usuário é dono (criou, foi
    atribuído, é autor/responsável). Models ausentes do mapa => escrita negada
    para ``member`` (ex.: ``costs.categoria``, dado de referência compartilhado).
    """
    from django.db.models import Q

    return {
        'projects.projeto': Q(criado_por=user),
        'projects.membroprojeto': Q(usuario=user) | Q(projeto__criado_por=user),
        'projects.historicostatusprojeto': Q(projeto__criado_por=user),
        'projects.sprint': Q(criado_por=user),

        'tasks.tarefa': Q(criado_por=user) | Q(atribuicoes__usuario=user),
        'tasks.atribuicaotarefa': Q(usuario=user) | Q(atribuido_por=user),
        'tasks.comentariotarefa': Q(autor=user),
        'tasks.historicostatustarefa': Q(alterado_por=user),

        'teams.equipe': Q(criado_por=user),
        'teams.membroequipe': Q(usuario=user) | Q(equipe__criado_por=user),
        'teams.permissaoequipe': Q(equipe__criado_por=user),

        'risks.risco': Q(criado_por=user) | Q(responsavel_mitigacao=user),
        'risks.historicorisco': Q(alterado_por=user),

        'costs.custo': Q(criado_por=user),
        'costs.orcamentoprojeto': Q(aprovado_por=user) | Q(projeto__criado_por=user),
        'costs.orcamentotarefa': Q(aprovado_por=user),
        'costs.alerta': Q(resolvido_por=user),

        'documents.documento': Q(enviado_por=user),
        'documents.historicodocumento': Q(alterado_por=user),
        'documents.comentario': Q(autor=user),

        'communications.chatmensagem': Q(autor=user),
        'communications.chatmensagemleitura': Q(usuario=user),
        'communications.notificacao': Q(usuario=user),
        'communications.configuracaonotificacao': Q(usuario=user),
        'communications.comunicacao': Q(remetente=user),
    }


def member_can_write_object(user, obj):
    """``True`` se um ``member`` pode modificar/excluir ``obj`` (recurso próprio).

    Avalia o ``Q`` de propriedade contra a própria linha. ``obj`` já passou pelo
    filtro de tenant/leitura, então ``.objects`` (TenantManager, escopado pelo
    contexto da request) só confirma a relação de posse — sem vazar cross-tenant.
    """
    write_filter = _member_write_filters(user).get(obj._meta.label_lower)
    if write_filter is None:
        return False
    model = type(obj)
    return model.objects.filter(pk=obj.pk).filter(write_filter).exists()


class TenantObjectWritePermission(BasePermission):
    """Escrita por objeto por papel, sobre a base de isolamento por tenant.

    Leitura (``SAFE_METHODS``) é liberada aqui — quem pode ler já foi decidido pelo
    queryset escopado. As escritas é que afunilam por papel.
    """

    message = 'Seu papel não permite modificar este recurso.'

    def has_permission(self, request, view):
        # Leitura segue o gate de membership/queryset; aqui só barramos escrita.
        if request.method in SAFE_METHODS:
            return True
        membership = get_request_membership(request)
        if membership is None:
            return False
        # ``viewer`` (e papéis fora do conjunto de escrita) é somente-leitura,
        # inclusive create (POST na coleção, que não dispara has_object_permission).
        return (
            membership.role in FULL_TENANT_WRITE_ROLES
            or membership.role == MEMBER_ROLE
        )

    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        membership = get_request_membership(request)
        if membership is None:
            return False
        if membership.role in FULL_TENANT_WRITE_ROLES:
            return True
        if membership.role == MEMBER_ROLE:
            return member_can_write_object(request.user, obj)
        return False  # viewer e demais: somente leitura
