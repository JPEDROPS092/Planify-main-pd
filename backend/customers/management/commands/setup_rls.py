"""Cria/atualiza a role de aplicação ``app_user`` para a RLS nativa (R7).

A RLS do PostgreSQL só vale para roles **sem** ``BYPASSRLS`` que não sejam
superuser nem donas das tabelas. A conexão padrão (``planify``) é superuser e
ignora RLS — ótimo para migrations/seed/testes, péssimo para a app web. Este
comando provisiona uma role ``app_user`` (LOGIN, NOSUPERUSER, NOBYPASSRLS) com os
privilégios CRUD necessários, para a app web conectar com ela em produção::

    python manage.py setup_rls                 # cria/atualiza app_user
    # depois, rode a app web com POSTGRES_USER=app_user (+ POSTGRES_PASSWORD)

Roda pela conexão privilegiada atual (``planify``), que é dona das tabelas e pode
conceder privilégios. É idempotente.
"""
import os
import re

from django.core.management.base import BaseCommand, CommandError
from django.db import connection

IDENT_RE = re.compile(r'^[A-Za-z_][A-Za-z0-9_]*$')


class Command(BaseCommand):
    help = 'Cria/atualiza a role app_user (sem bypass de RLS) com privilégios CRUD.'

    def add_arguments(self, parser):
        parser.add_argument(
            '--user',
            default='app_user',
            help='Nome da role de aplicação (default: app_user).',
        )
        parser.add_argument(
            '--password',
            default=None,
            help='Senha da role (default: env APP_DB_PASSWORD ou "app_user").',
        )

    def handle(self, *args, **options):
        user = options['user']
        if not IDENT_RE.match(user):
            raise CommandError(f'Nome de role inválido: {user!r}')
        password = options['password'] or os.environ.get('APP_DB_PASSWORD', 'app_user')

        if connection.vendor != 'postgresql':
            raise CommandError('setup_rls só faz sentido no PostgreSQL.')

        ident = '"%s"' % user
        with connection.cursor() as c:
            c.execute('SELECT 1 FROM pg_roles WHERE rolname = %s', [user])
            exists = c.fetchone() is not None
            verbo = 'ALTER' if exists else 'CREATE'
            c.execute(
                f"{verbo} ROLE {ident} LOGIN NOSUPERUSER NOBYPASSRLS NOCREATEDB "
                f"NOCREATEROLE PASSWORD %s",
                [password],
            )
            c.execute(f'GRANT USAGE ON SCHEMA public TO {ident}')
            c.execute(f'GRANT SELECT, INSERT, UPDATE, DELETE ON ALL TABLES IN SCHEMA public TO {ident}')
            c.execute(f'GRANT USAGE, SELECT ON ALL SEQUENCES IN SCHEMA public TO {ident}')
            # Tabelas/sequences futuras criadas pela conexão atual (dona) já nascem
            # com os privilégios concedidos para a role de aplicação.
            c.execute(
                f'ALTER DEFAULT PRIVILEGES IN SCHEMA public '
                f'GRANT SELECT, INSERT, UPDATE, DELETE ON TABLES TO {ident}'
            )
            c.execute(
                f'ALTER DEFAULT PRIVILEGES IN SCHEMA public '
                f'GRANT USAGE, SELECT ON SEQUENCES TO {ident}'
            )

        self.stdout.write(self.style.SUCCESS(
            f'Role {user!r} {"atualizada" if exists else "criada"} (LOGIN, NOSUPERUSER, '
            f'NOBYPASSRLS) com privilégios CRUD em public. '
            f'Rode a app web com POSTGRES_USER={user}.'
        ))
