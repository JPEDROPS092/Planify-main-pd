"""Ponte entre o contexto de tenant da app (R4) e a RLS nativa do banco (R7).

Cada request roda numa transação onde a GUC de sessão ``app.current_tenant`` é
setada (``SET LOCAL``, escopo de transação) a partir do mesmo contexto que dirige
o ``TenantManager``. As policies do PostgreSQL (migração ``customers/0006``) leem
essa GUC para filtrar/checar as linhas — a garantia dura, independente da app.

Valores da GUC (espelham o contexto):

- bypass administrativo (``/admin/``/ferramentas internas) -> ``''`` (todas as
  linhas).
- tenant resolvido                        -> ``str(tenant_id)``.
- sem tenant / contexto inativo           -> ``'-1'`` (nenhuma linha; fail-closed).

Só tem efeito real quando a conexão é uma role sem ``BYPASSRLS`` (``app_user``);
sob ``planify`` (superuser) o ``SET`` é inócuo (superuser ignora RLS).
"""
from django.db import connection, transaction

from customers import context

GUC_KEY = 'app.current_tenant'
DENY = '-1'


def current_guc_value():
    if not context.is_active():
        return DENY
    if context.is_bypass():
        return ''
    tenant_id = context.get_tenant_id()
    return str(tenant_id) if tenant_id is not None else DENY


class TenantDatabaseRLSMiddleware:
    """Seta ``app.current_tenant`` por request, dentro de uma transação.

    Deve ficar **depois** de ``users.middleware.PermissionMiddleware`` no
    ``MIDDLEWARE`` (que resolve o tenant e ativa o contexto antes daqui).
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        value = current_guc_value()
        with transaction.atomic():
            with connection.cursor() as cursor:
                # SET LOCAL: vale só nesta transação; as queries da view rodam aqui.
                cursor.execute("SELECT set_config(%s, %s, true)", [GUC_KEY, value])
            return self.get_response(request)
