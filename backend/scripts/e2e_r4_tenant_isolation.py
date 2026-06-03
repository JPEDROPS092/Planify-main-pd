#!/usr/bin/env python
"""E2E de isolamento por ``tenant_id`` (R4 — shared schema, sem subdomínio).

Valida o marco da R4: nenhuma query de negócio escapa do filtro por tenant. O
isolamento agora é central (``TenantManager`` + ``apply_tenant_rls``), dirigido
pelo contexto de tenant resolvido da ``TenantMembership`` ativa (o middleware
seta/limpa o contexto por request). Não há mais schema/host por tenant.

Cenário (dois tenants no mesmo schema):

    alpha  ->  alice (owner), mallory (member)
    beta   ->  bob   (owner)
    root   ->  superuser sem membership (admin SaaS; sem acesso a dados de tenant)

Dados homônimos de propósito: alpha e beta têm um projeto "Projeto Compartilhado"
(títulos iguais, tenants distintos) — só possível com o ``unique`` reescopado por
tenant (R2) e a checagem de unicidade escopada pelo manager (R4).

Asserções:
    1.  alice lista projetos -> só os de alpha (não vê o de beta)
    2.  alice detalha projeto de beta -> 404 (cross-tenant)
    3.  alice detalha o próprio projeto -> 200
    4.  bob lista -> só os de beta
    5.  mallory (member) lista -> só o projeto em que é membro (RLS por papel
        sobre o limite de tenant)
    6.  root sem membership -> 403 em API tenant-scoped
    7.  root com X-Tenant-ID legado -> continua 403 (sem bypass de negócio)
    8.  alice cria projeto com título que já existe em beta -> 201 (manager
        escopa a unicidade) e o projeto nasce carimbado com tenant=alpha
    9.  carimbo no create fora de HTTP: context.scope(beta) -> tenant=beta
    10. "filtro esquecido": Projeto.objects dentro de scope(alpha) só conta alpha

Idempotente: limpa remanescentes no início e remove tudo ao final.

Uso:  python scripts/e2e_r4_tenant_isolation.py
"""
import os
import sys
from datetime import date

import django

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'planify.settings')
django.setup()

from django.conf import settings  # noqa: E402
from django.contrib.auth import get_user_model  # noqa: E402
from django.test import Client as HttpClient  # noqa: E402

# Script standalone (fora do test-runner): o host padrão do test Client
# ('testserver') não é adicionado ao ALLOWED_HOSTS automaticamente.
if 'testserver' not in settings.ALLOWED_HOSTS:
    settings.ALLOWED_HOSTS = list(settings.ALLOWED_HOSTS) + ['testserver']
from rest_framework_simplejwt.tokens import RefreshToken  # noqa: E402

from customers import context  # noqa: E402
from customers.models import Client, TenantMembership  # noqa: E402
from projects.models import MembroProjeto, Projeto  # noqa: E402

User = get_user_model()

ALICE_EMAIL = 'alice.r4@planify.test'
BOB_EMAIL = 'bob.r4@planify.test'
MALLORY_EMAIL = 'mallory.r4@planify.test'
ROOT_EMAIL = 'root.r4@planify.test'
EMAILS = [ALICE_EMAIL, BOB_EMAIL, MALLORY_EMAIL, ROOT_EMAIL]
CLIENT_NAMES = ['R4 Alpha', 'R4 Beta']

SHARED_TITLE = 'Projeto Compartilhado'
BETA_ONLY_TITLE = 'Somente Beta'

_results = []


def check(label, condition, detail=''):
    status = 'PASS' if condition else 'FAIL'
    _results.append(bool(condition))
    suffix = f'  ({detail})' if detail else ''
    print(f'  [{status}] {label}{suffix}')
    return condition


def token_for(user):
    return str(RefreshToken.for_user(user).access_token)


def cleanup():
    # Sem contexto ativo -> manager não filtra; apagar Client cascateia os dados
    # de negócio do tenant (FK tenant CASCADE) e as memberships.
    Client.objects.filter(name__in=CLIENT_NAMES).delete()
    User.objects.filter(email__in=EMAILS).delete()


def _mk_projeto(tenant, titulo, criado_por):
    return Projeto.objects.create(
        tenant=tenant,
        titulo=titulo,
        descricao=f'{titulo} ({tenant.name})',
        data_inicio=date(2026, 1, 1),
        data_fim=date(2026, 12, 31),
        criado_por=criado_por,
    )


def setup():
    print('Setup: criando tenants alpha/beta, usuários e projetos homônimos...')
    alpha = Client.objects.create(name='R4 Alpha')
    beta = Client.objects.create(name='R4 Beta')

    alice = User.objects.create_user(
        email=ALICE_EMAIL, username='alice_r4', full_name='Alice R4', password='Senha-R4-123')
    bob = User.objects.create_user(
        email=BOB_EMAIL, username='bob_r4', full_name='Bob R4', password='Senha-R4-123')
    mallory = User.objects.create_user(
        email=MALLORY_EMAIL, username='mallory_r4', full_name='Mallory R4', password='Senha-R4-123')
    root = User.objects.create_superuser(
        email=ROOT_EMAIL, username='root_r4', full_name='Root R4', password='Senha-R4-123')

    TenantMembership.objects.create(user=alice, tenant=alpha, role=TenantMembership.ROLE_OWNER, is_active=True)
    TenantMembership.objects.create(user=bob, tenant=beta, role=TenantMembership.ROLE_OWNER, is_active=True)
    TenantMembership.objects.create(user=mallory, tenant=alpha, role=TenantMembership.ROLE_MEMBER, is_active=True)

    # alpha: a1 (sem mallory) + a2 (mallory é membro). beta: b1 com título igual a a1.
    a1 = _mk_projeto(alpha, SHARED_TITLE, alice)
    a2 = _mk_projeto(alpha, 'Projeto da Mallory', alice)
    MembroProjeto.objects.create(tenant=alpha, projeto=a2, usuario=mallory, papel='DESENVOLVEDOR')
    b1 = _mk_projeto(beta, SHARED_TITLE, bob)
    # Título que existe APENAS em beta — alvo do teste de unicidade escopada.
    _mk_projeto(beta, BETA_ONLY_TITLE, bob)

    return {
        'alpha': alpha, 'beta': beta,
        'alice': alice, 'bob': bob, 'mallory': mallory, 'root': root,
        'a1': a1.pk, 'a2': a2.pk, 'b1': b1.pk,
    }


