#!/usr/bin/env python
"""Validação ponta-a-ponta do comando ``migrate_legacy_data`` (shared schema).

Re-arquitetura R8 (2026-06-03): o destino agora é o **shared schema** (um único
schema PostgreSQL + ``tenant_id``), sem ``django-tenants``/``Domain``/schema por
tenant. O comando lê uma base single-tenant legada (SQLite) e copia: identidade
global para ``users`` (dedup por e-mail) e dados de negócio carimbados com o
``tenant_id`` do ``Client`` destino.

Como o SQLite legado real deste projeto não tem dados de negócio (apenas um
superusuário), este script EXERCITA o caminho de negócio de forma sintética:

1. Constrói um SQLite legado temporário com o schema atual dos models (via
   ``schema_editor``) e o popula com uma base representativa carimbada num tenant
   de origem fictício: 2 usuários + equipe/membro + projeto/sprint/tarefa + risco
   + categoria/custo + documento + comunicação (com M2M ``destinatarios``).
2. Provisiona um ``Client`` destino descartável no banco shared.
3. Roda ``migrate_legacy_data --legacy-db <temp> --tenant <nome>``.
4. Asserções (lendo com o tenant destino escopado pelo ``TenantManager``):
   - usuários criados/deduplicados no ``users`` e ``TenantMembership`` por papel;
   - contagens por tabela no tenant destino == contagens da base legada;
   - **remapeamento de FK de usuário** (ex.: ``Tarefa.criado_por`` e
     ``Comunicacao.destinatarios`` apontam para os NOVOS ids de ``users``);
   - PKs de negócio preservados; FK circular ``Projeto.custos`` restaurada;
   - **carimbo de ``tenant_id``** correto em todas as linhas migradas;
   - **idempotência**: 2ª execução copia 0 linhas de negócio.
5. Teardown completo (apaga o Client destino — cascateia o negócio —, os usuários
   e o arquivo temp).

Uso:
    python scripts/e2e_migrate_legacy.py
"""
import os
import sys
import tempfile
from datetime import date
from io import StringIO

import django

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'planify.settings')
django.setup()

from django.contrib.auth import get_user_model  # noqa: E402
from django.core.management import call_command  # noqa: E402
from django.db import connections  # noqa: E402
from django.db.models.signals import post_save  # noqa: E402

from communications.models import Comunicacao  # noqa: E402
from costs.models import Categoria, Custo  # noqa: E402
from customers import config, context  # noqa: E402
from customers.management.commands.migrate_legacy_data import sqlite_connection_settings  # noqa: E402
from customers.models import Client, TenantMembership  # noqa: E402
from documents.models import Documento  # noqa: E402
from projects.models import Projeto, Sprint  # noqa: E402
from risks.models import Risco  # noqa: E402
from tasks.models import Tarefa  # noqa: E402
from teams.models import Equipe, MembroEquipe  # noqa: E402

User = get_user_model()

TENANT_NAME = 'E2E Migrate'
BUILD_ALIAS = 'e2e_legacy_build'
# id do "Client" de origem fictício dentro do SQLite legado (só para satisfazer a
# FK tenant das tabelas de negócio na origem; o destino re-carimba o tenant_id).
SRC_TENANT_ID = 1
# Faixa alta de PKs de negócio na origem (migrate preserva PK; evita colisão com
# dados já existentes no banco shared de dev, ex.: o seed Demo).
PK_BASE = 90_000_000
EMAIL_A = 'legacy.alice@planify.test'
EMAIL_B = 'legacy.bob@planify.test'
EMAILS = [EMAIL_A, EMAIL_B]

_results = []


def check(label, condition, detail=''):
    status = 'PASS' if condition else 'FAIL'
    _results.append(bool(condition))
    suffix = f'  ({detail})' if detail else ''
    print(f'  [{status}] {label}{suffix}')
    return condition


# --------------------------------------------------------------- legado temp

