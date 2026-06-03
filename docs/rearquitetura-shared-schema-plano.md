# Plano de Execução — Re-arquitetura para Shared Schema + `tenant_id`

> Plano detalhado das fases **R0–R10** decididas em 2026-06-03 (ver
> `backend/codex-task-01.md` → "Revisão de Decisão Arquitetural" e o registro
> da Fase R0 em `docs/backend-multitenant-audit.md`). Este documento é o **passo a
> passo de implementação**; o `codex-task-01.md` mantém o checklist resumido.
>
> Cada fase segue o protocolo do projeto: **executar → validar → registrar no
> audit**. Branch: `Dev-tenant`.

## Alvo da arquitetura (resumo)

- **Um único schema** PostgreSQL (`public`); sem `django-tenants`.
- **`tenant_id` inteiro** (FK para `customers.Client`) em todos os dados de negócio.
- Isolamento **centralizado** num manager/queryset default + RLS de aplicação
  recriada sobre `tenant_id`. PostgreSQL RLS nativo como rede de segurança (R7).
- Tenant da request derivado da **`TenantMembership` ativa** do usuário (sem
  subdomínio). Superuser informa o tenant explicitamente.
- Customização por empresa via **config/feature-flags** (`TenantSettings`); schema
  físico separado só como exceção dura.

## ⚠️ Janela sem isolamento (R1 → R4)

Hoje o isolamento depende inteiramente de `request.tenant.schema_name` (setado
pelo `TenantMainMiddleware`). Ao remover o `django-tenants` (R1):

- `request.tenant` deixa de existir → em `customers/querysets.py` e
  `users/middleware.py`, `schema_name` cai no default `PUBLIC_SCHEMA_NAME` → o
  RLS e o gate de membership **liberam tudo** (ramo de bypass público).
- Ainda não há coluna `tenant_id` (R2) nem filtro por manager (R4): os dados de
  negócio de todas as empresas ficam num único monte **sem separação**.

**Consequência:** entre R1 e R4 **não há isolamento de dados**. É inevitável nesta
migração. Mitigação:

- É branch de desenvolvimento; só existe o tenant `demo`; **sem dados de produção**.
- **Tratar R1–R4 como um bloco único** e **não fazer deploy** antes de R4 concluída
  e validada (isolamento por `tenant_id` ativo e testado).

## Mapa de acoplamento com `django-tenants` (arquivos do projeto)

Levantado por varredura em 2026-06-03 (fora de `venv/` e `migrations/`):

| Arquivo | Acoplamento | Quebra o `check`? | Fase |
| --- | --- | --- | --- |
| `planify/settings.py` | app, middleware, engine, router, `TENANT_MODEL`/`TENANT_DOMAIN_MODEL` | — | R1 |
| `customers/models.py` | `Client(TenantMixin)`, `Domain(DomainMixin)` | **Sim** (import nível módulo) | R1 |
| `customers/admin.py` | importa/registra `Domain`, colunas `schema_name` | **Sim** (admin carrega no check) | R1 |
| `customers/querysets.py` | `request.tenant.schema_name`, `PUBLIC_SCHEMA_NAME` | Não (runtime) | R3/R4 |
| `users/middleware.py` | `request.tenant.schema_name`, `PUBLIC_SCHEMA_NAME` | Não (runtime) | R3/R4 |
| `customers/management/commands/create_dev_tenant.py` | importa `Domain`, usa `schema_name` | Não (lazy) | R9 |
| `customers/management/commands/provision_tenant.py` | importa `Domain`, cria `Domain` | Não (lazy) | R9 |
| `customers/management/commands/migrate_legacy_data.py` | `django_tenants.utils` (schema_context) | Não (lazy) | R6 |
| `customers/emails.py` | usa `tenant.schema_name` p/ montar URL | Não (runtime) | R3/R9 |
| `seed_data.py` | `schema_context`, `get_tenant_model` | Não (script) | R6 |
| `scripts/e2e_*.py` (3) | `schema_context`, `Domain` | Não (scripts) | R8 |
| `tests/tenant_base.py` | `TenantTestCase` | **Sim** (coleta pytest) | R8 |

> Para manter `manage.py check` verde ao fim do R1, basta tratar os três marcados
> "Sim": `settings.py`, `customers/models.py`, `customers/admin.py`. O restante é
> runtime/scripts e é endereçado nas fases indicadas. A suíte `pytest` fica
> vermelha até R8 (a base importa `TenantTestCase`); é esperado e documentado.

