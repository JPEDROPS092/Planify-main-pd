"""R7 — RLS nativo do PostgreSQL (rede de segurança no banco).

Habilita ``ROW LEVEL SECURITY`` (com ``FORCE``) nas 26 tabelas de negócio e cria
uma policy ``FOR ALL`` (USING + WITH CHECK) por tabela, escopada à GUC de sessão
``app.current_tenant`` que o ``TenantDatabaseRLSMiddleware`` seta por transação a
partir do tenant resolvido (fonte confiável: o JWT, nunca o frontend).

Semântica da GUC:

- ``''`` (string vazia)  -> bypass administrativo interno, todas as linhas.
- ``'<id>'``            -> apenas o tenant ``<id>``.
- ``'-1'`` / não setada -> nenhuma linha (deny-by-default / fail-closed).

As tabelas ``customers_*`` (membership/invitation/settings) **não** recebem RLS:
a resolução do tenant consulta ``TenantMembership`` antes de a GUC existir, e a
infra de tenancy precisa ser legível para administração de plataforma.

Só tem efeito quando a app conecta como uma role **sem** ``BYPASSRLS`` e que não
seja superuser nem dona das tabelas (ver ``manage.py setup_rls`` → ``app_user``).
``planify`` (superuser) continua ignorando o RLS — por isso migrations/seed/testes
seguem funcionando por essa conexão.
"""
from django.db import migrations

# (app_label, model_name) das 26 tabelas de negócio (mesmo conjunto de
# customers.scoping.TENANT_SCOPED_MODELS). Inline para a migração ser autocontida.
TENANT_TABLES = [
    ('projects', 'Projeto'),
    ('projects', 'MembroProjeto'),
    ('projects', 'HistoricoStatusProjeto'),
    ('projects', 'Sprint'),
    ('tasks', 'Tarefa'),
    ('tasks', 'AtribuicaoTarefa'),
    ('tasks', 'ComentarioTarefa'),
    ('tasks', 'HistoricoStatusTarefa'),
    ('teams', 'Equipe'),
    ('teams', 'MembroEquipe'),
    ('teams', 'PermissaoEquipe'),
    ('risks', 'Risco'),
    ('risks', 'HistoricoRisco'),
    ('costs', 'Categoria'),
    ('costs', 'Custo'),
    ('costs', 'OrcamentoProjeto'),
    ('costs', 'OrcamentoTarefa'),
    ('costs', 'Alerta'),
    ('documents', 'Documento'),
    ('documents', 'HistoricoDocumento'),
    ('documents', 'Comentario'),
    ('communications', 'ChatMensagem'),
    ('communications', 'ChatMensagemLeitura'),
    ('communications', 'Notificacao'),
    ('communications', 'ConfiguracaoNotificacao'),
    ('communications', 'Comunicacao'),
]

POLICY = 'tenant_isolation'

# tenant_id é bigint. GUC '' => global; '<id>' => só o tenant; '-1'/ausente => nada.
PREDICATE = (
    "current_setting('app.current_tenant', true) = '' "
    "OR tenant_id = NULLIF(current_setting('app.current_tenant', true), '')::bigint"
)


def enable_rls(apps, schema_editor):
    for app_label, model_name in TENANT_TABLES:
        table = apps.get_model(app_label, model_name)._meta.db_table
        q = schema_editor.quote_name(table)
        schema_editor.execute(f'ALTER TABLE {q} ENABLE ROW LEVEL SECURITY')
        schema_editor.execute(f'ALTER TABLE {q} FORCE ROW LEVEL SECURITY')
        schema_editor.execute(f'DROP POLICY IF EXISTS {POLICY} ON {q}')
        schema_editor.execute(
            f'CREATE POLICY {POLICY} ON {q} '
            f'USING ({PREDICATE}) WITH CHECK ({PREDICATE})'
        )


def disable_rls(apps, schema_editor):
    for app_label, model_name in TENANT_TABLES:
        table = apps.get_model(app_label, model_name)._meta.db_table
        q = schema_editor.quote_name(table)
        schema_editor.execute(f'DROP POLICY IF EXISTS {POLICY} ON {q}')
        schema_editor.execute(f'ALTER TABLE {q} NO FORCE ROW LEVEL SECURITY')
        schema_editor.execute(f'ALTER TABLE {q} DISABLE ROW LEVEL SECURITY')


class Migration(migrations.Migration):

    dependencies = [
        ('customers', '0005_tenantsettings'),
        ('projects', '0003_historicostatusprojeto_tenant_membroprojeto_tenant_and_more'),
        ('tasks', '0003_atribuicaotarefa_tenant_comentariotarefa_tenant_and_more'),
        ('teams', '0002_equipe_tenant_membroequipe_tenant_and_more'),
        ('risks', '0002_historicorisco_tenant_risco_tenant_and_more'),
        ('costs', '0003_alerta_tenant_categoria_tenant_custo_tenant_and_more'),
        ('documents', '0002_comentario_tenant_documento_tenant_and_more'),
        ('communications', '0004_chatmensagem_tenant_chatmensagemleitura_tenant_and_more'),
    ]

    operations = [
        migrations.RunPython(enable_rls, disable_rls),
    ]