def _ids(response):
    if response.status_code != 200:
        return []
    body = response.json()
    rows = body.get('results') if isinstance(body, dict) else body
    return [row.get('id') for row in (rows or [])]


def run_assertions(ctx):
    http = HttpClient()
    alice_t = token_for(ctx['alice'])
    bob_t = token_for(ctx['bob'])
    mallory_t = token_for(ctx['mallory'])
    root_t = token_for(ctx['root'])
    a1, a2, b1 = ctx['a1'], ctx['a2'], ctx['b1']

    def get(path, token, tenant_id=None):
        extra = {'HTTP_AUTHORIZATION': f'Bearer {token}'}
        if tenant_id is not None:
            extra['HTTP_X_TENANT_ID'] = str(tenant_id)
        return http.get(path, **extra)

    print('\n[1-3] alice (owner alpha):')
    ids = _ids(get('/api/projects/', alice_t))
    check('alice lista -> 200 e vê a1,a2', set(ids) >= {a1, a2}, f'ids={ids}')
    check('alice NÃO vê o projeto de beta (b1)', b1 not in ids, f'ids={ids}')
    check('alice detalha b1 -> 404 (cross-tenant)',
          get(f'/api/projects/{b1}/', alice_t).status_code == 404)
    check('alice detalha a1 -> 200',
          get(f'/api/projects/{a1}/', alice_t).status_code == 200)

    print('\n[4] bob (owner beta):')
    ids = _ids(get('/api/projects/', bob_t))
    check('bob lista -> só beta (b1, sem a1/a2)',
          b1 in ids and a1 not in ids and a2 not in ids, f'ids={ids}')

    print('\n[5] mallory (member alpha) — RLS por papel sobre o tenant:')
    ids = _ids(get('/api/projects/', mallory_t))
    check('mallory vê a2 (é membro)', a2 in ids, f'ids={ids}')
    check('mallory NÃO vê a1 (não é membro nem criador)', a1 not in ids, f'ids={ids}')
    check('mallory NÃO vê b1 (outro tenant)', b1 not in ids, f'ids={ids}')

    print('\n[6-7] root (superuser SaaS, sem membership):')
    resp = get('/api/projects/', root_t)
    check('root sem membership em /api/projects/ -> 403', resp.status_code == 403,
          f'status={resp.status_code}')
    resp = get('/api/projects/', root_t, tenant_id=ctx['alpha'].id)
    check('root com X-Tenant-ID legado também -> 403', resp.status_code == 403,
          f'status={resp.status_code}')

    print('\n[8] create: título duplicado entre tenants + carimbo automático:')
    resp = http.post(
        '/api/projects/',
        data={
            'titulo': BETA_ONLY_TITLE,  # existe só em beta; deve ser permitido em alpha
            'descricao': 'Criado por HTTP no tenant alpha',
            'data_inicio': '2026-02-01',
            'data_fim': '2026-11-30',
        },
        content_type='application/json',
        HTTP_AUTHORIZATION=f'Bearer {alice_t}',
    )
    created = check('alice POST título que só existe em beta -> 201 (manager escopa unicidade)',
                    resp.status_code == 201, f'status={resp.status_code} body={resp.content[:200]}')
    if created:
        new_id = resp.json().get('id')
        # Leitura fora de contexto (unscoped) para inspecionar o carimbo real.
        novo = Projeto.objects.get(pk=new_id)
        check('projeto criado carimbado com tenant=alpha',
              novo.tenant_id == ctx['alpha'].id, f'tenant_id={novo.tenant_id}')
        membro = MembroProjeto.objects.filter(projeto_id=new_id).first()
        check('MembroProjeto auto-criado também carimbado com tenant=alpha',
              membro is not None and membro.tenant_id == ctx['alpha'].id,
              f'tenant_id={getattr(membro, "tenant_id", None)}')

    print('\n[9] carimbo no create fora de HTTP (context.scope):')
    with context.scope(tenant_id=ctx['beta'].id):
        p = Projeto.objects.create(
            titulo='Projeto via scope', descricao='x',
            data_inicio=date(2026, 3, 1), data_fim=date(2026, 4, 1),
        )
    check('create dentro de scope(beta) carimba tenant=beta', p.tenant_id == ctx['beta'].id,
          f'tenant_id={p.tenant_id}')

    print('\n[10] "filtro esquecido": .objects cru dentro de scope só vê o tenant:')
    with context.scope(tenant_id=ctx['alpha'].id):
        n = Projeto.objects.filter(titulo=SHARED_TITLE).count()
    check('Projeto.objects.filter(titulo=compartilhado) em scope(alpha) conta só 1',
          n == 1, f'count={n}')


def main():
    print('=== E2E R4: isolamento por tenant_id (shared schema) ===\n')
    cleanup()
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
