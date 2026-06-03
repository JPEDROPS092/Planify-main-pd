"""Migra os dados de uma instância single-tenant legada (SQLite) para o stack
multi-tenant **shared schema** (PostgreSQL, um único schema + ``tenant_id``).

Contexto (Fase R6 do plano ``docs/rearquitetura-shared-schema-plano.md``): a
arquitetura deixou de usar schema-per-tenant (``django-tenants``); agora há um só
schema e cada linha de negócio carrega ``tenant_id`` (FK para ``customers.Client``).
Este comando faz o *onboarding* do acervo legado:

* **Identidade global** (``users.User`` e satélites) é copiada com **dedup por
  e-mail** — usuários já existentes são reaproveitados (não duplicados). PKs de
  usuário **não** são preservados; toda FK/M2M que aponta para o usuário é
  remapeada pelo mapa ``{id_legado: id_novo}``.
* **Dados de negócio** são copiados para as tabelas compartilhadas **carimbando
  ``tenant_id``** com o ``Client`` destino.
* Cada usuário legado migrado (exceto superusuário) ganha uma
  ``TenantMembership`` ativa no tenant destino, respeitando "um usuário = uma
  empresa". O mapeamento de papel legado → papel de tenant é configurável.

Garantias e limites:

* **Idempotente**: linhas de negócio cujo PK já existe **no tenant destino** são
  puladas; re-rodar é no-op.
* **PKs de negócio preservados** quando possível. ⚠️ No shared schema o espaço de
  PK é **global** entre tenants: se um PK legado já existir apontando para **outro**
  tenant, preservá-lo colidiria — o comando **aborta** com mensagem clara (importar
  para um banco que já contém dados de negócio de outros tenants exigiria remapear
  também as FKs entre models de negócio; fora do escopo atual, pois o caso real é
  importar uma base legada para um banco de negócio vazio).
* **FKs de usuário remapeadas**; **timestamps preservados** (``save_base``).
* **Dependência circular** ``projects.Projeto.custos -> costs.Custo`` é tratada com
  gravação diferida (projeto entra com ``custos=NULL`` e é atualizado depois).
* **``--dry-run``** roda tudo numa transação revertida: reporta contagens sem gravar.

Exemplos::

    # Só identidade global (caso real deste projeto: 1 superusuário, sem negócio)
    python manage.py migrate_legacy_data --users-only

    # Onboarding completo de uma base legada para o tenant "Acme" (id ou nome)
    python manage.py migrate_legacy_data --legacy-db backups/db.sqlite3.baseline \
        --tenant Acme

    # Simulação sem gravar
    python manage.py migrate_legacy_data --tenant 1 --dry-run

Rollback: como a gravação é transacional por execução e idempotente, basta apagar
o ``Client`` destino (cascateia os dados de negócio do tenant) e remover do banco
os usuários recém-criados (listados no relatório final).
"""
from pathlib import Path

from django.apps import apps
from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand, CommandError
from django.db import DatabaseError, connections, transaction
from django.db.models import ForeignKey, ManyToManyField, OneToOneField

from customers.models import Client, TenantMembership

LEGACY_ALIAS = 'legacy_source'
TARGET_DB = 'default'


def sqlite_connection_settings(name):
    """Dict de configuração completo para registrar um SQLite em tempo de execução.

    ``connections.databases`` não passa por ``ensure_defaults`` quando alterado
    após a inicialização, então preenchemos todas as chaves exigidas pelo
    backend manualmente.
    """
    return {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': name,
        'USER': '',
        'PASSWORD': '',
        'HOST': '',
        'PORT': '',
        'OPTIONS': {},
        'TIME_ZONE': None,
        'CONN_MAX_AGE': 0,
        'CONN_HEALTH_CHECKS': False,
        'AUTOCOMMIT': True,
        'ATOMIC_REQUESTS': False,
        'TEST': {
            'CHARSET': None, 'COLLATION': None, 'MIGRATE': True,
            'MIRROR': None, 'NAME': None,
        },
    }


