from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand, CommandError
from django.db import transaction

from customers.models import Client, Domain, TenantMembership


class Command(BaseCommand):
    help = 'Cria um tenant local com domínio e, opcionalmente, vincula um owner.'

    def add_arguments(self, parser):
        parser.add_argument('--schema', default='demo', help='Nome do schema PostgreSQL do tenant.')
        parser.add_argument('--name', default='Demo', help='Nome visível do cliente.')
        parser.add_argument('--domain', default='demo.localhost', help='Domínio/subdomínio do tenant.')
        parser.add_argument('--owner-username', help='Username do usuário owner do tenant.')
        parser.add_argument(
            '--skip-schema-create',
            action='store_true',
            help='Cria apenas os registros no public schema, sem criar schema automaticamente.',
        )

    @transaction.atomic
    def handle(self, *args, **options):
        schema_name = options['schema']
        domain_name = options['domain']

        if Client.objects.filter(schema_name=schema_name).exists():
            raise CommandError(f'O tenant com schema "{schema_name}" já existe.')

        if Domain.objects.filter(domain=domain_name).exists():
            raise CommandError(f'O domínio "{domain_name}" já está em uso.')

        tenant = Client(
            schema_name=schema_name,
            name=options['name'],
        )
        if options['skip_schema_create']:
            tenant.auto_create_schema = False
        tenant.save()

        Domain.objects.create(
            tenant=tenant,
            domain=domain_name,
            is_primary=True,
        )

        owner_username = options.get('owner_username')
        if owner_username:
            User = get_user_model()
            try:
                owner = User.objects.get(username=owner_username)
            except User.DoesNotExist as exc:
                raise CommandError(f'Usuário "{owner_username}" não encontrado.') from exc

            TenantMembership.objects.create(
                user=owner,
                tenant=tenant,
                role=TenantMembership.ROLE_OWNER,
            )

        self.stdout.write(
            self.style.SUCCESS(
                f'Tenant "{tenant.name}" criado: schema={tenant.schema_name}, domain={domain_name}'
            )
        )