# Models a materializar no SQLite legado (ordem de dependência de FK). ``Client``
# entra primeiro para satisfazer a FK ``tenant`` das tabelas de negócio na origem.
BUILD_MODELS = [
    Client, User, Equipe, MembroEquipe, Projeto, Sprint, Tarefa,
    Categoria, Custo, Risco, Documento, Comunicacao,
]


def build_legacy_db(path):
    connections.databases[BUILD_ALIAS] = sqlite_connection_settings(path)
    conn = connections[BUILD_ALIAS]
    with conn.schema_editor() as se:
        for model in BUILD_MODELS:
            se.create_model(model)


def populate_legacy():
    """Cria a base single-tenant legada. Retorna contagens esperadas por model.

    O comando ``migrate_legacy_data`` **preserva os PKs** de negócio ao copiar; se
    o banco shared de destino já tiver dados de outros tenants (ex.: o seed
    ``Demo``), PKs baixos colidiriam e o comando abortaria. Para o e2e ser robusto
    a um banco de dev já populado, geramos os PKs de negócio numa faixa **alta**
    (``PK_BASE``), improvável de colidir com dados reais.
    """
    db = BUILD_ALIAS
    next_pk = iter(range(PK_BASE, PK_BASE + 1000)).__next__

    # Client de origem fictício (FK tenant). Desconectamos o post_save que cria
    # TenantSettings no banco default — aqui o Client vive só no SQLite legado.
    post_save.disconnect(dispatch_uid='create_tenant_settings', sender=Client)
    try:
        Client(id=SRC_TENANT_ID, name='Origem Legada').save(using=db)
    finally:
        post_save.connect(
            config._create_tenant_settings,
            sender=Client, dispatch_uid='create_tenant_settings',
        )

    alice = User(email=EMAIL_A, username='legacy_alice', full_name='Legacy Alice',
                 role='ADMIN', is_active=True)
    alice.set_password('x')
    alice.save(using=db)
    bob = User(email=EMAIL_B, username='legacy_bob', full_name='Legacy Bob',
               role='TEAM_MEMBER', is_active=True)
    bob.set_password('x')
    bob.save(using=db)

    t = SRC_TENANT_ID
    equipe = Equipe(pk=next_pk(), tenant_id=t, nome='Equipe Legada', criado_por=alice)
    equipe.save(using=db)
    # bulk_create evita o save() custom de MembroEquipe, que consulta o DB
    # default (postgres) e quebraria ao popular o SQLite legado.
    MembroEquipe.objects.using(db).bulk_create([
        MembroEquipe(pk=next_pk(), tenant_id=t, equipe=equipe, usuario=bob,
                     papel='DEV', adicionado_por=alice),
    ])

    projeto = Projeto(
        pk=next_pk(), tenant_id=t, titulo='Projeto Legado', descricao='desc',
        data_inicio=date(2025, 1, 1), data_fim=date(2025, 12, 31), criado_por=alice,
    )
    projeto.save(using=db)
    sprint = Sprint(pk=next_pk(), tenant_id=t, projeto=projeto, nome='Sprint 1',
                    data_inicio=date(2025, 1, 1), data_fim=date(2025, 2, 1), criado_por=alice)
    sprint.save(using=db)
    tarefa = Tarefa(
        pk=next_pk(), tenant_id=t, titulo='Tarefa Legada', descricao='desc',
        data_inicio=date(2025, 1, 1), data_termino=date(2025, 1, 15), projeto=projeto,
        sprint=sprint, criado_por=bob, atualizado_por=alice,
    )
    tarefa.save(using=db)

    categoria = Categoria(pk=next_pk(), tenant_id=t, nome='Infra')
    categoria.save(using=db)
    custo = Custo(pk=next_pk(), tenant_id=t, projeto=projeto, tarefa=tarefa, categoria=categoria,
                  descricao='Servidores', valor='1000.00', data=date(2025, 1, 10),
                  criado_por=alice)
    custo.save(using=db)
    # Exercita a FK circular Projeto.custos -> Custo.
    projeto.custos = custo
    projeto.save(using=db)

    Risco(pk=next_pk(), tenant_id=t, projeto=projeto, descricao='Risco legado',
          probabilidade='ALTA', impacto='ALTO', criado_por=alice).save(using=db)

    Documento(
        pk=next_pk(), tenant_id=t, projeto=projeto, tarefa=tarefa, titulo='Doc Legado',
        tipo='OUTRO', arquivo='documentos/legacy.txt', tamanho_arquivo=10,
        tipo_arquivo='text/plain', enviado_por=alice,
    ).save(using=db)

    com = Comunicacao(pk=next_pk(), tenant_id=t, projeto=projeto, tipo='ATA',
                      titulo='Ata Legada', texto='conteudo', remetente=alice)
    com.save(using=db)
    # M2M de usuário (deve ser remapeado). A tabela through não tem tenant_id e é
    # copiada preservando PK; geramos PKs altos para não colidir com o seed.
    through = Comunicacao.destinatarios.through
    src_field = next(f for f in through._meta.fields
                     if f.is_relation and f.related_model is Comunicacao)
    usr_field = next(f for f in through._meta.fields
                     if f.is_relation and f.related_model is User)
    through.objects.using(db).bulk_create([
        through(**{'pk': next_pk(), src_field.attname: com.pk, usr_field.attname: alice.pk}),
        through(**{'pk': next_pk(), src_field.attname: com.pk, usr_field.attname: bob.pk}),
    ])

    return {
        'teams.Equipe': 1,
        'teams.MembroEquipe': 1,
        'projects.Projeto': 1,
        'projects.Sprint': 1,
        'tasks.Tarefa': 1,
        'costs.Categoria': 1,
        'costs.Custo': 1,
        'risks.Risco': 1,
        'documents.Documento': 1,
        'communications.Comunicacao': 1,
    }


