#!/usr/bin/env python
"""E2E da RLS nativa do PostgreSQL (R7) — a garantia no nível do banco.

Conecta como ``app_user`` (role sem ``BYPASSRLS``, não-superuser) e prova que o
PostgreSQL filtra/checa por ``tenant_id`` mesmo numa query **crua** (sem WHERE),
a partir da GUC ``app.current_tenant`` — independente da camada de aplicação.

Cenário: dois tenants (A, B), cada um com um projeto, criados via ORM (conexão
``planify``, superuser, que ignora RLS no setup). Depois, como ``app_user``:

    1. GUC = A   -> SELECT projects_projeto vê só o projeto de A (não o de B)
    2. GUC = B   -> vê só o de B
    3. GUC = ''  -> vê os dois (bypass administrativo interno)
    4. GUC = -1  -> não vê nada (deny-by-default)
    5. GUC ausente (sessão nova) -> não vê nada (fail-closed)
    6. GUC = A, UPDATE movendo o projeto de A para tenant B -> bloqueado (WITH CHECK)

Pré-requisito: ``manage.py migrate`` (policies) e ``manage.py setup_rls`` (cria a
role ``app_user``). Idempotente: cria e remove os tenants de teste.

Uso:  python scripts/e2e_r7_native_rls.py
"""
import os
import sys
from datetime import date

import django

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'planify.settings')
django.setup()

import psycopg  # noqa: E402
from django.conf import settings as dj_settings  # noqa: E402

from customers.models import Client  # noqa: E402
from projects.models import Projeto  # noqa: E402

CLIENT_NAMES = ['R7 A', 'R7 B']
_results = []


def check(label, condition, detail=''):
    status = 'PASS' if condition else 'FAIL'
    _results.append(bool(condition))
    suffix = f'  ({detail})' if detail else ''
    print(f'  [{status}] {label}{suffix}')
    return condition


def cleanup():
    Client.objects.filter(name__in=CLIENT_NAMES).delete()


def setup():
    a = Client.objects.create(name='R7 A')
    b = Client.objects.create(name='R7 B')
    pa = Projeto.objects.create(
        tenant=a, titulo='Projeto A (R7)', descricao='x',
        data_inicio=date(2026, 1, 1), data_fim=date(2026, 12, 31))
    pb = Projeto.objects.create(
        tenant=b, titulo='Projeto B (R7)', descricao='x',
        data_inicio=date(2026, 1, 1), data_fim=date(2026, 12, 31))
    return a, b, pa.pk, pb.pk


def app_user_conn():
    db = dj_settings.DATABASES['default']
    return psycopg.connect(
        host=db.get('HOST') or '127.0.0.1',
        port=db.get('PORT') or '5432',
        dbname=db['NAME'],
        user=os.environ.get('APP_DB_USER', 'app_user'),
        password=os.environ.get('APP_DB_PASSWORD', 'app_user'),
        autocommit=True,
    )


def visible_ids(conn, guc):
    """IDs de projects_projeto visíveis com a GUC dada (None = não setar)."""
    with conn.cursor() as cur:
        if guc is not None:
            cur.execute("SELECT set_config('app.current_tenant', %s, false)", [guc])
        cur.execute('SELECT id FROM projects_projeto ORDER BY id')
        return [r[0] for r in cur.fetchall()]


def run():
    a, b, pa, pb = setup()
    conn = app_user_conn()
    try:
        print('\n[1-2] Isolamento por GUC (app_user, query crua sem WHERE):')
        ids_a = visible_ids(conn, str(a.id))
        check('GUC=A vê o projeto de A', pa in ids_a, f'ids={ids_a}')
        check('GUC=A NÃO vê o projeto de B', pb not in ids_a, f'ids={ids_a}')
        ids_b = visible_ids(conn, str(b.id))
        check('GUC=B vê só o de B', pb in ids_b and pa not in ids_b, f'ids={ids_b}')

        print('\n[3-4] Bypass e deny:')
        ids_all = visible_ids(conn, '')
        check("GUC='' (global) vê A e B", pa in ids_all and pb in ids_all, f'ids={ids_all}')
        ids_deny = visible_ids(conn, '-1')
        check('GUC=-1 não vê nada', pa not in ids_deny and pb not in ids_deny, f'ids={ids_deny}')

        print('\n[5] Fail-closed (sessão nova, GUC nunca setada):')
        fresh = app_user_conn()
        try:
            ids_fresh = visible_ids(fresh, None)
            check('sem GUC -> nenhuma linha (fail-closed)',
                  pa not in ids_fresh and pb not in ids_fresh, f'ids={ids_fresh}')
        finally:
            fresh.close()

        print('\n[6] WITH CHECK no UPDATE (mover linha para outro tenant):')
        blocked = False
        try:
            with conn.cursor() as cur:
                cur.execute("SELECT set_config('app.current_tenant', %s, false)", [str(a.id)])
                cur.execute('UPDATE projects_projeto SET tenant_id = %s WHERE id = %s', [b.id, pa])
        except psycopg.errors.Error:
            blocked = True
        check('GUC=A: mover projeto de A para B -> bloqueado (WITH CHECK)', blocked)
    finally:
        conn.close()


def main():
    print('=== E2E R7: RLS nativa do PostgreSQL (conectando como app_user) ===')
    cleanup()
    try:
        run()
    finally:
        print('\nTeardown: removendo tenants de teste...')
        cleanup()

    total = len(_results)
    passed = sum(1 for r in _results if r)
    print(f'\n=== Resultado: {passed}/{total} asserções OK ===')
    if passed != total:
        sys.exit(1)


if __name__ == '__main__':
    main()