# Mapeamento padrão: papel legado (users.User.role) -> papel de tenant.
# 'owner' é deliberadamente evitado: o owner é provisionado por superuser
# (provision_tenant). ADMIN legado vira 'admin' do tenant.
DEFAULT_ROLE_MAP = {
    'ADMIN': TenantMembership.ROLE_ADMIN,
    'PROJECT_MANAGER': TenantMembership.ROLE_MANAGER,
    'TEAM_LEADER': TenantMembership.ROLE_MANAGER,
    'TEAM_MEMBER': TenantMembership.ROLE_MEMBER,
    'STAKEHOLDER': TenantMembership.ROLE_VIEWER,
    'AUDITOR': TenantMembership.ROLE_VIEWER,
}

# Tabelas-satélite do usuário (identidade global): dados que pertencem
# inequivocamente a um único usuário (FK só para User). Migradas SEM preservar PK,
# remapeando a FK de usuário e com idempotência por usuário.
USER_SATELLITE_MODELS = [
    ('users', 'UserProfile'),      # OneToOne com User
    ('users', 'PasswordHistory'),  # N por usuário
    ('users', 'AccessAttempt'),    # N por usuário
]

# RBAC legado global (AccessProfile/Permission/UserAccessProfile) NÃO é migrado
# automaticamente: é configuração global semeada por `create_access_profiles`,
# e a decisão "global vs por tenant" segue em aberto na arquitetura
# (ver docs/multi-tenant-architecture.md). Reportado como pulado, nunca dropado.
SKIPPED_SHARED_MODELS = [
    ('users', 'AccessProfile'),
    ('users', 'Permission'),
    ('users', 'UserAccessProfile'),
]

# Modelos de negócio em ordem de dependência de FK. A única FK "para a frente" é
# Projeto.custos -> Custo, tratada por diferimento.
TENANT_MODELS = [
    ('teams', 'Equipe'),
    ('teams', 'MembroEquipe'),
    ('teams', 'PermissaoEquipe'),
    ('projects', 'Projeto'),
    ('projects', 'Sprint'),
    ('tasks', 'Tarefa'),
    ('projects', 'MembroProjeto'),
    ('projects', 'HistoricoStatusProjeto'),
    ('costs', 'Categoria'),
    ('costs', 'Custo'),
    ('costs', 'OrcamentoProjeto'),
    ('costs', 'OrcamentoTarefa'),
    ('costs', 'Alerta'),
    ('tasks', 'AtribuicaoTarefa'),
    ('tasks', 'ComentarioTarefa'),
    ('tasks', 'HistoricoStatusTarefa'),
    ('risks', 'Risco'),
    ('risks', 'HistoricoRisco'),
    ('documents', 'Documento'),
    ('documents', 'HistoricoDocumento'),
    ('documents', 'Comentario'),
    ('communications', 'ChatMensagem'),
    ('communications', 'ChatMensagemLeitura'),
    ('communications', 'Notificacao'),
    ('communications', 'ConfiguracaoNotificacao'),
    ('communications', 'Comunicacao'),
]