# --------------------------------------------------------------- tenant util

def cleanup_all(legacy_path):
    # Apagar o Client destino cascateia o negócio do tenant (FK CASCADE).
    Client.objects.filter(name=TENANT_NAME).delete()
    User.objects.filter(email__in=EMAILS).delete()
    if BUILD_ALIAS in connections.databases:
        connections[BUILD_ALIAS].close()
        connections.databases.pop(BUILD_ALIAS, None)
    if legacy_path and os.path.exists(legacy_path):
        os.remove(legacy_path)


def make_tenant():
    return Client.objects.create(name=TENANT_NAME)


# --------------------------------------------------------------- asserções

def run_assertions(expected, tenant):
    # Usuários migrados para a identidade global + memberships.
    alice = User.objects.filter(email=EMAIL_A).first()
    bob = User.objects.filter(email=EMAIL_B).first()
    check('alice criada em users', alice is not None)
    check('bob criado em users', bob is not None)
    if alice and bob:
        check('hash de senha preservado (alice)', alice.password.startswith('pbkdf2_'),
              alice.password[:12])
        m_alice = TenantMembership.objects.filter(user=alice, is_active=True).first()
        m_bob = TenantMembership.objects.filter(user=bob, is_active=True).first()
        check('membership de alice = admin (ADMIN->admin)',
              m_alice is not None and m_alice.role == TenantMembership.ROLE_ADMIN,
              getattr(m_alice, 'role', None))
        check('membership de bob = member (TEAM_MEMBER->member)',
              m_bob is not None and m_bob.role == TenantMembership.ROLE_MEMBER,
              getattr(m_bob, 'role', None))

    # Contagens por tabela escopadas ao tenant destino (TenantManager filtra por
    # tenant_id no contexto) — robusto mesmo com outros tenants no mesmo banco.
    label_to_model = {
        'teams.Equipe': Equipe, 'teams.MembroEquipe': MembroEquipe,
        'projects.Projeto': Projeto, 'projects.Sprint': Sprint, 'tasks.Tarefa': Tarefa,
        'costs.Categoria': Categoria, 'costs.Custo': Custo, 'risks.Risco': Risco,
        'documents.Documento': Documento, 'communications.Comunicacao': Comunicacao,
    }
    with context.scope(tenant_id=tenant.id):
        for label, model in label_to_model.items():
            got = model.objects.count()
            check(f'contagem {label}: {got} == {expected[label]}', got == expected[label],
                  f'esperado={expected[label]} obtido={got}')

        # Integridade referencial + remapeamento de FK de usuário + carimbo de tenant.
        tarefa = Tarefa.objects.first()
        check('Tarefa.criado_por remapeado para o id novo de bob',
              tarefa is not None and bob is not None and tarefa.criado_por_id == bob.id,
              f'criado_por_id={getattr(tarefa, "criado_por_id", None)} bob.id={getattr(bob, "id", None)}')
        check('Tarefa.atualizado_por remapeado para o id novo de alice',
              tarefa is not None and alice is not None and tarefa.atualizado_por_id == alice.id)
        check('Tarefa carimbada com tenant destino',
              tarefa is not None and tarefa.tenant_id == tenant.id,
              f'tenant_id={getattr(tarefa, "tenant_id", None)} destino={tenant.id}')

        projeto = Projeto.objects.first()
        custo = Custo.objects.first()
        check('FK circular Projeto.custos restaurada',
              projeto is not None and custo is not None and projeto.custos_id == custo.id,
              f'custos_id={getattr(projeto, "custos_id", None)} custo.id={getattr(custo, "id", None)}')
        check('Custo.projeto aponta para o projeto migrado',
              custo is not None and projeto is not None and custo.projeto_id == projeto.id)

        com = Comunicacao.objects.first()
        dest_ids = set(com.destinatarios.values_list('id', flat=True)) if com else set()
        check('Comunicacao.destinatarios (M2M) remapeado p/ ids novos',
              alice and bob and dest_ids == {alice.id, bob.id},
              f'dest_ids={dest_ids} esperado={{alice={getattr(alice,"id",None)}, bob={getattr(bob,"id",None)}}}')


