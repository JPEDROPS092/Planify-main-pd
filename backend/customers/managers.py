"""Manager default com isolamento por tenant (R4).

Cada model de negócio usa ``objects = TenantManager()``. Em **runtime**, dentro de
uma request, toda query ``Model.objects...`` ganha ``WHERE tenant_id = <atual>``
automaticamente — inclusive as dezenas de chamadas ``.objects`` diretas em
dashboards, exports, validações de serializer e métodos de model que não passam
pelo ``apply_tenant_rls`` dos viewsets. É a rede que garante o filtro mesmo quando
alguém esquece de aplicá-lo à mão.

Importante (limitação conhecida): um ``queryset = Model.objects.all()`` declarado
no **nível de classe** (atributo de viewset ou ``queryset=`` de campo de
serializer) é avaliado no import, **sem** contexto, e o DRF apenas clona esse
queryset por request — ou seja, o manager **não** re-filtra esses casos. Por isso
o ``apply_tenant_rls`` aplica o ``filter(tenant=...)`` explicitamente na camada de
viewset. O manager cobre o resto (queries montadas em runtime). A garantia dura
final virá da RLS nativa do PostgreSQL na R7.

O ``_base_manager`` do Django (usado em cascade de delete, validação de forms e
resolução de FKs internas) permanece um ``Manager`` simples não-filtrado — o
Django só usa o manager filtrado como ``_default_manager``. Isso evita que o
filtro por tenant quebre operações internas do framework.
"""
from django.db import models

from customers import context


class TenantManager(models.Manager):
    """Filtra automaticamente por ``tenant_id`` segundo o contexto da request."""

    # Não serializar em migrations: o filtro é puramente de runtime.
    use_in_migrations = False

    def get_queryset(self):
        queryset = super().get_queryset()

        # Fora de request (shell, migrations, management commands, seed): sem filtro.
        if not context.is_active():
            return queryset

        # Superuser global / admin: acesso sem escopo de tenant.
        if context.is_bypass():
            return queryset

        tenant_id = context.get_tenant_id()

        # Request sem tenant resolvido (anônimo / sem membership): nega tudo.
        if tenant_id is None:
            return queryset.none()

        return queryset.filter(tenant_id=tenant_id)
