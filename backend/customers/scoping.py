"""Carimbo automático de ``tenant_id`` no create (R4).

O ``TenantManager`` garante a **leitura** escopada; este módulo garante a
**escrita**: um ``pre_save`` que preenche ``tenant_id`` a partir do contexto da
request quando a instância ainda não o tem. Cobre todos os caminhos de criação —
``serializer.save()``, ``perform_create``, ``Model.objects.create()``, admin e
shell dentro de ``context.scope(...)`` — sem depender de cada viewset lembrar de
setar o campo.

Regras:

- Só carimba quando ``tenant_id`` está ausente (nunca sobrescreve um valor já
  definido — ex.: criação explícita com tenant em scripts/migração R6).
- Só carimba dentro de um contexto ativo e não-bypass com tenant resolvido. Em
  bypass administrativo (`/admin/`/ferramentas internas), a criação de dado de
  negócio exige tenant explícito;
  sem ele a FK NOT NULL falha — comportamento desejado (não adivinhamos o tenant).
"""
from django.apps import apps
from django.db.models.signals import pre_save

from customers import context

# (app_label, model_name) dos 26 models de negócio com FK ``tenant`` (R2).
TENANT_SCOPED_MODELS = (
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
)


def stamp_tenant(sender, instance, **kwargs):
    if getattr(instance, 'tenant_id', None) is not None:
        return
    if not context.is_active() or context.is_bypass():
        return
    tenant_id = context.get_tenant_id()
    if tenant_id is not None:
        instance.tenant_id = tenant_id


def register():
    """Conecta o ``pre_save`` de carimbo a cada model de negócio."""
    for app_label, model_name in TENANT_SCOPED_MODELS:
        model = apps.get_model(app_label, model_name)
        pre_save.connect(
            stamp_tenant,
            sender=model,
            dispatch_uid=f'tenant_stamp_{app_label}_{model_name}',
        )