def run_idempotency(legacy_path):
    out = StringIO()
    call_command('migrate_legacy_data', legacy_db=legacy_path, tenant=TENANT_NAME, stdout=out)
    text = out.getvalue()
    # Na 2ª execução, total de linhas de negócio migradas deve ser 0.
    check('2ª execução é idempotente (0 linhas de negócio)',
          'total de linhas de negócio migradas: 0' in text,
          'ver relatório')
    # Usuários todos reutilizados.
    check('2ª execução reutiliza usuários (criados=0)',
          'criados=0' in text and 'reutilizados=2' in text)


def main():
    print('=== E2E migrate_legacy_data (shared schema) ===\n')
    legacy_path = tempfile.NamedTemporaryFile(suffix='.sqlite3', delete=False).name
    # Limpa remanescentes de execuções anteriores.
    cleanup_all(None)
    try:
        print('Setup: construindo SQLite legado temporário...')
        build_legacy_db(legacy_path)
        expected = populate_legacy()
        connections[BUILD_ALIAS].close()

        print('Setup: provisionando Client destino descartável...')
        tenant = make_tenant()

        print('Executando migrate_legacy_data...\n')
        out = StringIO()
        call_command('migrate_legacy_data', legacy_db=legacy_path, tenant=TENANT_NAME, stdout=out)
        print(out.getvalue())

        print('Asserções:')
        run_assertions(expected, tenant)
        print('\nIdempotência (2ª execução):')
        run_idempotency(legacy_path)
    finally:
        print('\nTeardown: removendo tenant/usuários/arquivo temp...')
        cleanup_all(legacy_path)

    total = len(_results)
    passed = sum(1 for r in _results if r)
    print(f'\n=== Resultado: {passed}/{total} asserções OK ===')
    if passed != total:
        sys.exit(1)


if __name__ == '__main__':
    main()