---

## Fase R1 — Desativar `django-tenants` (banco único)

**Objetivo:** o projeto roda num único schema PostgreSQL, sem `django-tenants`,
com `manage.py check` e `migrate` verdes. Isolamento **intencionalmente desligado**
até R4.

### Passos

1. **`planify/settings.py`**
   - Remover o `SHARED_APPS.insert(0, 'django_tenants')`.
   - Colapsar `SHARED_APPS` + `TENANT_APPS` num único `INSTALLED_APPS` explícito
     (manter todos os apps; `django.contrib.contenttypes` uma vez só). Pode-se
     manter as listas como documentação, mas o `INSTALLED_APPS` efetivo deixa de
     depender da divisão shared/tenant.
   - Remover `TenantMainMiddleware` do `MIDDLEWARE` (o `insert(0, ...)`).
   - Trocar o engine do banco: `django_tenants.postgresql_backend` →
     `django.db.backends.postgresql`.
   - Remover `DATABASE_ROUTERS` (`TenantSyncRouter`) — deixar vazio/omitir.
   - Remover `TENANT_MODEL`, `TENANT_DOMAIN_MODEL`, `SHOW_PUBLIC_IF_NO_TENANT_FOUND`.
   - **Manter** `PUBLIC_SCHEMA_NAME = 'public'` como constante simples
     (querysets/middleware ainda a referenciam; mantê-la evita `AttributeError`
     enquanto o ramo de bypass público é o comportamento temporário até R3/R4).
   - Simplificar os blocos `if not USE_SQLITE:` que existiam só para o
     `django-tenants` (engine/route/middleware passam a ser únicos).

2. **`customers/models.py`**
   - `class Client(TenantMixin)` → `class Client(models.Model)`. Manter `name`,
     `paid_until`, `on_trial`, `created_on`. Remover `auto_create_schema`.
     - Decisão (2026-06-03): **remover** `schema_name` (vinha do `TenantMixin`) —
       não há mais schema por tenant. A migração gera `RemoveField('schema_name')`
       em `Client`.
   - **Remover** o model `Domain` (sem resolução por host).
   - Remover o import `from django_tenants.models import DomainMixin, TenantMixin`.

3. **`customers/admin.py`**
   - Remover `DomainInline`, `@admin.register(Domain)` e o import de `Domain`.
   - Remover `schema_name` de `list_display`/`search_fields` do `ClientAdmin` e dos
     demais admins (`search_fields` com `tenant__schema_name`).

4. **Migração**
   - `makemigrations customers` deve gerar: `RemoveField` de `schema_name` (e afins
     do `TenantMixin`) em `Client`, `DeleteModel` de `Domain`, e ajuste de bases.
   - Conferir a migração gerada manualmente (mudança de base + delete de tabela).
   - Como o banco de dev tem schemas de tenant (`demo`) criados pelo
     `django-tenants`, o caminho limpo é **recriar o banco de dev** após o R1
     (drop/recreate) e rodar `migrate`. Os dados do `demo` são re-semeados (sem
     valor a preservar agora; a migração de dados real é a R6).

5. **Comando de migração operacional**
   - Passa a ser `python manage.py migrate` (não mais `migrate_schemas --shared`).
   - Atualização de README/ONBOARDING fica para R10; anotar no audit.

### Validação (gate do R1)

- `manage.py check` sem issues.
- `makemigrations` gera a migração esperada; `migrate` aplica em banco limpo.
- App sobe; `/admin/` carrega e lista `Client`/`TenantMembership`/`TenantInvitation`.
- **Não** validar isolamento (desligado até R4) — registrar isso explicitamente.

### Fora de escopo (adiado)

`tenant_id` (R2), resolução de tenant (R3), manager/RLS (R4), commands/emails
(R9), scripts/testes (R8). `pytest` fica vermelho até R8 — esperado.

### Riscos

- **Isolamento desligado** R1–R4: não fazer deploy.
- Histórico de migração com `django-tenants`: preferir recriar o banco de dev.
- Imports nível-módulo escondidos (admin) — cobertos acima; rodar `check` confirma.

---

## Fase R2 — `tenant_id` nos models de negócio

