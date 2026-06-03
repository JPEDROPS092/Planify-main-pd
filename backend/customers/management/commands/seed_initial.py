"""Seed inicial idempotente: garante o operador SaaS global (superuser).

Roda em **dev e em produção**. NÃO cria empresas: o tenant de demonstração e o
seu owner ficam em ``seed_demo_data`` (apenas dev) e os tenants reais são criados
via ``provision_tenant`` (prod). Assim este comando é seguro para rodar em prod
sem vazar dados demo.
"""
from django.core.management.base import BaseCommand
from django.db import transaction

from customers.provisioning import ensure_user


class Command(BaseCommand):
    help = 'Seed inicial idempotente: garante o superuser SaaS (dev e prod).'

    def add_arguments(self, parser):
        parser.add_argument('--superuser-username', default='admin')
        parser.add_argument('--superuser-email', default='admin@planify.local')
        parser.add_argument('--superuser-password', default='admin123')
        parser.add_argument('--superuser-full-name', default='Administrador SaaS')
        parser.add_argument(
            '--reset-passwords',
            action='store_true',
            help='Tambem redefine a senha se o superuser ja existir.',
        )

    @transaction.atomic
    def handle(self, *args, **options):
        superuser = ensure_user(
            username=options['superuser_username'],
            email=options['superuser_email'],
            full_name=options['superuser_full_name'],
            password=options['superuser_password'],
            role='ADMIN',
            is_staff=True,
            is_superuser=True,
            reset_password=options['reset_passwords'],
        )

        self.stdout.write(self.style.SUCCESS(
            f'Superuser SaaS garantido: {superuser.username} <{superuser.email}>'
        ))
