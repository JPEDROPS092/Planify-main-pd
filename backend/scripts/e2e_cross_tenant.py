#!/usr/bin/env python
"""Teste ponta-a-ponta de isolamento entre tenants (negação cross-tenant).

Exercita o stack HTTP REAL — TenantMainMiddleware (roteamento por host) +
JWT + PermissionMiddleware.check_tenant_membership + RLS por schema — usando
o ``django.test.Client`` com ``HTTP_HOST`` apontando para o domínio de cada
tenant e ``Authorization: Bearer`` com token de cada usuário.

Cenário (dois tenants reais, schemas separados):

    alpha  ->  domínio e2e-alpha.localhost  ->  usuária alice (owner)
    beta   ->  domínio e2e-beta.localhost   ->  usuário  bob   (owner)

Asserções:
    1. alice@alpha  GET /api/projects/         -> 200 e vê o projeto de alpha
    2. alice@alpha  GET /api/projects/<pk>/    -> 200
    3. alice@beta   GET /api/projects/         -> 403 (sem vínculo no tenant)
    4. alice@beta   GET /api/projects/<pk>/    -> 403 (negada antes do schema)
    5. bob@beta     GET /api/projects/         -> 200, lista NÃO contém o
                                                  projeto de alpha (isolamento)
    6. bob@beta     GET /api/projects/<pk>/    -> 404 (objeto inexistente no
                                                  schema beta)
    7. alice@beta   GET /api/teams/...usuarios_disponiveis -> 403

É idempotente: limpa tenants/usuários de teste remanescentes no início e
remove tudo o que cria ao final (drop dos schemas inclusive).

Uso:
    python scripts/e2e_cross_tenant.py
"""
import os
import sys
from datetime import date

import django

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'planify.settings')
django.setup()

from django.contrib.auth import get_user_model  # noqa: E402
from django.db import connection  # noqa: E402
from django.test import Client as HttpClient  # noqa: E402
from django_tenants.utils import schema_context  # noqa: E402
from rest_framework_simplejwt.tokens import RefreshToken  # noqa: E402

from customers.models import Client, Domain, TenantMembership  # noqa: E402
from projects.models import Projeto  # noqa: E402

User = get_user_model()

ALPHA_SCHEMA = 'e2e_alpha'
BETA_SCHEMA = 'e2e_beta'
ALPHA_DOMAIN = 'e2e-alpha.localhost'
BETA_DOMAIN = 'e2e-beta.localhost'
ALICE_EMAIL = 'alice.e2e@planify.test'
BOB_EMAIL = 'bob.e2e@planify.test'

# Contadores de resultado
_results = []


def check(label, condition, detail=''):
    status = 'PASS' if condition else 'FAIL'
    _results.append(condition)
    suffix = f'  ({detail})' if detail else ''
    print(f'  [{status}] {label}{suffix}')
    return condition


def token_for(user):
    return str(RefreshToken.for_user(user).access_token)


def drop_tenant(schema_name):
    """Remove tenant + schema + domínios + memberships de testes anteriores."""
    for tenant in Client.objects.filter(schema_name=schema_name):
        tenant.auto_drop_schema = True
        tenant.delete(force_drop=True)


def cleanup():
    # O test Client deixa a conexão no schema do último host acessado;
    # django_tenants só permite dropar tenant a partir do schema público.
    connection.set_schema_to_public()
    drop_tenant(ALPHA_SCHEMA)
    drop_tenant(BETA_SCHEMA)
    # Garante que nenhum schema órfão fique para trás (drop dos tenants acima
    # já remove, mas isto cobre execuções interrompidas no meio).
    with connection.cursor() as cur:
        cur.execute('DROP SCHEMA IF EXISTS %s CASCADE' % ALPHA_SCHEMA)
        cur.execute('DROP SCHEMA IF EXISTS %s CASCADE' % BETA_SCHEMA)
    # Remoção dos usuários via SQL: deletar User (shared) pelo ORM dispara o
    # collector de cascata, que consulta tabelas de apps-tenant
    # (ex.: projects_membroprojeto) no schema público — onde não existem.
    # Com os schemas de tenant já dropados, não restam FKs apontando para
    # estes usuários, então o DELETE direto é seguro.
    with connection.cursor() as cur:
        cur.execute(
            'DELETE FROM users_user WHERE email = ANY(%s)',
            [[ALICE_EMAIL, BOB_EMAIL]],
        )


def make_tenant(schema_name, name, domain_name):
    tenant = Client(schema_name=schema_name, name=name)
    tenant.auto_create_schema = True
    tenant.save()
    Domain.objects.create(tenant=tenant, domain=domain_name, is_primary=True)
    return tenant