**Objetivo:** toda tabela de negócio passa a ter `tenant_id` (FK inteiro para
`Client`), com índices e uniques reescopados — seguindo o playbook seguro.

### Passos (playbook: nullable → backfill → NOT NULL + FK)

1. Em cada model de `projects`, `tasks`, `teams`, `risks`, `costs`, `documents`,
   `communications`: adicionar
   `tenant = models.ForeignKey('customers.Client', on_delete=models.PROTECT, null=True)`
   (temporariamente `null=True`).
2. Migração de dados (data migration) de **backfill**: como hoje os dados vivem em
   schemas, o `tenant_id` de cada linha vem do tenant de origem (só `demo`). Em
   banco já consolidado, atribuir o `Client` correspondente.
3. Segunda migração: alterar para `null=False` (após backfill garantido).
4. **Índices compostos** começando por `tenant_id`: revisar `Meta.indexes` e
   `ordering` mais usados → `models.Index(fields=['tenant', <campos>])`.
5. **Uniques por tenant**: trocar `unique=True` global por `UniqueConstraint`
   com `tenant`. Ex. concreto: `projects.Projeto.titulo` (`unique=True`) →
   `UniqueConstraint(fields=['tenant', 'titulo'], name='uniq_projeto_titulo_por_tenant')`.
   Auditar todos os `unique=True`/`unique_together` dos 7 apps.

### Validação

- `makemigrations`/`migrate` ok; backfill confere contagens; nenhum `tenant_id`
  nulo ao fim; uniques aceitam título repetido entre tenants distintos.

### Riscos

- `on_delete=PROTECT` evita apagar empresa com dados; confirmar que é o desejado.
- FKs circulares já conhecidas (`Projeto.custos ↔ Custo`) não afetam `tenant_id`,
  mas o backfill deve cobrir ambos.

---

## Fase R3 — Resolução de tenant por membership (sem subdomínio)

**Objetivo:** definir o tenant da request a partir do usuário autenticado, sem
host/subdomínio.

### Passos

1. Middleware/util (substitui o papel do `TenantMainMiddleware`): após a auth,
   resolver a `TenantMembership` **ativa** do `request.user` e setar
   `request.tenant` (o `Client`) e `request.tenant_id`.
2. Superuser: aceitar tenant explícito via header (ex. `X-Tenant-Id`) ou query
   param para operação global; sem isso, sem tenant (acesso operacional).
3. Ajustar `customers/querysets.py` e `users/middleware.py` para usar
   `request.tenant`/`tenant_id` resolvido (parar de depender de `schema_name`).
4. `customers/emails.py`: URL de convite deixa de usar `schema_name`/subdomínio →
   usar domínio único do app + token.

### Validação

- Usuário com membership ativa → `request.tenant` correto; sem membership → sem
  tenant (e gate de R4 nega). Superuser com header → tenant alvo.

---

## Fase R4 — Isolamento centralizado (manager/queryset) + RLS

**Objetivo:** garantir que **nenhuma** query de negócio escape do filtro por
`tenant_id`, de forma central. É o passo 5 do playbook.

### Passos

1. **Manager/QuerySet default** nos models de negócio: filtra automaticamente por
   `request.tenant_id` (via util de contexto de request, ex. thread-local ou
   passagem explícita pelo viewset). Set automático de `tenant_id` no `create`.
2. **Mixin de viewset** (evoluir o atual `TenantRLSQuerysetMixin`): injeta o
   filtro de tenant + aplica a RLS por papel.
3. **Recriar `apply_tenant_rls`/`apply_member_rls`** sobre `tenant_id` (hoje
   assumem schema). Manter a matriz de papéis (`owner/admin/manager/viewer` =
   tenant inteiro; `member` = recursos ligados a ele; sem membership = vazio;
   superuser = bypass com tenant explícito).
4. **Auditoria**: varrer `.objects` cru, `raw()`, agregações e `values()` nos 7
   apps + `core` (dashboards) e garantir que passam pelo manager/filtro. Listar e
   corrigir cada escape.

### Validação

- Dois tenants com dados homônimos: tenant A nunca vê dados de B em nenhum
  endpoint (lista, detalhe, agregação). `member` vê só o que é dele. Recriar o
  e2e cross-tenant equivalente (agora por `tenant_id`).

### Marco

- **Fim do R4 = isolamento restabelecido.** Só aqui o sistema volta a ser seguro
  para deploy.

---

