#!/usr/bin/env python
"""Teste ponta-a-ponta do fluxo de auth multi-tenant (provisionamento + convites).

Re-arquitetura R8/R9 (2026-06-03): **shared schema**, sem subdomínio. O tenant é
uma linha ``customers.Client`` (sem schema/``Domain``); o tenant da request vem da
``TenantMembership`` ativa (não do host). Exercita o stack HTTP real
(``PermissionMiddleware`` resolve o tenant pela membership + JWT + ``HasTenantRole``
+ ``TenantManager``) e o management command ``provision_tenant``:

    1. Superuser provisiona empresa + owner (command provision_tenant).
    2. Owner cria um convite (member) em /api/tenant/invitations/  -> 201.
    3. Inspeção pública do convite por token                       -> 200.
    4. Aceite público cria conta nova + TenantMembership ativa     -> 201.
    5. Convidado acessa /api/projects/ no tenant                   -> 200.
    6. Convidado (member) tenta criar convite                      -> 403.
    7. Reaceitar convite já aceito                                 -> 400.
    8. Convidar e-mail que já tem vínculo ativo (o owner)          -> 400.
    9. Usuário sem vínculo acessa o tenant                         -> 403.

Idempotente: limpa remanescentes no início e remove tudo ao final.

Uso:
    python scripts/e2e_invitations.py
"""
import os
import sys

import django

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'planify.settings')
django.setup()

from django.conf import settings  # noqa: E402

# Script standalone (fora do test-runner): 'testserver' não entra no ALLOWED_HOSTS.
if 'testserver' not in settings.ALLOWED_HOSTS:
    settings.ALLOWED_HOSTS = list(settings.ALLOWED_HOSTS) + ['testserver']

from django.contrib.auth import get_user_model  # noqa: E402
from django.core.management import call_command  # noqa: E402
from django.test import Client as HttpClient  # noqa: E402
from rest_framework_simplejwt.tokens import RefreshToken  # noqa: E402

from customers.models import Client, TenantInvitation, TenantMembership  # noqa: E402

User = get_user_model()

TENANT_NAME = 'E2E Invites'
OWNER_EMAIL = 'owner.inv@planify.test'
INVITEE_EMAIL = 'invitee.inv@planify.test'
OUTSIDER_EMAIL = 'outsider.inv@planify.test'
ALL_EMAILS = [OWNER_EMAIL, INVITEE_EMAIL, OUTSIDER_EMAIL]

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
    # Apagar o Client cascateia memberships, convites e dados de negócio do tenant
    # (FKs CASCADE). Os usuários de teste (identidade global) são removidos à parte.
    Client.objects.filter(name=TENANT_NAME).delete()
    # Convites por e-mail de tenants que porventura não foram apagados.
    TenantInvitation.objects.filter(email__in=ALL_EMAILS).delete()
    User.objects.filter(email__in=ALL_EMAILS).delete()


def get(http, path, token=None):
    kwargs = {}
    if token:
        kwargs['HTTP_AUTHORIZATION'] = f'Bearer {token}'
    return http.get(path, **kwargs)


def post(http, path, data, token=None):
    kwargs = {'content_type': 'application/json'}
    if token:
        kwargs['HTTP_AUTHORIZATION'] = f'Bearer {token}'
    return http.post(path, data=data, **kwargs)


def main():
    print('=== E2E auth multi-tenant (shared schema: provision + convites) ===\n')
    cleanup()
    try:
        print('1) Superuser provisiona empresa + owner (provision_tenant):')
        call_command(
            'provision_tenant',
            name=TENANT_NAME,
            owner_email=OWNER_EMAIL, owner_username='owner_inv',
            owner_full_name='Owner Inv', owner_password='Senha-E2E-123',
            verbosity=0,
        )
        owner = User.objects.get(email=OWNER_EMAIL)
        owner_membership = TenantMembership.objects.filter(
            user=owner, is_active=True, role=TenantMembership.ROLE_OWNER
        ).first()
        check('owner criado com TenantMembership owner ativa', owner_membership is not None)

        http = HttpClient()
        owner_tok = token_for(owner)

        print('\n2) Owner cria convite (member):')
        r = post(http, '/api/tenant/invitations/',
                 {'email': INVITEE_EMAIL, 'role': 'member'}, owner_tok)
        check('POST /api/tenant/invitations/ -> 201', r.status_code == 201, f'status={r.status_code}')
        token = r.json().get('token') if r.status_code == 201 else None
        check('convite retornou token', bool(token))

        print('\n3) Inspeção pública do convite:')
        r = get(http, f'/api/invitations/{token}/')
        body = r.json() if r.status_code == 200 else {}
        check('GET /api/invitations/<token>/ -> 200', r.status_code == 200, f'status={r.status_code}')
        check('convite pendente e exige conta nova',
              body.get('is_pending') is True and body.get('requires_new_account') is True,
              f'body={body}')

        print('\n4) Aceite público cria conta + membership:')
        r = post(http, f'/api/invitations/{token}/accept/',
                 {'username': 'invitee_inv', 'full_name': 'Invitee Inv',
                  'password': 'Senha-E2E-123'})
        check('POST accept -> 201', r.status_code == 201, f'status={r.status_code}')
        invitee = User.objects.filter(email=INVITEE_EMAIL).first()
        invitee_membership = TenantMembership.objects.filter(
            user=invitee, is_active=True, role=TenantMembership.ROLE_MEMBER
        ).first() if invitee else None
        check('convidado ganhou TenantMembership member ativa', invitee_membership is not None)
        inv = TenantInvitation.objects.get(token=token)
        check('convite marcado como aceito', inv.status == TenantInvitation.STATUS_ACCEPTED)

        print('\n5) Convidado acessa o tenant:')
        invitee_tok = token_for(invitee)
        r = get(http, '/api/projects/', invitee_tok)
        check('convidado GET /api/projects/ -> 200', r.status_code == 200, f'status={r.status_code}')

        print('\n6) Convidado (member) tenta criar convite:')
        r = post(http, '/api/tenant/invitations/',
                 {'email': 'x@planify.test', 'role': 'member'}, invitee_tok)
        check('member POST convite -> 403', r.status_code == 403, f'status={r.status_code}')

        print('\n7) Reaceite de convite já aceito:')
        r = post(http, f'/api/invitations/{token}/accept/',
                 {'username': 'dup', 'full_name': 'Dup', 'password': 'Senha-E2E-123'})
        check('reaceite -> 400', r.status_code == 400, f'status={r.status_code}')

        print('\n8) Convidar e-mail com vínculo ativo (owner):')
        r = post(http, '/api/tenant/invitations/',
                 {'email': OWNER_EMAIL, 'role': 'member'}, owner_tok)
        check('convidar usuário já vinculado -> 400', r.status_code == 400, f'status={r.status_code}')

        print('\n9) Usuário sem vínculo acessa o tenant:')
        outsider = User.objects.create_user(
            email=OUTSIDER_EMAIL, username='outsider_inv',
            full_name='Outsider Inv', password='Senha-E2E-123',
        )
        r = get(http, '/api/projects/', token_for(outsider))
        check('outsider GET /api/projects/ -> 403', r.status_code == 403, f'status={r.status_code}')

    finally:
        print('\nTeardown: removendo tenant/usuários de teste...')
        cleanup()

    total = len(_results)
    passed = sum(1 for r in _results if r)
    print(f'\n=== Resultado: {passed}/{total} asserções OK ===')
    if passed != total:
        sys.exit(1)


if __name__ == '__main__':
    main()
