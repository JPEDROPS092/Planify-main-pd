"""Provisiona um tenant e designa seu owner (operação de superuser).

Modelo de produto: o operador da plataforma (superuser) cria o schema/domínio
da empresa e designa o owner. O owner então popula e gerencia a própria
empresa, inclusive convidando os demais membros.

Exemplos::

    # Cria tenant e um owner novo (senha temporária gerada e exibida)
    python manage.py provision_tenant \
        --schema acme --name "ACME" --domain acme.localhost \
        --owner-email owner@acme.com --owner-username acme_owner \
        --owner-full-name "Maria Owner"

    # Designa um usuário já existente como owner
    python manage.py provision_tenant \
        --schema acme --name "ACME" --domain acme.localhost \
        --owner-email owner@acme.com
"""
from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand, CommandError
from django.db import transaction
from django.utils.crypto import get_random_string

from customers.models import Client, Domain, TenantMembership


class Command(BaseCommand):
    help = 'Provisiona um tenant (schema + domínio) e designa o owner.'

    def add_arguments(self, parser):
        parser.add_argument('--schema', required=True, help='Nome do schema PostgreSQL do tenant.')
        parser.add_argument('--name', required=True, help='Nome visível da empresa.')
        parser.add_argument('--domain', required=True, help='Domínio/subdomínio do tenant.')
        parser.add_argument('--owner-email', required=True, help='E-mail do owner.')
        parser.add_argument('--owner-username', help='Username do owner (default: parte local do e-mail).')
        parser.add_argument('--owner-full-name', help='Nome completo do owner.')
        parser.add_argument(
            '--owner-password',
            help='Senha do owner ao criar uma conta nova. Se omitida, uma senha temporária é gerada.',
        )
        parser.add_argument(
            '--skip-schema-create',
            action='store_true',
            help='Não cria o schema automaticamente (apenas registros no public).',
        )

    @transaction.atomic
    def handle(self, *args, **options):
        User = get_user_model()
        schema_name = options['schema']
        domain_name = options['domain']
        owner_email = User.objects.normalize_email(options['owner_email'])

        if Client.objects.filter(schema_name=schema_name).exists():
            raise CommandError(f'O tenant com schema "{schema_name}" já existe.')
        if Domain.objects.filter(domain=domain_name).exists():
            raise CommandError(f'O domínio "{domain_name}" já está em uso.')

        # Resolve/cria o owner antes de criar o tenant para falhar cedo.
        owner = User.objects.filter(email__iexact=owner_email).first()
        created_owner = False
        temp_password = None

        if owner is None:
            username = options.get('owner_username') or owner_email.split('@')[0]
            if User.objects.filter(username__iexact=username).exists():
                raise CommandError(f'O username "{username}" já está em uso. Informe --owner-username.')
            full_name = options.get('owner_full_name') or username
            temp_password = options.get('owner_password') or get_random_string(12)
            owner = User.objects.create_user(
                email=owner_email,
                username=username,
                full_name=full_name,
                password=temp_password,
            )
            owner.is_active = True
            owner.password_change_required = bool(not options.get('owner_password'))
            owner.save(update_fields=['is_active', 'password_change_required'])
            created_owner = True
        else:
            if TenantMembership.objects.filter(user=owner, is_active=True).exists():
                raise CommandError(
                    f'O usuário "{owner_email}" já possui um vínculo ativo com uma empresa '
                    '(regra: um usuário = uma empresa).'
                )

        tenant = Client(schema_name=schema_name, name=options['name'])
        if options['skip_schema_create']:
            tenant.auto_create_schema = False
        tenant.save()

        Domain.objects.create(tenant=tenant, domain=domain_name, is_primary=True)

        TenantMembership.objects.create(
            user=owner,
            tenant=tenant,
            role=TenantMembership.ROLE_OWNER,
        )

        self.stdout.write(self.style.SUCCESS(
            f'Tenant "{tenant.name}" provisionado: schema={schema_name}, domain={domain_name}'
        ))
        self.stdout.write(self.style.SUCCESS(
            f'Owner: {owner.username} <{owner_email}> (conta {"criada" if created_owner else "existente"})'
        ))
        if temp_password is not None:
            self.stdout.write(self.style.WARNING(
                f'Senha temporária do owner: {temp_password} (troque após o primeiro login)'
            ))
