"""Cria um tenant local de desenvolvimento (conveniência).

Re-arquitetura R9 (2026-06-03): **shared schema**. Um tenant é só uma linha
``customers.Client`` (sem schema/``Domain``); o ``post_save`` cria suas
``TenantSettings`` (R5). Para provisionar empresa + owner de forma canônica use
``provision_tenant``; este comando é o atalho de dev e, opcionalmente, vincula um
usuário existente como owner.
"""
from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand, CommandError
from django.db import transaction

from customers.models import Client, TenantMembership


class Command(BaseCommand):
    help = 'Cria um tenant local de desenvolvimento e, opcionalmente, vincula um owner.'

    def add_arguments(self, parser):
        parser.add_argument('--name', default='Demo', help='Nome visível do tenant (default: Demo).')
        parser.add_argument('--owner-username', help='Username de um usuário existente para vincular como owner.')

    @transaction.atomic
    def handle(self, *args, **options):
        name = options['name']

        if Client.objects.filter(name=name).exists():
            raise CommandError(f'Já existe um tenant com o nome "{name}".')

        tenant = Client.objects.create(name=name)

        owner_username = options.get('owner_username')
        if owner_username:
            User = get_user_model()
            try:
                owner = User.objects.get(username=owner_username)
            except User.DoesNotExist as exc:
                raise CommandError(f'Usuário "{owner_username}" não encontrado.') from exc

            if (
                not owner.is_superuser
                and TenantMembership.objects.filter(user=owner, is_active=True).exists()
            ):
                raise CommandError(
                    f'O usuário "{owner_username}" já possui um vínculo ativo com uma empresa '
                    '(regra: um usuário = uma empresa).'
                )

            TenantMembership.objects.create(
                user=owner,
                tenant=tenant,
                role=TenantMembership.ROLE_OWNER,
            )

        self.stdout.write(
            self.style.SUCCESS(f'Tenant "{tenant.name}" criado (id={tenant.id}).')
        )
