"""Contexto de tenant da request (R4 — isolamento centralizado).

Guarda, por thread, o tenant ativo da request corrente. O ``TenantManager``
(ver ``customers.managers``) consulta este contexto para injetar
``WHERE tenant_id = <atual>`` automaticamente em **toda** query ``.objects`` de
runtime, sem que cada call site precise lembrar de filtrar.

Estados do contexto:

- **inativo** (``is_active() is False``): fora de uma request — shell, management
  commands, migrations, seed. O manager **não filtra** (comportamento normal do
  Django), para não quebrar essas operações.
- **ativo, ``bypass=True``**: superuser operando global ou ``/admin/`` — o manager
  não filtra (acesso global controlado).
- **ativo, ``tenant_id`` setado**: usuário normal (ou superuser com tenant
  explícito) — o manager filtra por esse ``tenant_id``.
- **ativo, ``tenant_id is None`` e ``bypass=False``**: request sem tenant resolvido
  (anônimo / sem membership) — o manager devolve ``none()`` (deny-by-default).

O ciclo (ativar no início da request / desativar no fim) é responsabilidade do
``users.middleware.PermissionMiddleware``. Fora de requests, use o context
manager ``scope()`` para escopar explicitamente (testes, scripts, R6).
"""
import threading
from contextlib import contextmanager

_state = threading.local()


def activate(tenant_id=None, bypass=False):
    """Ativa o contexto da thread corrente com o tenant resolvido."""
    _state.active = True
    _state.tenant_id = tenant_id
    _state.bypass = bypass


def deactivate():
    """Desativa o contexto (volta ao modo "sem filtro" fora de request)."""
    _state.active = False
    _state.tenant_id = None
    _state.bypass = False


def is_active():
    return getattr(_state, 'active', False)


def get_tenant_id():
    return getattr(_state, 'tenant_id', None)


def is_bypass():
    return getattr(_state, 'bypass', False)


@contextmanager
def scope(tenant_id=None, bypass=False):
    """Escopa um bloco a um tenant (ou bypass), restaurando o estado anterior.

    Útil em scripts, seed e testes, onde não há middleware setando o contexto::

        with scope(tenant_id=cliente.id):
            Projeto.objects.create(...)  # carimbado e filtrado por esse tenant
    """
    prev = (
        getattr(_state, 'active', False),
        getattr(_state, 'tenant_id', None),
        getattr(_state, 'bypass', False),
    )
    activate(tenant_id=tenant_id, bypass=bypass)
    try:
        yield
    finally:
        _state.active, _state.tenant_id, _state.bypass = prev