class Command(BaseCommand):
    help = 'Migra dados de uma base single-tenant legada (SQLite) para o shared schema multi-tenant.'

    def add_arguments(self, parser):
        parser.add_argument(
            '--legacy-db',
            default='db.sqlite3',
            help='Caminho do SQLite legado (default: db.sqlite3).',
        )
        parser.add_argument(
            '--tenant',
            help='Client destino (id ou nome) para os dados de negócio. '
                 'Obrigatório, exceto com --users-only.',
        )
        parser.add_argument(
            '--users-only',
            action='store_true',
            help='Migra apenas a identidade global (users); ignora dados de negócio.',
        )
        parser.add_argument(
            '--no-membership',
            action='store_true',
            help='Não cria TenantMembership para os usuários migrados.',
        )
        parser.add_argument(
            '--default-role',
            default=TenantMembership.ROLE_MEMBER,
            choices=[c[0] for c in TenantMembership.ROLE_CHOICES],
            help='Papel de tenant para usuários sem mapeamento (default: member).',
        )
        parser.add_argument(
            '--allow-nonempty',
            action='store_true',
            help='Permite migrar negócio mesmo se o tenant destino já tiver linhas '
                 '(desliga a checagem de idempotência por PK no tenant).',
        )
        parser.add_argument(
            '--dry-run',
            action='store_true',
            help='Não persiste: roda dentro de uma transação revertida e só reporta contagens.',
        )

    # ------------------------------------------------------------------ utils

    def _register_legacy(self, path):
        legacy_path = Path(path)
        if not legacy_path.exists():
            raise CommandError(f'Banco legado não encontrado: {legacy_path}')
        connections.databases[LEGACY_ALIAS] = sqlite_connection_settings(str(legacy_path))

    @staticmethod
    def _resolve_tenant(value):
        qs = Client.objects.all()
        tenant = None
        if value.isdigit():
            tenant = qs.filter(pk=int(value)).first()
        if tenant is None:
            tenant = qs.filter(name=value).first()
        return tenant

    @staticmethod
    def _user_fk_fields(model, user_model):
        return [
            f for f in model._meta.get_fields()
            if isinstance(f, (ForeignKey, OneToOneField))
            and not f.auto_created
            and f.related_model is user_model
        ]

    @staticmethod
    def _user_m2m_fields(model, user_model):
        return [
            f for f in model._meta.get_fields()
            if isinstance(f, ManyToManyField) and f.related_model is user_model
        ]

    def _legacy_rows(self, model):
        """Lê todas as linhas de um modelo na base legada.

        Retorna ``None`` se a tabela não existir (drift de schema do legado),
        para que o caller possa pular o modelo sem abortar a migração inteira.
        """
        try:
            return list(model.objects.using(LEGACY_ALIAS).all())
        except DatabaseError:
            return None

    # ----------------------------------------------------------------- handle

    def handle(self, *args, **options):
        users_only = options['users_only']
        dry_run = options['dry_run']

        self._register_legacy(options['legacy_db'])

        tenant = None
        if not users_only:
            raw = options.get('tenant')
            if not raw:
                raise CommandError('Informe --tenant (id ou nome do Client destino) ou use --users-only.')
            tenant = self._resolve_tenant(raw)
            if tenant is None:
                raise CommandError(
                    f'Client destino "{raw}" não existe. Provisione-o antes '
                    '(provision_tenant / create_dev_tenant) ou crie via admin.'
                )

        User = get_user_model()
        role_map = dict(DEFAULT_ROLE_MAP)
        default_role = options['default_role']

        report = {'users': {}, 'shared': {}, 'tenant': {}, 'memberships': 0}
        migrated_user_emails = []

        try:
            with transaction.atomic():
                user_id_map = self._migrate_users(User, report, migrated_user_emails)
                self._migrate_shared(report, user_id_map)

                if not users_only:
                    if not options['no_membership']:
                        report['memberships'] = self._create_memberships(
                            User, tenant, user_id_map, role_map, default_role,
                        )
                    self._migrate_tenant_data(
                        tenant, user_id_map, report, options['allow_nonempty'],
                    )

                if dry_run:
                    transaction.set_rollback(True)
        finally:
            connections[LEGACY_ALIAS].close()
            connections.databases.pop(LEGACY_ALIAS, None)

        self._print_report(report, migrated_user_emails, dry_run, users_only, tenant)

    # --------------------------------------------------------------- migração

    def _migrate_users(self, User, report, migrated_emails):
        """Copia usuários legados para a identidade global (dedup por e-mail).

        Não preserva PKs de usuário: retorna o mapa ``{id_legado: id_novo}``
        usado para remapear todas as FKs de negócio.
        """
        user_id_map = {}
        legacy_users = self._legacy_rows(User)
        if legacy_users is None:
            raise CommandError('A base legada não possui a tabela de usuários.')

        report['users'] = {'lidos': len(legacy_users), 'criados': 0, 'reutilizados': 0}

        field_names = [
            f.name for f in User._meta.fields
            if f.name not in ('id', 'password')
        ]

        for legacy in legacy_users:
            existing = User.objects.filter(email__iexact=legacy.email).first()
            if existing is not None:
                user_id_map[legacy.pk] = existing.pk
                report['users']['reutilizados'] += 1
                continue

            new_user = User(**{name: getattr(legacy, name) for name in field_names})
            # Preserva o hash de senha exatamente como estava (sem re-hash).
            new_user.password = legacy.password
            new_user.save()
            user_id_map[legacy.pk] = new_user.pk
            report['users']['criados'] += 1
            migrated_emails.append(legacy.email)

        return user_id_map

    def _migrate_shared(self, report, user_id_map):
        """Migra satélites do usuário (perfil, histórico de senha, tentativas).

        Sem preservação de PK: remapeia a FK de usuário e usa idempotência por
        usuário. RBAC legado é apenas reportado como pulado.
        """
        User = get_user_model()
        for app_label, model_name in USER_SATELLITE_MODELS:
            model = apps.get_model(app_label, model_name)
            rows = self._legacy_rows(model)
            if rows is None:
                report['shared'][model._meta.label] = 'tabela ausente'
                continue
            copied = self._copy_user_satellite(model, rows, user_id_map, User)
            report['shared'][model._meta.label] = copied

        for app_label, model_name in SKIPPED_SHARED_MODELS:
            model = apps.get_model(app_label, model_name)
            rows = self._legacy_rows(model)
            n = 0 if rows is None else len(rows)
            report['shared'][model._meta.label] = f'pulado (RBAC global; {n} na origem)'

    def _copy_user_satellite(self, model, rows, user_id_map, user_model):
        """Copia uma tabela-satélite do usuário sem preservar PK.

        - Remapeia a única FK de usuário para o id novo.
        - Idempotência por usuário: se o usuário-destino já tiver linha(s) nesse
          model, pula esse usuário (evita duplicar perfis/históricos ao re-rodar).
        - Preserva timestamps via ``save_base(raw=True)``.
        """
        fk = next(iter(self._user_fk_fields(model, user_model)), None)
        if fk is None:
            return 0
        users_with_rows = set(model.objects.values_list(fk.attname, flat=True))
        copied = 0
        for obj in rows:
            old_uid = getattr(obj, fk.attname)
            new_uid = user_id_map.get(old_uid)
            if new_uid is None or new_uid in users_with_rows:
                continue
            setattr(obj, fk.attname, new_uid)
            obj.pk = None
            obj._state.db = TARGET_DB
            obj._state.adding = True
            obj.save_base(using=TARGET_DB, raw=True, force_insert=True)
            copied += 1
        return copied

    def _create_memberships(self, User, tenant, user_id_map, role_map, default_role):
        created = 0
        for new_id in set(user_id_map.values()):
            user = User.objects.filter(pk=new_id).first()
            if user is None or user.is_superuser:
                continue  # superusuário tem bypass global; não precisa de membership
            if TenantMembership.objects.filter(user=user, is_active=True).exists():
                continue  # respeita "um usuário = uma empresa"
            role = role_map.get(user.role, default_role)
            TenantMembership.objects.create(user=user, tenant=tenant, role=role)
            created += 1
        return created

    def _migrate_tenant_data(self, tenant, user_id_map, report, allow_nonempty):
        User = get_user_model()
        projeto_custos = {}  # {projeto_pk: custos_pk} para gravação diferida

        for app_label, model_name in TENANT_MODELS:
            model = apps.get_model(app_label, model_name)
            rows = self._legacy_rows(model)
            if rows is None:
                report['tenant'][model._meta.label] = 'tabela ausente'
                continue

            if model._meta.label == 'projects.Projeto':
                for obj in rows:
                    custos_id = getattr(obj, 'custos_id', None)
                    if custos_id is not None:
                        projeto_custos[obj.pk] = custos_id
                        obj.custos_id = None

            copied = self._copy_rows(model, rows, user_id_map, User, tenant, allow_nonempty)
            report['tenant'][model._meta.label] = copied

        # Segunda passada: resolve a FK circular Projeto.custos.
        if projeto_custos:
            Projeto = apps.get_model('projects', 'Projeto')
            for projeto_pk, custos_id in projeto_custos.items():
                Projeto._base_manager.filter(pk=projeto_pk).update(custos_id=custos_id)

    def _copy_rows(self, model, rows, user_id_map, user_model, tenant, allow_nonempty=False):
        """Copia linhas de negócio preservando PK e timestamps, carimbando ``tenant_id``.

        - **Carimba** ``tenant_id`` com o ``Client`` destino em cada linha.
        - **Remapeia** as FKs de usuário pelo mapa de identidade.
        - **Idempotente**: pula linhas cujo PK já existe **no tenant destino**.
        - **Colisão cross-tenant**: se o PK já existir apontando para outro tenant,
          aborta (preservar PK colidiria no espaço de PK global do shared schema).
        - Usa ``_base_manager`` (não-filtrado) para inspeção, independente de contexto.
        """
        fk_fields = self._user_fk_fields(model, user_model)
        m2m_fields = self._user_m2m_fields(model, user_model)

        # {pk: tenant_id} de tudo que já existe na tabela compartilhada.
        existing = dict(model._base_manager.values_list('pk', 'tenant_id'))
        copied = 0

        for obj in rows:
            owner = existing.get(obj.pk)
            if owner is not None:
                if owner == tenant.id:
                    if allow_nonempty:
                        pass  # ainda assim pulamos (PK já ocupado); allow_nonempty não recria
                    continue  # já migrado neste tenant: idempotente
                raise CommandError(
                    f'Colisão de PK no shared schema: {model._meta.label} pk={obj.pk} '
                    f'já pertence ao tenant {owner} (destino={tenant.id}). Preservar PK '
                    'colidiria. Importe para um banco sem dados de negócio de outros '
                    'tenants, ou estenda o comando para remapear FKs de negócio.'
                )
            for f in fk_fields:
                old = getattr(obj, f.attname)
                if old is not None:
                    setattr(obj, f.attname, user_id_map.get(old, old))
            obj.tenant_id = tenant.id  # carimbo do tenant destino
            obj._state.db = TARGET_DB
            obj._state.adding = True
            obj.save_base(using=TARGET_DB, raw=True, force_insert=True)
            copied += 1

        # M2M para usuário (ex.: Comunicacao.destinatarios), remapeado.
        if m2m_fields:
            for f in m2m_fields:
                through = getattr(model, f.name).through
                self._copy_m2m(through, f, user_id_map, user_model)

        return copied

    def _copy_m2m(self, through, m2m_field, user_id_map, user_model):
        """Copia a tabela intermediária de um M2M usuário, remapeando a coluna de usuário.

        A tabela through é auto-gerada e não tem ``tenant_id``; preserva PK e é
        idempotente por PK.
        """
        rows = self._legacy_rows(through)
        if rows is None:
            return
        existing_pks = set(through._base_manager.values_list('pk', flat=True))
        user_fk = next(
            f for f in through._meta.fields
            if isinstance(f, ForeignKey) and f.related_model is user_model
        )
        for obj in rows:
            if obj.pk in existing_pks:
                continue
            old = getattr(obj, user_fk.attname)
            if old is not None:
                setattr(obj, user_fk.attname, user_id_map.get(old, old))
            obj._state.db = TARGET_DB
            obj._state.adding = True
            obj.save_base(using=TARGET_DB, raw=True, force_insert=True)

    # ---------------------------------------------------------------- relatório

    def _print_report(self, report, migrated_emails, dry_run, users_only, tenant):
        w = self.stdout.write
        style = self.style
        tenant_label = tenant.name if tenant is not None else None
        header = 'SIMULAÇÃO (dry-run, nada gravado)' if dry_run else 'MIGRAÇÃO CONCLUÍDA'
        w(style.MIGRATE_HEADING(f'\n=== {header} ==='))

        u = report['users']
        w(style.SUCCESS(
            f"Usuários: lidos={u.get('lidos', 0)} "
            f"criados={u.get('criados', 0)} reutilizados={u.get('reutilizados', 0)}"
        ))
        if not users_only:
            w(style.SUCCESS(f"TenantMemberships criadas: {report['memberships']} (tenant={tenant_label})"))

        if report['shared']:
            w(style.MIGRATE_LABEL('\n-- Identidade global --'))
            for label, n in report['shared'].items():
                w(f'  {label}: {n}')

        if not users_only and report['tenant']:
            w(style.MIGRATE_LABEL(f'\n-- Negócio (tenant {tenant_label}) --'))
            total = 0
            for label, n in report['tenant'].items():
                w(f'  {label}: {n}')
                if isinstance(n, int):
                    total += n
            w(style.SUCCESS(f'  total de linhas de negócio migradas: {total}'))

        if migrated_emails:
            w(style.WARNING('\nUsuários criados (para rollback, se necessário):'))
            for email in migrated_emails:
                w(f'  - {email}')