def setup():
    print('Setup: criando tenants alpha/beta e usuários...')
    alpha = make_tenant(ALPHA_SCHEMA, 'E2E Alpha', ALPHA_DOMAIN)
    beta = make_tenant(BETA_SCHEMA, 'E2E Beta', BETA_DOMAIN)

    alice = User.objects.create_user(
        email=ALICE_EMAIL, username='alice_e2e', full_name='Alice E2E',
        password='Senha-E2E-123',
    )
    bob = User.objects.create_user(
        email=BOB_EMAIL, username='bob_e2e', full_name='Bob E2E',
        password='Senha-E2E-123',
    )

    TenantMembership.objects.create(
        user=alice, tenant=alpha, role=TenantMembership.ROLE_OWNER, is_active=True,
    )
    TenantMembership.objects.create(
        user=bob, tenant=beta, role=TenantMembership.ROLE_OWNER, is_active=True,
    )

    # Cria um projeto APENAS no schema alpha, de autoria da alice.
    with schema_context(ALPHA_SCHEMA):
        projeto = Projeto.objects.create(
            titulo='Projeto Secreto Alpha',
            descricao='Visível apenas dentro do tenant alpha.',
            data_inicio=date(2026, 1, 1),
            data_fim=date(2026, 12, 31),
            criado_por=alice,
        )
        alpha_pk = projeto.pk

    return {'alice': alice, 'bob': bob, 'alpha_pk': alpha_pk}


def run_assertions(ctx):
    http = HttpClient()
    alice_tok = token_for(ctx['alice'])
    bob_tok = token_for(ctx['bob'])
    pk = ctx['alpha_pk']

    def get(path, host, token):
        return http.get(
            path, HTTP_HOST=host, HTTP_AUTHORIZATION=f'Bearer {token}',
        )

    print('\nAsserções de acesso legítimo (alice no próprio tenant alpha):')
    r = get('/api/projects/', ALPHA_DOMAIN, alice_tok)
    body = r.json() if r.status_code == 200 else {}
    titulos = [p.get('titulo') for p in (body.get('results') or body if isinstance(body, (list, dict)) else [])] \
        if r.status_code == 200 else []
    check('alice@alpha lista projetos -> 200', r.status_code == 200, f'status={r.status_code}')
    check('alice@alpha vê "Projeto Secreto Alpha"', 'Projeto Secreto Alpha' in titulos, f'titulos={titulos}')

    r = get(f'/api/projects/{pk}/', ALPHA_DOMAIN, alice_tok)
    check('alice@alpha detalha o projeto -> 200', r.status_code == 200, f'status={r.status_code}')

    print('\nAsserções de NEGAÇÃO cross-tenant (alice tentando o tenant beta):')
    r = get('/api/projects/', BETA_DOMAIN, alice_tok)
    check('alice@beta lista projetos -> 403', r.status_code == 403, f'status={r.status_code}')

    r = get(f'/api/projects/{pk}/', BETA_DOMAIN, alice_tok)
    check('alice@beta detalha projeto de alpha -> 403', r.status_code == 403, f'status={r.status_code}')

    r = get('/api/teams/usuarios_disponiveis/', BETA_DOMAIN, alice_tok)
    check('alice@beta acessa endpoint de teams -> 403', r.status_code == 403, f'status={r.status_code}')

    print('\nAsserções de ISOLAMENTO por schema (bob no próprio tenant beta):')
    r = get('/api/projects/', BETA_DOMAIN, bob_tok)
    ok_status = r.status_code == 200
    body = r.json() if ok_status else {}
    titulos_beta = [p.get('titulo') for p in (body.get('results') if isinstance(body, dict) else body)] \
        if ok_status else []
    check('bob@beta lista projetos -> 200', ok_status, f'status={r.status_code}')
    check('bob@beta NÃO vê projeto de alpha (isolamento)',
          'Projeto Secreto Alpha' not in titulos_beta, f'titulos={titulos_beta}')

    r = get(f'/api/projects/{pk}/', BETA_DOMAIN, bob_tok)
    check('bob@beta detalha pk de alpha -> 404 (inexistente no schema)',
          r.status_code == 404, f'status={r.status_code}')


def main():
    print('=== E2E cross-tenant isolation ===\n')
    cleanup()  # limpa remanescentes de execuções anteriores
    try:
        ctx = setup()
        run_assertions(ctx)
    finally:
        print('\nTeardown: removendo tenants/usuários de teste...')
        cleanup()

    total = len(_results)
    passed = sum(1 for r in _results if r)
    print(f'\n=== Resultado: {passed}/{total} asserções OK ===')
    if passed != total:
        sys.exit(1)


if __name__ == '__main__':
    main()