## Fase R5 — Customização por tenant (config/feature-flags)

**Objetivo:** regras de negócio diferentes por empresa sem schema separado.

### Passos

- Model `TenantSettings` (1-1 com `Client`) ou campos/JSON de flags no `Client`.
- Ponto único de leitura das flags no código de negócio.
- Documentar que schema físico separado é exceção dura (contrato/lei), tratada
  caso a caso, não design padrão.

---

## Fase R6 — Migração de dados (schemas → shared)

**Objetivo:** trazer dados dos schemas existentes para as tabelas compartilhadas
com `tenant_id` populado.

### Passos

- Script/comando que lê cada schema de tenant e insere nas tabelas shared
  carimbando `tenant_id`. Custo baixo (sem produção; só `demo`).
- Reescrever/aposentar `migrate_legacy_data.py` para o novo alvo (sem
  `schema_context`); manter dedup de identidade global e remapeamento de FKs.
- Atualizar `seed_data.py` para o modelo shared (sem `schema_context`).

### Validação

- Contagens antes/depois por tabela; `tenant_id` correto; idempotência;
  plano de rollback (banco único — backup/restore padrão).

---

## Fase R7 — PostgreSQL RLS nativo (rede de segurança)

**Objetivo:** segunda camada de isolamento no banco, independente da aplicação.

### Passos

- Habilitar `ROW LEVEL SECURITY` nas tabelas de negócio; policy
  `tenant_id = current_setting('app.tenant_id')`.
- Setar `app.tenant_id` por conexão/transação a partir do tenant da request.
- Validar que mesmo uma query sem filtro de aplicação não vaza entre tenants.

> Opcional/posterior: só depois dos contratos de R4 estáveis.

---

## Fase R8 — Testes

**Objetivo:** suíte e e2e validando isolamento por `tenant_id` (sem schema/host).

### Passos

- Reescrever `tests/tenant_base.py` sem `TenantTestCase` (banco único; criar
  `Client` + `TenantMembership` + JWT; tenant resolvido por membership).
- Reescrever os `scripts/e2e_*.py` para o modelo shared (sem `Domain`/schema).
- Cobrir: dois tenants, dados homônimos, negação cross-tenant, `member` restrito,
  superuser com tenant explícito.

### Validação

- `pytest tests/` verde; e2e de isolamento cross-tenant verde.

---

## Fase R9 — Provisionamento e convites

**Objetivo:** provisionar empresa sem criar schema/domínio.

### Passos

- `provision_tenant`: cria só a linha `Client` + owner + `TenantMembership`
  (sem `Domain`/schema).
- `create_dev_tenant`: idem (conveniência dev).
- Convites (`TenantInvitation`): fluxo mantido; URL de aceite sem subdomínio.

### Validação

- Provisionar empresa + convidar + aceitar + acessar, tudo num schema único.

---

## Fase R10 — Docs e onboarding

**Objetivo:** documentação coerente com o modelo shared.

### Passos

- Atualizar `ONBOARDING.md`, `backend/readme-backend.md` e
  `docs/multi-tenant-architecture.md` (de schema-per-tenant para shared +
  `tenant_id`; comandos `migrate` em vez de `migrate_schemas`; sem subdomínio).
- Atualizar o `docs/backend-multitenant-audit.md` com o fechamento de cada fase R.

---

## Ordem de execução e marcos

1. **R1 → R2 → R3 → R4** como um bloco (sem deploy no meio; isolamento volta no R4).
2. R5 (customização) e R6 (migração de dados) na sequência.
3. R7 (RLS nativo) opcional, após contratos estáveis.
4. R8 (testes) acompanha R4–R6; fechar antes de considerar a re-arquitetura pronta.
5. R9 e R10 finalizam operação e documentação.

## Critérios de aceite (re-arquitetura)

- [ ] `manage.py check` e `migrate` (banco único) verdes.
- [ ] `tenant_id NOT NULL` em todos os models de negócio; uniques por tenant.
- [ ] Nenhuma query de negócio escapa do filtro central por `tenant_id`.
- [ ] Dois tenants coexistem; dados de A não aparecem para B (testado).
- [ ] `member` restrito aos próprios recursos; superuser opera com tenant explícito.
- [ ] Provisionamento/convites funcionam sem schema/subdomínio.
- [ ] Docs (ONBOARDING/readme/arquitetura) atualizados.
