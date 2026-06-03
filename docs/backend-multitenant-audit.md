# Auditoria da Refatoração Multi-Tenant do Backend

Este documento deve ser atualizado sempre que uma fase da `backend/codex-task-01.md` for concluída ou quando uma fase avançar com ressalvas relevantes.

> **⚠️ Revisão de decisão arquitetural (2026-06-03).** A estratégia de isolamento
> foi alterada de **schema-per-tenant (`django-tenants`)** para **shared schema +
> `tenant_id`** (FK inteiro para `customers.Client`). As Fases 4–8 abaixo
> permanecem como **registro histórico** do caminho percorrido, mas o isolamento
> físico por schema dos dados de negócio será **substituído** pela camada
> `tenant_id`, com isolamento centralizado em manager/queryset e RLS de aplicação
> recriada. Resolução de tenant **sem subdomínio** (via `TenantMembership` ativa).
> Customização por empresa via config/feature-flags; schema físico separado só
> como exceção dura. Plano completo em `backend/codex-task-01.md` ("Revisão de
> Decisão Arquitetural" + "Plano da Re-arquitetura para Shared Schema", fases
> R0–R10). O acompanhamento das fases `R` é feito na seção "Registros".

## Protocolo de atualização

Para cada fase concluída, registrar:

- Data local da conclusão.
- Branch usada.
- Arquivos principais alterados.
- Comandos executados.
- Resultado da validação.
- Evidências objetivas.
- Pendências ou ressalvas.

## Status resumido

| Fase | Status | Observação |
| --- | --- | --- |
| Fase 0: Preparação e Baseline | Concluída com ressalvas | Baseline, backup e falhas conhecidas registrados. Dump de dados não foi gerado porque não houve confirmação de dados importantes além do SQLite local. |
| Fase 1: Review Completo do Banco e dos Domínios | Concluída | Review documentado em `docs/database-review.md`. |
| Fase 2: Desenho da Nova Arquitetura | Concluída inicialmente | Arquitetura documentada em `docs/multi-tenant-architecture.md`; pode evoluir após permissões e testes. |
| Fase 3: Migração para PostgreSQL | Concluída com ressalvas | PostgreSQL local via Docker validado. Testes automatizados foram adiados por decisão do projeto até refazer contratos. |
| Fase 4: Introdução do django-tenants | Concluída inicialmente | `django-tenants`, tenant demo e migrations shared/tenant validados. |
| Fase 5: Classificação e Movimentação dos Apps | Concluída | `SHARED_APPS`/`TENANT_APPS` configurados; revisão de imports shared↔tenant, views/querysets e admin concluída. Override de admin index do app shared `core` (que consultava models tenant e quebrava `/admin/` no public) removido; admin valida 200 em public e tenant. |
| Fase 6: Membership, Permissões e Isolamento | Parcial validada | `TenantMembership`, roles, bloqueio `403`, remoção do bypass global por `User.role == ADMIN` e RLS de aplicação em querysets principais validados parcialmente. |
| Fase 7: Refatoração de Autenticação | Concluída inicialmente | ADR `docs/adr-0001-auth-multitenant.md`. Djoser+JWT mantidos; provisionamento de owner por superuser e fluxo de convite implementados e validados (e2e 13/13). |
| Fase 8: Migração de Dados Existentes | Concluída | Comando `migrate_legacy_data` (idempotente, com `--dry-run` e relatório de contagens), validado por e2e sintético (22/22) e executado contra o SQLite legado real (1 superusuário migrado para o `public`). Plano de rollback documentado. |
| Fase 9: Testes | Não iniciada | Suite será refeita após contratos multi-tenant. |
| Fase 10: Admin, Docs e Operação | Parcial | README e comando de criação de tenant adicionados; guia completo de operação ainda pendente. |
| Fase 11: Observabilidade e Segurança | Não iniciada | Logs com tenant, auditoria e hardening pendentes. |
| Fase 12: Frontend e Integração | Não iniciada | Integração por subdomínio ainda pendente. |
| **R0: Registro da decisão (shared schema)** | Concluída | Pivô schema-per-tenant → shared + `tenant_id` registrado. |
| **R1: Desativar `django-tenants` (banco único)** | Concluída | Banco único `public`; `check`/`migrate` verdes; `Domain`/schema removidos. **Isolamento desligado até R4.** |
| **R2: `tenant_id` nos models de negócio** | Concluída | `tenant = FK(customers.Client, CASCADE)` NOT NULL nos 26 models dos 7 apps; `Projeto.titulo` reescopado por tenant; índices compostos `(tenant, …)`; 7 migrations; `check`/`migrate` verdes. **Isolamento ainda desligado até R4.** |
| **R3: Resolução de tenant por membership** | Concluída | `request.tenant`/`tenant_id` resolvidos pela `TenantMembership` ativa (superuser via header `X-Tenant-ID`); `querysets`/`permissions`/`middleware`/`emails` sem `schema_name`/`.domains`; validado 9/9. **Filtro real por `tenant_id` ainda é R4.** |
| **R4: Isolamento centralizado (manager/queryset) + RLS** | Concluída | `TenantManager` (contexto thread-local por request) filtra `tenant_id` em toda query `.objects` de runtime nos 26 models; `pre_save` carimba `tenant_id` no create; `apply_tenant_rls` aplica o limite duro de tenant na camada de viewset (queryset de classe não passa pelo manager) + RLS por papel preservada; middleware ativa/limpa o contexto (deny-by-default, bypass admin/superuser-global). e2e 16/16. **Isolamento restabelecido.** Rede de segurança no banco (RLS nativo) é a R7. |
| **R5: Customização por tenant (config/feature-flags)** | Concluída | `customers.TenantSettings` (1-1 com `Client`, JSON `features`/`config`); ponto único de leitura `customers.config.get_tenant_settings`/`tenant_feature_enabled`; auto-criação via `post_save` em `Client`; admin. `migrations/0005`. Schema físico separado documentado como exceção dura. |
| **R6: Migração de dados (schemas → shared)** | Concluída | `seed_data.py` e `migrate_legacy_data.py` reescritos para o shared schema (sem `schema_context`/`get_tenant_model`); tenant resolvido por `Client` (nome/id), negócio gravado no schema único carimbando `tenant_id` (seed via `context.scope`; migração via carimbo explícito + colisão de PK tenant-aware). Validado: seed → 504 linhas, 0 `tenant_id` nulo/fora do tenant; `migrate_legacy_data --users-only --dry-run` OK. |
| **R7: RLS nativo do PostgreSQL** | Concluída | `ENABLE`+`FORCE ROW LEVEL SECURITY` + policy `tenant_isolation` (`FOR ALL`, USING+WITH CHECK por `app.current_tenant`) nas **26 tabelas de negócio** (`migrations/0006`); `TenantDatabaseRLSMiddleware` faz `SET LOCAL app.current_tenant` por transação a partir do contexto R4; `manage.py setup_rls` cria a role `app_user` (sem `BYPASSRLS`) com CRUD. Validado conectando como `app_user`: 7/7 (isolamento em query crua, `''`=global, deny/fail-closed, WITH CHECK bloqueia troca de tenant). Default segue `planify` (superuser, bypassa); RLS vale ao rodar a web como `app_user`. |
| **R8: Testes** | Concluída | `tests/tenant_base.py` reescrito sem `django-tenants` (`APITestCase` + `Client` + `TenantMembership` + JWT; tenant por membership; cliente restaura o contexto de tenant pós-request). Suíte `pytest tests/` **27 passed**. `scripts/e2e_invitations.py` (13/13) e `scripts/e2e_migrate_legacy.py` (23/23) reescritos p/ shared schema; `e2e_cross_tenant.py` removido (substituído por `e2e_r4_tenant_isolation.py`, 16/16). `e2e_r7_native_rls.py` 7/7. |
| **R9: Provisionamento e convites** | Concluída | `provision_tenant` e `create_dev_tenant` reescritos: criam só a linha `Client` (dispara `TenantSettings` via `post_save`) + owner + `TenantMembership`, sem `Domain`/`schema_name`/`auto_create_schema`. Convites já sem subdomínio desde a R3 (aceite por token em `FRONTEND_URL`). Validado fim-a-fim por `e2e_invitations.py` (provisionar → convidar → aceitar → acessar) e smoke de `create_dev_tenant`. |
| **R10: Docs e onboarding** | Concluída | `ONBOARDING.md`, `backend/readme-backend.md`, `docs/multi-tenant-architecture.md` e `backend/tests/README.txt` atualizados de schema-per-tenant → shared + `tenant_id` (comandos `migrate`/`setup_rls`, sem subdomínio, role `app_user`, provisionamento por `--name`). Fases R0–R10 fechadas neste audit. |

## Registros

### Fase 0: Preparação e Baseline

Data local: 2026-06-01

Branch: `Dev-tenant`

Arquivos/artefatos:

- `docs/backend-baseline.md`
- `backend/backups/db.sqlite3.codex-task-01-baseline`

Comandos executados:

```bash
git branch --show-current
git status --short
./venv/bin/python --version
./venv/bin/python manage.py check
./venv/bin/pytest
cp db.sqlite3 backups/db.sqlite3.codex-task-01-baseline
```

Resultado:

- Branch confirmada: `Dev-tenant`.
- `manage.py check` passou sem issues.
- Backup SQLite criado.
- `pytest` falhou na coleta por testes legados importando `projects.models.Project`, enquanto o model real é `Projeto`.

Evidências:

- Python do virtualenv: `Python 3.12.3`.
- Backup local: `backend/backups/db.sqlite3.codex-task-01-baseline`, tamanho observado `604K`.
- Falhas de teste registradas em `docs/backend-baseline.md`.

Pendências/ressalvas:

- Testes legados não serão corrigidos agora; serão recriados depois com contratos atualizados.
- Dump adicional dos dados não foi feito.

### Fase 1: Review Completo do Banco e dos Domínios

Data local: 2026-06-01

Branch: `Dev-tenant`

Arquivos/artefatos:

- `docs/database-review.md`

Comandos executados:

```bash
rg -n "class .*\(models\.Model\)|ForeignKey|OneToOneField|ManyToManyField|UniqueConstraint|unique_together" backend/*/models.py
```

Resultado:

- Models classificados entre `public`, `tenant` e híbridos.
- Relacionamentos principais documentados.
- Dependências e riscos de migração identificados.

Evidências:

- Usuário global mantido como `users.User`.
- Apps de negócio identificados como tenant: `projects`, `tasks`, `teams`, `risks`, `costs`, `documents`, `communications`.
- Dependência circular relevante registrada: `projects.Projeto -> costs.Custo` e `costs.Custo -> projects.Projeto`.

Pendências/ressalvas:

- `communications` continua híbrido em análise, especialmente notificações e configurações por usuário.

### Fase 2: Desenho da Nova Arquitetura

Data local: 2026-06-01

Branch: `Dev-tenant`

Arquivos/artefatos:

- `docs/multi-tenant-architecture.md`

Resultado:

- Decisão por PostgreSQL + `django-tenants`.
- App de tenants definido como `customers`.
- Models definidos como `Client`, `Domain` e `TenantMembership`.
- Usuário global mantido em `public`.
- Resolução de tenant definida por subdomínio.
- Roles definidas: `owner`, `admin`, `manager`, `member`, `viewer`.

Pendências/ressalvas:

- A política final de superuser em APIs tenant ainda precisa ser formalizada.
- A regra final de notificações globais vs tenant ainda precisa ser fechada.

### Fase 3: Migração para PostgreSQL

Data local: 2026-06-01

Branch: `Dev-tenant`

Arquivos/artefatos:

- `backend/requirements.txt`
- `backend/planify/settings.py`
- `backend/.env.example`
- `compose.yml`
- `backend/readme-backend.md`

Comandos executados:

```bash
./venv/bin/python -m pip install django-tenants psycopg-binary
./venv/bin/python -m pip install psycopg
docker compose up -d postgres
./venv/bin/python manage.py check
./venv/bin/python manage.py makemigrations --check --dry-run
```

Resultado:

- PostgreSQL local subiu via Docker Compose em `127.0.0.1:15432`.
- Django passou a usar PostgreSQL como padrão.
- SQLite ficou disponível apenas como fallback explícito via `USE_SQLITE=True`.
- `manage.py check` passou.
- `makemigrations --check --dry-run` retornou sem mudanças pendentes.

Evidências:

- Pacotes instalados: `django-tenants==3.10.1`, `psycopg==3.3.4`, `psycopg-binary==3.3.4`.
- Docker Compose validado com serviço `planify-postgres`.

Pendências/ressalvas:

- `pytest` não foi executado como critério desta fase por decisão técnica: suite atual será refeita após contratos multi-tenant.

### Fase 4: Introdução do django-tenants

Data local: 2026-06-01

Branch: `Dev-tenant`

Arquivos/artefatos:

- `backend/customers/models.py`
- `backend/customers/admin.py`
- `backend/customers/apps.py`
- `backend/customers/migrations/0001_initial.py`
- `backend/customers/management/commands/create_dev_tenant.py`
- `backend/planify/settings.py`
- `backend/readme-backend.md`
- `docs/multi-tenant-architecture.md`

Comandos executados:

```bash
./venv/bin/python manage.py makemigrations customers
./venv/bin/python manage.py check
./venv/bin/python manage.py migrate_schemas --shared
./venv/bin/python manage.py create_dev_tenant --schema demo --name Demo --domain demo.localhost
./venv/bin/python manage.py migrate_schemas --tenant --schema demo --check
```

Resultado:

- `django-tenants` configurado com:
  - `TENANT_MODEL = 'customers.Client'`
  - `TENANT_DOMAIN_MODEL = 'customers.Domain'`
  - `DATABASE_ROUTERS = ('django_tenants.routers.TenantSyncRouter',)`
  - `TenantMainMiddleware`
- `SHARED_APPS` e `TENANT_APPS` configurados.
- Tenant local `demo.localhost` criado com schema `demo`.
- Migrations shared e tenant validadas.

Evidências:

Schema `public` contém tabelas compartilhadas:

- `users_*`
- `customers_*`
- `auth_*`
- `django_admin_log`
- `django_content_type`
- `django_migrations`
- `django_session`

Schema `demo` contém tabelas de negócio:

- `projects_*`
- `tasks_*`
- `teams_*`
- `risks_*`
- `costs_*`
- `documents_*`
- `communications_*`

Pendências/ressalvas:

- Validar fluxo HTTP real por `demo.localhost`.
- Validar admin no contexto tenant.
- Reduzir verbosidade de SQL logs em desenvolvimento se atrapalhar operação.

### Fase 5: Classificação e Movimentação dos Apps

Data local: 2026-06-01

Branch: `Dev-tenant`

Status: concluída.

Resultado inicial (2026-06-01):

- Apps compartilhados configurados em `SHARED_APPS`.
- Apps de negócio configurados em `TENANT_APPS`.
- Validação estrutural dos schemas confirmou a separação física no PostgreSQL.
- Referências antigas a `Projeto.name` corrigidas para `Projeto.titulo` em serializers e mensagens de alerta.

Comandos executados:

```bash
rg -n "projeto\.name|tarefa\.projeto\.name" backend -g '*.py'
./venv/bin/python manage.py check
./venv/bin/python manage.py makemigrations --check --dry-run
```

Resultado:

- Nenhuma ocorrência restante de `projeto.name` ou `tarefa.projeto.name`.
- `manage.py check` passou.
- `makemigrations --check --dry-run` retornou sem mudanças pendentes.

Encerramento (2026-06-02): revisão fina concluída.

- **Imports shared ↔ tenant**: auditados todos os apps shared (`users`, `core`,
  `customers`). O único acoplamento shared→tenant era em `core`
  (`views.py`, `services.py`, `admin.py` importando `Projeto`/`Tarefa`/`Risco`/
  `Custo`). Imports em si não tocam o banco; o que importa é o schema em runtime.
  - `core/views.py` (dashboards): já tratado na Fase 6 (`apply_tenant_rls`) e os
    endpoints estão sob prefixos tenant-scoped
    (`/api/dashboard/`, `/api/user/dashboard/`, `/api/projects/.../metrics/`),
    então no schema public o `PermissionMiddleware` devolve `403` antes da query.
  - Apps tenant importando apps tenant (`tasks→projects`, `costs→projects/tasks`,
    `documents`/`risks`/`communications→projects/tasks`): correto, todos no mesmo
    escopo de schema.
- **Admin** (entregável "admin sem erro de registro ou schema"): `core/admin.py`
  sobrescrevia `admin.site.index` agregando métricas de `Projeto`/`Tarefa` a cada
  carga do admin. Como `core` é app SHARED e `/admin/` não é tenant-scoped,
  acessar pelo host público (schema public) quebrava a página inicial com
  `ProgrammingError` (tabelas tenant inexistentes no public). Além disso, o
  template do admin não renderizava nenhuma das variáveis de contexto produzidas
  — era código morto. O override foi **removido**. As métricas de negócio
  permanecem nos endpoints de dashboard tenant-scoped de `core/views.py`.
  - Bug de queryset latente no mesmo override (`Tarefa.objects.filter(status='concluida')`,
    valor inexistente nos choices — o correto é `FEITO`) eliminado junto.
- **Registros de admin dos apps tenant**: `@admin.register(...)` é lazy (não
  consulta o banco no import); os contadores em métodos de exibição
  (`projects/admin.py`, `users/admin.py`) rodam por linha no schema da
  requisição. Sem ajuste necessário.
- **Signals/managers/`.using()`**: nenhum `signals.py`; o único `ready()`
  (`users/apps.py`) só carrega OpenAPI e config de admin; nenhum manager custom
  em apps tenant; nenhum `.using()`/`connections[...]` hardcoded em apps de
  negócio (o único uso de `.using()` é intencional, no comando da Fase 8).

Validação (2026-06-02):

- `manage.py check`: sem issues.
- `/admin/` com superusuário autenticado: **200** tanto em `localhost` (public)
  quanto em `demo.localhost` (tenant); changelist de model tenant
  (`/admin/projects/projeto/`) **200** no host do tenant.
- Comportamento esperado documentado: dados de models tenant são administrados
  pelo **domínio do tenant** (no host público as tabelas tenant não existem, como
  é próprio do django-tenants).
- Regressão: `scripts/e2e_cross_tenant.py` 9/9; `scripts/e2e_invitations.py` 13/13;
  `scripts/e2e_migrate_legacy.py` 22/22.

### Fase 6: Membership, Permissões e Isolamento

Data local: 2026-06-01

Branch: `Dev-tenant`

Status: concluída.

Encerramento (2026-06-01): o objetivo da fase — isolamento multi-tenant com
membership e autorização por papel — está implementado e validado de ponta a
ponta. Resumo do que fecha a fase:

- `TenantMembership` + matriz de papéis (owner/admin/manager/member/viewer).
- Gate de membership no `PermissionMiddleware` para rotas tenant-scoped; bypass
  apenas para `is_superuser`.
- RLS de aplicação (`apply_tenant_rls`/`apply_member_rls`) nos viewsets e em
  queries manuais relevantes.
- Regra "um usuário = uma empresa" (constraint parcial + `clean()`).
- Vazamento cross-tenant via `users.User` (model shared) corrigido
  (`tenant_users_queryset`).
- `seed_data.py` multi-tenant; management commands revisados.
- Permissão DRF reutilizável `customers.permissions.IsTenantMember`.
- Teste HTTP ponta-a-ponta de negação cross-tenant (`scripts/e2e_cross_tenant.py`,
  9/9) e suíte de API migrada para o stack multi-tenant real (27 passed).

Follow-up (escopo de fase futura, não bloqueia o fechamento da Fase 6):

- Autorização a nível de objeto / por entidade (ex.: `member` editar apenas a
  tarefa atribuída a ele, não qualquer tarefa do projeto que acessa). É
  refinamento de regra de produto sobre a base de isolamento já estabelecida.

Resultado até agora:

- Criado `customers.TenantMembership`.
- Roles iniciais criadas:
  - `owner`
  - `admin`
  - `manager`
  - `member`
  - `viewer`
- Middleware de permissão agora exige membership ativa para caminhos tenant-scoped quando o schema atual não é `public`.
- Prefixos protegidos configurados em `TENANT_MEMBERSHIP_REQUIRED_PATH_PREFIXES`.
- Apenas `is_superuser=True` mantém bypass global.
- `users.User.role == ADMIN` não concede mais bypass global.
- Implementada camada inicial de RLS de aplicação em `customers.querysets`.
- ViewSets principais passaram a aplicar `TenantRLSQuerysetMixin` em `get_queryset`.
- Actions/relatórios em `projects`, `tasks`, `teams`, `risks`, `costs`, `documents`, `communications` e dashboards em `core` passaram a aplicar `apply_tenant_rls` em queries manuais relevantes antes de agregações, serialização, exclusões ou updates em massa.
- Corrigidas actions de riscos que usavam `request` sem declará-lo na assinatura.
- Corrigidos dashboards legados que consultavam campos inexistentes nos models atuais (`Projeto.gerente`, `Tarefa.responsavel`, `Tarefa.data_fim`).
- Corrigidas anotações de custos para usar os `related_name` atuais (`custos_do_projeto` e `custos_da_tarefa`).
- Para `member`, a leitura de dados de negócio foi reduzida a recursos relacionados ao usuário por autoria, atribuição ou membership de projeto/equipe, conforme o model.
- Matriz inicial por `TenantMembership.role` adicionada:
  - `owner`, `admin`, `manager`: todas as ações nos módulos tenant-scoped.
  - `member`: leitura geral e escrita em tarefas, documentos e comunicações.
  - `viewer`: leitura.

Comandos/testes executados:

```bash
./venv/bin/python manage.py check
./venv/bin/python manage.py makemigrations --check --dry-run
./venv/bin/python -m compileall projects tasks teams risks costs documents communications customers core users
./venv/bin/python manage.py shell -c "<compilação dos 26 querysets de RLS member sem fetch de banco>"
```

Validação técnica adicional em 2026-06-01:

- `manage.py check`: passou sem issues.
- `compileall`: passou para apps tenant/shared principais.
- Compilação ORM dos filtros de `apply_member_rls`: passou para 26 models usando instância `User(id=1)` sem buscar dados no banco.
- Tentativa de validação com fetch real de usuário no PostgreSQL falhou inicialmente por conexão indisponível no sandbox; o container local `planify-postgres` foi confirmado como `healthy`, mas a validação fora do sandbox foi interrompida manualmente. Portanto, ainda falta repetir a validação funcional completa com banco acessível.

Validação de RLS de aplicação:

- Host: `demo.localhost`
- Caminho: `/api/projects/`
- Autenticação: token `Bearer` SimpleJWT.
- Dados criados/atualizados no schema `demo`:
  - `Codex RLS Visible Project`
  - `Codex RLS Hidden Project`
- Usuário `codex_rls_member` com `TenantMembership.role = member` e vínculo apenas no projeto visível:
  - status `200`
  - recebeu apenas `Codex RLS Visible Project`
  - não recebeu `Codex RLS Hidden Project`
- Usuário `codex_rls_manager` com `TenantMembership.role = manager`:
  - status `200`
  - recebeu ambos os projetos.

Teste funcional com `APIClient`:

- Host: `demo.localhost`
- Caminho: `/api/projects/`
- Usuário sem `TenantMembership`: `403`
- Usuário com `TenantMembership` ativa no tenant `demo`: `200`
- Usuário com `users.User.role == ADMIN` sem membership: `403`
- Usuário `viewer` com membership:
  - `GET /api/projects/`: `200`
  - `POST /api/projects/`: `403`
- Usuário `member` com membership:
  - `POST /api/projects/`: `403`
- Usuário `manager` com membership:
  - `POST /api/projects/` com payload vazio: `400`, confirmando que passou pela autorização e falhou na validação da view.
- Usuário `is_superuser=True` sem membership:
  - `GET /api/projects/`: `200`

Continuação em 2026-06-01 (escopo de usuário público em endpoints tenant):

- Auditoria de usos restantes de `.objects` em serializers, services, admin e views identificou que models tenant (`Projeto`, `Tarefa`, etc.) já têm isolamento físico por schema do `django-tenants`; o risco residual de `.objects` direto nesses models é intra-tenant (consistência de RLS por papel), não vazamento cross-tenant.
- Identificado vazamento cross-tenant real via `users.User`, que é model compartilhado (schema `public`): a action `teams.usuarios_disponiveis` listava `User.objects.exclude(...)` sem escopo de tenant, expondo usuários de outras empresas.
- Adicionado helper reutilizável `customers.querysets.tenant_users_queryset(request, base_queryset=None)`, com o mesmo critério de bypass de `apply_tenant_rls` (superuser e schema público veem todos; schema tenant vê apenas usuários com `TenantMembership` ativa no tenant).
- `teams.usuarios_disponiveis` passou a usar `tenant_users_queryset(request).exclude(...)`.
- `projects.adicionar_membro` passou a resolver o usuário-alvo via `tenant_users_queryset(request).get(pk=...)`, de modo que tentar adicionar usuário fora do tenant retorna `404` em vez de permitir vínculo cross-tenant.
- `core/admin.py` (`User.objects.count()` e agregações globais) mantido como está: é dashboard do Django admin, restrito a staff/superuser e global por design.
- Contagens agregadas intra-tenant em `projects/serializers.py` (`get_tasks_count`, `get_progresso`) foram avaliadas e mantidas: refletem totais de projetos/sprints que o membro já acessa, sem vazar dados individuais; eventual restrição por papel é decisão de produto, não de isolamento.

Validação desta continuação em 2026-06-01:

- `manage.py check`: passou sem issues.
- `compileall` de `customers/querysets.py`, `teams/views.py`, `projects/views.py`: passou.
- Validação funcional com PostgreSQL real (container `planify-postgres`, porta `127.0.0.1:15432`): criados dois tenants (`val_a`, `val_b`) com schemas e usuários membros distintos. Resultados:
  - Usuário membro do tenant A via `tenant_users_queryset`: recebeu apenas o usuário de A; não recebeu o usuário de B.
  - Usuário membro do tenant B: simétrico, sem vazamento.
  - Superuser no tenant A: recebeu todos os usuários (bypass operacional confirmado).
  - Schema público: recebeu todos os usuários (sem escopo, conforme esperado).
  - Dados de teste (`val_*`, schemas `val_a`/`val_b`) removidos do banco de desenvolvimento após a validação.

Continuação em 2026-06-01 (seed e management commands):

- Revisão dos management commands:
  - `customers/create_dev_tenant`: opera apenas sobre models compartilhados (`Client`, `Domain`, `TenantMembership`) no schema `public`; é o caminho legítimo de provisionamento de tenant. Sem ajuste.
  - `users/create_access_profiles`: semeia `AccessProfile`/`Permission` legados globais no `public`. Não toca dados tenant nem vaza entre empresas; mantido como está enquanto a decisão sobre perfis de acesso por tenant não é fechada.
- `seed_data.py` estava incompatível com o multi-tenant: rodava sem contexto de schema, então as escritas em models tenant caíam no `public` (onde as tabelas de negócio não existem) e eram silenciosamente engolidas pelos `try/except`; além disso não criava `TenantMembership`, o que faria os usuários semeados tomarem `403` nos endpoints tenant.
- `seed_data.py` refatorado em duas fases:
  - Fase compartilhada (`public`): cria usuários/perfis e agora cria `TenantMembership` para cada usuário semeado no tenant alvo, mapeando papel legado → papel tenant (`ADMIN→owner`, `PROJECT_MANAGER→manager`, `TEAM_LEADER→manager`, `TEAM_MEMBER→member`, `STAKEHOLDER→viewer`).
  - Fase tenant: todos os dados de negócio são gravados dentro de `schema_context(<schema>)`.
  - Tenant alvo configurável por `SEED_TENANT_SCHEMA` (default `demo`); se o tenant não existir, o seed aborta com instrução de criação em vez de semear no `public`.
- Validação funcional com PostgreSQL real (tenant `demo`):
  - 7 memberships criadas com os papéis mapeados.
  - Dados de negócio gravados no schema `demo` (ex.: `projects`/`tasks` populados).
  - Confirmado que o schema `public` não possui tabela de projetos (consulta levanta `ProgrammingError`), comprovando que o seed não vaza dados tenant para o schema compartilhado.

Continuação em 2026-06-01 (regra "um usuário = uma empresa"):

- Decisão de produto confirmada: um usuário pertence a uma única empresa e a vários projetos dentro dela. A identidade permanece global (`users.User` no `public`, `email`/`username` únicos globalmente, login único); "um usuário por empresa" é modelado como no máximo uma `TenantMembership` ativa.
- `customers.TenantMembership` ganhou `UniqueConstraint(fields=['user'], condition=Q(is_active=True), name='unique_active_membership_per_user')` e método `clean()` com erro amigável.
- Migração `customers/0002_tenantmembership_unique_active_membership_per_user` criada e aplicada via `migrate_schemas --shared`.
- Dados existentes verificados antes da migração: nenhum usuário com mais de uma membership ativa.
- Validação funcional com PostgreSQL real:
  - `clean()` bloqueia segunda membership ativa (erro de validação).
  - Banco bloqueia segunda membership ativa mesmo sem `clean()` (`IntegrityError` na constraint).
  - Membership inativa em outra empresa permitida (histórico/troca de empresa).
  - Tenant temporário do teste removido.

Arquivos principais alterados nesta etapa parcial:

- `backend/customers/querysets.py`
- `backend/customers/models.py`
- `backend/customers/migrations/0002_tenantmembership_unique_active_membership_per_user.py`
- `backend/seed_data.py`
- `backend/projects/views.py`
- `backend/tasks/views.py`
- `backend/teams/views.py`
- `backend/risks/views.py`
- `backend/costs/views.py`
- `backend/documents/views.py`
- `backend/communications/views.py`

## Permissão DRF reutilizável e teste HTTP ponta-a-ponta (concluído)

- **Permissão DRF `customers.permissions.IsTenantMember`**: encapsula a regra
  "usuário precisa de `TenantMembership` ativa no tenant da requisição" numa
  `BasePermission` declarável por viewset. Mesmo critério de bypass do RLS
  (superuser e schema público liberados). Acompanham `HasTenantRole`
  (fábrica `with_roles(*roles)`) e `IsTenantReader` para casos por papel.
  - O middleware (`PermissionMiddleware.check_tenant_membership`) foi
    refatorado para reutilizar `customers.querysets.get_request_membership`,
    deixando uma única fonte de verdade para a resolução do vínculo,
    compartilhada entre middleware (gate global por prefixo) e permissão DRF
    (gate por view, defesa-em-profundidade).
  - Aplicada explicitamente em `ProjetoViewSet`, `SprintViewSet`,
    `EquipeViewSet`, `MembroEquipeViewSet` e `PermissaoEquipeViewSet`.

- **Teste HTTP ponta-a-ponta**: `backend/scripts/e2e_cross_tenant.py` cria dois
  tenants reais (schemas separados) e exercita o stack HTTP completo
  (`TenantMainMiddleware` por host + JWT + `PermissionMiddleware` + RLS) via
  `django.test.Client` com `HTTP_HOST` por domínio e `Authorization: Bearer`.
  Idempotente e com teardown que dropa schemas/usuários. 9/9 asserções OK:
  - acesso legítimo do dono ao próprio tenant (lista e detalha);
  - **negação cross-tenant** (usuário de A em B → `403` na lista, no detalhe e
    em endpoint de teams);
  - **isolamento por schema** (dono de B não vê projeto de A; pk de A → `404`).

Pendências:
- Revisão de usos restantes de `.objects` concluída para serializers/views/admin/services: models tenant ficam cobertos pelo isolamento físico de schema; o único vazamento cross-tenant real (usuário compartilhado em `teams.usuarios_disponiveis` e `projects.adicionar_membro`) foi corrigido com `tenant_users_queryset`. Resta revisar `seed_data.py` e management commands quanto a escopo de tenant.
- Repetir a compilação ORM dos filtros RLS por model com conexão real ao PostgreSQL e registrar o resultado.
## Migração da suíte de testes para o stack multi-tenant (concluído)

- **Base tenant-aware** em `backend/tests/tenant_base.py`:
  - `TenantAPITestCase` (sobre `django_tenants.test.cases.TenantTestCase`):
    cria um schema de tenant de teste, um usuário com `TenantMembership` ativa
    e um `APIClient` autenticado por **JWT Bearer** e roteado para o **domínio
    do tenant** (`HTTP_HOST`). Substitui `force_authenticate` (que ignorava o
    `PermissionMiddleware`), exercitando o caminho HTTP real
    (`TenantMainMiddleware` + JWT + membership + RLS), idêntico ao do e2e.
  - `SuperuserAPITestCase`: superusuário via JWT para endpoints
    administrativos (`/api/users/`), que dependem de `HasModulePermission`.
- **Suíte canônica `tests/` reescrita e verde** (25 passed, PostgreSQL real):
  teams, projects, tasks, risks, costs, users, documents e communications.
  Além do auth/tenant, os testes legados usavam modelos/campos/rotas
  inexistentes (`Project`/`Task`, `name`/`start_date`, `data_termino`,
  `reverse('project-list')`); foram corrigidos para o contrato atual
  (`Projeto`, `titulo`/`data_inicio`/`data_fim`, `projects:projects-list`,
  `tarefas-list`, etc.). O teste de communications foi reescrito contra o
  contrato vigente (`mensagem`, custom actions de leitura/não-lidas,
  `configuracao-minha-configuracao`), com asserções por existência (robustas a
  paginação) no lugar de contagens exatas.
- **Diretórios de teste duplicados removidos** (`projects/tests`, `costs/tests`,
  `communications/tests`, `documents/tests`): eram scaffold quebrado, não
  coletado pelo pytest (`testpaths=tests`) e sem `__init__.py` (quebravam o
  `manage.py test`). Consolidado em `tests/`; histórico preservado no git.
- **Como rodar**: `pytest tests/ --create-db` (1ª vez) / `--reuse-db` (demais).
  Requer PostgreSQL; não usar `USE_SQLITE=True` (sem django_tenants/schema).
- **Bug corrigido**: `ConfiguracaoNotificacaoViewSet.perform_create` filtrava por
  um campo `tipo` inexistente no model/serializer atual (`ConfiguracaoNotificacao.usuario`
  é `OneToOneField`), causando `FieldError` em **todo POST** de configuração.
  Simplificado para apenas fixar `usuario=request.user` (uma config por usuário;
  duplicatas barradas pelo `UniqueValidator` → `400`). Coberto por
  `test_create_notification_config` e `test_post_config_duplicate_rejected`.
  (Observação menor: o `ConfiguracaoNotificacaoSerializer.create` tem lógica de
  upsert que é inalcançável por causa do `UniqueValidator` — código morto, sem
  impacto funcional; não alterado.)
- Follow-up (fase futura): autorização a nível de objeto / por entidade,
  refinada sobre a nova suíte de testes. Não bloqueia a Fase 6.
- (Concluído) Testes de isolamento: cobertos pelo e2e cross-tenant
  (`scripts/e2e_cross_tenant.py`) e pela suíte de API rodando em tenants reais.

### Fase 7: Refatoração de Autenticação

Data local: 2026-06-01

Branch: `Dev-tenant`

Status: concluída inicialmente.

Decisões formalizadas na ADR `docs/adr-0001-auth-multitenant.md`:

- **Manter Djoser + Simple JWT** nesta fase (não migrar para
  allauth/tenant-users), seguindo a recomendação do plano. Menor risco e sem
  quebra do frontend.
- **Provisionamento de tenant + primeiro owner é do superuser**; o owner popula
  e gerencia a própria empresa e convida os demais membros. Sem self-service de
  criação de empresa no cadastro público.
- **Fluxo de convite** owner/admin → membros, via `customers.TenantInvitation`.

Implementação:

- `customers.TenantInvitation` (modelo compartilhado no `public`): token opaco,
  expiração configurável (`TENANT_INVITATION_TTL_DAYS`), papéis convidáveis
  `admin/manager/member/viewer` (owner é provisionado), constraint de no máximo
  um convite pendente por `(tenant, email)`. Migração `customers/0003`.
- Gestão tenant-scoped (`owner`/`admin`): `TenantInvitationViewSet` em
  `/api/tenant/invitations/` (list/create/retrieve + actions `revoke`/`resend`),
  protegida por `HasTenantRole.with_roles('owner','admin')`. Prefixo `/api/tenant/`
  adicionado a `TENANT_MEMBERSHIP_REQUIRED_PATH_PREFIXES`.
- Aceite público por token: `GET /api/invitations/<token>/` (inspeção) e
  `POST /api/invitations/<token>/accept/` (aceite), liberados em `PUBLIC_PATHS`.
  Aceite cria conta nova **ou** vincula usuário existente sem vínculo ativo,
  respeitando "um usuário = uma empresa" (defesa pela constraint do banco).
- E-mail de convite (`customers/emails.py`) com URL de aceite no domínio do
  próprio tenant.
- Management command `customers/provision_tenant`: cria tenant + domínio +
  conta/designação do owner + `TenantMembership(owner)`; senha temporária
  autogerada quando não informada.
- `TenantInvitation` registrado no admin.

Arquivos principais:

- `backend/customers/models.py` (+ `migrations/0003_tenantinvitation.py`)
- `backend/customers/serializers.py`, `views.py`, `urls.py`, `emails.py`, `admin.py`
- `backend/customers/management/commands/provision_tenant.py`
- `backend/planify/urls.py`, `backend/planify/settings.py`
- `backend/users/permissions.py` (PUBLIC_PATHS)
- `backend/scripts/e2e_invitations.py`
- `docs/adr-0001-auth-multitenant.md`

Validação:

- `manage.py check`: sem issues.
- `migrate_schemas --shared`: `customers.0003` aplicado.
- `scripts/e2e_invitations.py`: 13/13 asserções OK (PostgreSQL real).
- Regressão: `scripts/e2e_cross_tenant.py` 9/9; `pytest tests/` 27 passed.

Pendências/ressalvas:

- Bug pré-existente corrigido: `users/views.py::reset_password` usava
  `User.objects.make_random_password()` (removido no Django 5.1; projeto no 5.2);
  trocado por `get_random_string(12)`.
- Restrição/curadoria do cadastro público (`registro.vue`) é decisão de produto.
- Integração de frontend (tela de gestão de convites, rota de aceite, baseURL
  por subdomínio) fica para a Fase 12, conforme plano de migração na ADR.

### Fase 8: Migração de Dados Existentes

Data local: 2026-06-02

Branch: `Dev-tenant`

Status: concluída.

Objetivo: fazer o *onboarding* do acervo single-tenant legado (SQLite) para o
stack multi-tenant (identidade global no `public`; dados de negócio no schema de
um tenant destino), com contagens antes/depois e plano de rollback.

Diagnóstico do dado legado real (`backend/db.sqlite3`, idêntico ao backup
baseline da Fase 0): **apenas 1 superusuário** (`caio.beniel55@gmail.com`) e
tabelas auto-geradas do Django (`auth_permission`, `django_content_type`,
`django_migrations`). **Nenhum dado de negócio** (0 projetos/tarefas/etc.). Isso
confirma a nota da Fase 0 de que não havia dados de negócio a preservar.

Entregáveis:

- **Comando versionado** `customers/management/commands/migrate_legacy_data.py`:
  - Registra o SQLite legado como conexão `legacy_source` em runtime
    (`sqlite_connection_settings`).
  - **Identidade global → `public`**: copia `users.User` com **dedup por e-mail**
    (usuário já existente é reutilizado, não duplicado) e **preserva o hash de
    senha** (sem re-hash). NÃO preserva PK de usuário — devolve um mapa
    `{id_legado: id_novo}` usado para remapear todas as FKs de negócio.
  - **Satélites do usuário** (`UserProfile`, `PasswordHistory`, `AccessAttempt`):
    copiados sem preservar PK (o `public` é compartilhado e já populado),
    remapeando a FK de usuário, com idempotência por usuário.
  - **RBAC legado** (`AccessProfile`/`Permission`/`UserAccessProfile`): **não
    migrado automaticamente** (configuração global semeada por
    `create_access_profiles`; decisão "global vs por tenant" segue em aberto na
    arquitetura). Reportado como pulado — **nunca dropado**.
  - **Memberships**: cada usuário não-superusuário migrado ganha uma
    `TenantMembership` ativa no tenant destino (mapa de papel legado → papel de
    tenant: `ADMIN→admin`, `PROJECT_MANAGER/TEAM_LEADER→manager`,
    `TEAM_MEMBER→member`, `STAKEHOLDER/AUDITOR→viewer`; `owner` é provisionado,
    não migrado). Superusuário não recebe membership (bypass global). Respeita
    "um usuário = uma empresa".
  - **Dados de negócio → schema do tenant**: copiados em ordem de dependência de
    FK, **preservando PK e timestamps** (`save_base(raw=True)`), remapeando FKs e
    M2M de usuário. A dependência circular `projects.Projeto.custos → costs.Custo`
    é resolvida com gravação diferida (projeto entra com `custos=NULL` e é
    atualizado após os custos).
  - **Idempotente**: linhas de negócio cujo PK já existe no destino são puladas;
    re-rodar é no-op. Guarda contra colisão: aborta se o destino tiver linhas com
    PK *fora* da origem legada (a menos de `--allow-nonempty`).
  - **`--dry-run`**: roda em transação revertida e só reporta contagens.
  - Tolerante a *drift* de schema do legado: tabela ausente na origem é pulada
    com aviso, sem abortar.

- **Relatório de contagens antes/depois** (execução real, `--users-only`):
  - `public.users_user`: **16 → 17** (1 superusuário legado criado).
  - Satélites/`RBAC`: 0 na origem (nada a migrar / pulado).
  - Re-execução: `criados=0 reutilizados=1`, total estável em 17 (idempotência).
  - Hash de senha do usuário migrado **idêntico** ao do SQLite; flags
    `is_superuser/is_staff` e `role` preservados (login com a senha original).

- **Validação do caminho de dados de negócio** (sintética, verificável):
  `backend/scripts/e2e_migrate_legacy.py` constrói um SQLite legado temporário
  (schema atual via `schema_editor`) com base representativa (2 usuários +
  equipe/membro + projeto/sprint/tarefa + risco + categoria/custo + documento +
  comunicação com M2M `destinatarios`), provisiona um tenant descartável, roda o
  comando e verifica: dedup/criação de usuários e memberships por papel;
  contagens por tabela == origem; **remapeamento de FK de usuário** (ex.:
  `Tarefa.criado_por/atualizado_por`, `Comunicacao.destinatarios`); PKs de
  negócio preservados; FK circular `Projeto.custos` restaurada; idempotência da
  2ª execução. **22/22 asserções OK** (PostgreSQL real). Teardown completo.

Comandos/validação:

```bash
./venv/bin/python manage.py check
./venv/bin/python scripts/e2e_migrate_legacy.py              # 22/22
./venv/bin/python manage.py migrate_legacy_data --users-only --dry-run
./venv/bin/python manage.py migrate_legacy_data --users-only # 16 -> 17
./venv/bin/python manage.py migrate_legacy_data --users-only # idempotente
# Regressão:
./venv/bin/python scripts/e2e_cross_tenant.py               # 9/9
./venv/bin/python scripts/e2e_invitations.py                # 13/13
```

#### Plano de rollback (Fase 8)

A migração é **transacional por execução** (em `--dry-run`, revertida ao final) e
**idempotente**, então re-rodar é seguro. Para desfazer:

- **Identidade global (public)**: remover os usuários recém-criados, listados ao
  final do relatório ("Usuários criados no public"). Pré-requisito: nenhum dado
  de negócio em schema de tenant deve referenciar esses usuários (drope os
  schemas de tenant antes, ver abaixo), pois o cascade do ORM consultaria tabelas
  tenant a partir do `public`. Com os schemas tenant já removidos, o delete
  direto é seguro:

  ```sql
  DELETE FROM users_user WHERE email = ANY(ARRAY['caio.beniel55@gmail.com']);
  ```

  Satélites (`UserProfile`/`PasswordHistory`/`AccessAttempt`) caem por cascade.
  As `TenantMembership` criadas caem junto com o usuário (ou com o tenant).

- **Dados de negócio (tenant)**: como os dados entram em um schema dedicado,
  basta dropar/recriar o tenant destino:

  ```bash
  ./venv/bin/python manage.py delete_tenant   # interativo, ou:
  # no schema public: DROP SCHEMA <schema> CASCADE; + remover Client/Domain.
  ```

- **Restauração total do estado pré-migração**: o backup
  `backend/backups/db.sqlite3.codex-task-01-baseline` (Fase 0) preserva o acervo
  legado original; o ambiente PostgreSQL pode ser recriado do zero com
  `migrate_schemas --shared` + `provision_tenant`/`create_dev_tenant` + `seed_data`.

Pendências/ressalvas:

- Migração de **arquivos de media** (`comprovante`, `arquivo` de documentos,
  `anexo` de chat) não foi exercitada com binários reais porque o acervo legado
  não possui registros de negócio nem arquivos; o comando copia os campos
  `FileField` (caminho relativo) fielmente, mas o particionamento físico de
  `MEDIA_ROOT` por tenant segue como item da Fase 11 (operação/segurança).
- RBAC legado permanece fora do escopo automático por decisão de arquitetura
  ainda aberta (ver `docs/multi-tenant-architecture.md`).

### Fase R0: Registro da decisão (Re-arquitetura Shared Schema)

Data local: 2026-06-03

Branch: `Dev-tenant`

Status: concluída.

Objetivo: registrar formalmente a virada de **schema-per-tenant** para **shared
schema + `tenant_id`**, antes de qualquer alteração de código, seguindo o fluxo do
projeto (plano em `codex-task-01.md`, acompanhamento neste audit).

Decisões fixadas:

- **Estratégia:** único schema compartilhado; `tenant_id` em todos os dados de
  negócio. Isolamento por **camada central de aplicação** (manager/queryset que
  injeta o filtro) + RLS de aplicação recriada sobre `tenant_id`; PostgreSQL RLS
  nativo como rede de segurança futura (Fase R7).
- **`tenant_id` inteiro** (FK para `customers.Client`, mantendo PKs atuais) — para
  reduzir o tamanho da migração; UUID reavaliável depois.
- **Sem subdomínio:** o `tenant_id` da request vem da `TenantMembership` ativa do
  usuário autenticado (evita dependência de DNS/wildcard/certificado por tenant).
  Superuser informa o tenant explicitamente.
- **Customização por empresa** via config/feature-flags por tenant; schema físico
  separado só como exceção dura (contrato/lei).
- `customers.Client` permanece como registro da empresa; `django-tenants`,
  `Domain` e o middleware de schema serão removidos a partir da Fase R1.

Motivação: evitar inflar o banco com muitos tenants padronizados (cada schema
duplica ~30 tabelas + índices) e remover a dependência de subdomínio.

Playbook de migração de dados (a ser seguido na R2/R6): adicionar coluna
**nullable → backfill → `NOT NULL` + FK**; índices recriados começando por
`tenant_id`; uniques reescopados por tenant; auditoria garante que nenhuma query
escapa do manager central.

Arquivos alterados nesta fase:

- `backend/codex-task-01.md` (seção "Revisão de Decisão Arquitetural" + "Plano da
  Re-arquitetura para Shared Schema", fases R0–R10).
- `docs/backend-multitenant-audit.md` (banner de revisão + este registro).

Próximo passo: Fase R1 (desativar `django-tenants`, consolidar em banco único).

Pendências/ressalvas:

- Fases 4–8 originais permanecem documentadas como histórico; serão parcialmente
  revertidas/substituídas a partir da R1.
- `migrate_legacy_data` precisa ser reavaliado para o novo alvo (R6).
- `ONBOARDING.md` e `multi-tenant-architecture.md` ainda descrevem o modelo
  schema-per-tenant; atualização planejada para a Fase R10.

### Fase R1: Desativar `django-tenants` (banco único)

Data local: 2026-06-03

Branch: `Dev-tenant`

Status: concluída.

Objetivo: rodar num único schema PostgreSQL (`public`), sem `django-tenants`, com
`manage.py check` e `migrate` verdes. **Isolamento intencionalmente desligado até
a R4** (ver "Janela sem isolamento" em `docs/rearquitetura-shared-schema-plano.md`).

Arquivos principais alterados:

- `backend/planify/settings.py`: removidos `django_tenants` (de `SHARED_APPS`),
  `TenantMainMiddleware`, engine `django_tenants.postgresql_backend` (→
  `django.db.backends.postgresql`), `DATABASE_ROUTERS` (`TenantSyncRouter`),
  `TENANT_MODEL`/`TENANT_DOMAIN_MODEL`/`SHOW_PUBLIC_IF_NO_TENANT_FOUND`.
  `PUBLIC_SCHEMA_NAME = 'public'` **mantido** como constante (querysets/middleware
  ainda a referenciam como ramo de bypass público — comportamento temporário até
  R3/R4). `SHARED_APPS`/`TENANT_APPS` mantidos só como documentação; o
  `INSTALLED_APPS` efetivo não depende mais da divisão.
- `backend/customers/models.py`: `Client` deixou de herdar `TenantMixin`
  (vira `models.Model`), removidos `auto_create_schema` e `schema_name`. Model
  `Domain` removido. Import de `django_tenants.models` removido.
- `backend/customers/admin.py`: removidos `DomainInline`, `DomainAdmin`, import de
  `Domain` e `schema_name` de `list_display`/`search_fields`.
- `backend/customers/migrations/0004_remove_client_schema_name_delete_domain.py`
  (gerada): `RemoveField(client.schema_name)` + `DeleteModel(Domain)`.

Comandos executados:

```bash
./venv/bin/python manage.py check                 # sem issues
./venv/bin/python manage.py makemigrations customers
# Recriar o banco de dev (tinha o schema de tenant `demo` do django-tenants):
docker exec planify-postgres psql -U planify -d postgres -c "DROP DATABASE planify;"
docker exec planify-postgres psql -U planify -d postgres -c "CREATE DATABASE planify OWNER planify;"
./venv/bin/python manage.py migrate               # banco limpo, schema único
```

Resultado da validação (gate R1):

- `manage.py check`: sem issues.
- `migrate` aplicou todas as migrações no schema único `public` (incluindo os apps
  de negócio `projects/tasks/teams/risks/costs/documents/communications`, que antes
  ficavam no schema do tenant).
- Antes da recriação o banco tinha os schemas `demo` + `public`; depois, apenas
  `public`.
- Tabelas confirmadas em `public`: `customers_client`,
  `customers_tenantmembership`, `customers_tenantinvitation`, além de
  `projects_projeto`, `tasks_tarefa`, `costs_custo` etc. `customers_domain` **não
  existe** (0 ocorrências).
- Admin (superuser via test client, `HTTP_HOST=localhost`): `GET /admin/` **200**;
  `/admin/customers/client/`, `/admin/customers/tenantmembership/` e
  `/admin/customers/tenantinvitation/` **200**; `/admin/customers/domain/` **404**
  (model removido). `Domain` ausente do registro do admin.

Pendências/ressalvas:

- **Isolamento desligado (R1→R4):** sem `request.tenant`, `customers/querysets.py`
  e `users/middleware.py` caem no ramo de bypass público (`PUBLIC_SCHEMA_NAME`) e
  **liberam tudo**. Esperado e intencional; **não fazer deploy** antes da R4.
- Comando operacional de migração passou a ser `python manage.py migrate` (não mais
  `migrate_schemas --shared`). README/ONBOARDING serão atualizados na R10.
- `pytest` fica **vermelho** até a R8 (`tests/tenant_base.py` importa
  `TenantTestCase` no nível de módulo). Esperado e documentado.
- Arquivos de runtime/scripts/commands ainda acoplados ao `django-tenants` serão
  tratados nas fases indicadas: `seed_data.py` e `migrate_legacy_data` (R6);
  `scripts/e2e_*.py` e `tests/tenant_base.py` (R8); `create_dev_tenant` e
  `provision_tenant` (R9). Todos com imports lazy — não quebram o `check`.
- Superuser de validação `r1admin` criado no banco de dev recriado (conveniência;
  dados de exemplo serão re-semeados na R6).

Próximo passo: Fase R2 (`tenant_id` nos models de negócio).

### Fase R2: `tenant_id` nos models de negócio

Data local: 2026-06-03

Branch: `Dev-tenant`

Status: concluída.

Objetivo: toda tabela de negócio passa a ter `tenant_id` (FK inteiro para
`customers.Client`), com índices compostos começando por `tenant` e o único
`unique=True` global reescopado por tenant.

Decisões fixadas nesta fase (com o usuário):

- **`on_delete=CASCADE`** na FK `tenant` (não `PROTECT` como rascunhado no plano):
  apagar um `Client` apaga em cascata os dados de negócio do tenant. Trava
  server-side contra exclusão acidental fica para R5/R9 (offboarding dedicado);
  guard de frontend sozinho não cobre admin/shell/API.
- **Single-step `NOT NULL`** em vez do playbook nullable→backfill→NOT NULL: o
  banco estava **vazio** (0 `Client`, 0 linhas de negócio — confirmado por
  contagem), então não há linha para proteger nem backfill a fazer. O carimbo
  real de `tenant_id` em dados legados acontece na R6 (no insert). Cada
  `makemigrations` pediu um default one-off para a FK não-nula; informado `1`
  (nunca aplicado, pois 0 linhas), com `preserve_default=False` na migração.
- **Escopo: todos os 26 models** recebem `tenant_id` (denormalizado, inclusive
  filhos como `ComentarioTarefa`/`HistoricoRisco` e os user-scoped `Notificacao`/
  `ConfiguracaoNotificacao`). É o que o manager central da R4 precisa para
  filtrar qualquer model direto por `tenant_id` sem JOIN.
- **Uniques**: só `Projeto.titulo` (único `unique=True` global) foi reescopado
  para `UniqueConstraint(['tenant','titulo'], name='uniq_projeto_titulo_por_tenant')`.
  Os demais `unique_together`/`UniqueConstraint` referenciam uma FK pai que já
  carrega o tenant (`MembroProjeto`, `Sprint`, `AtribuicaoTarefa`, `MembroEquipe`,
  `PermissaoEquipe`, `ChatMensagemLeitura`) → não colidem cross-tenant; mantidos
  como estão. Ressalva conhecida: `Sprint.unique_together(projeto,nome)` tem
  `projeto` nullable; o caso de sprint órfã (sem projeto) não tem uniqueness
  garantida por tenant — revisar se virar requisito.

Models tocados (26): `projects` (Projeto, MembroProjeto, HistoricoStatusProjeto,
Sprint), `tasks` (Tarefa, AtribuicaoTarefa, ComentarioTarefa,
HistoricoStatusTarefa), `teams` (Equipe, MembroEquipe, PermissaoEquipe), `risks`
(Risco, HistoricoRisco), `costs` (Categoria, Custo, OrcamentoProjeto,
OrcamentoTarefa, Alerta), `documents` (Documento, HistoricoDocumento,
Comentario), `communications` (ChatMensagem, ChatMensagemLeitura, Notificacao,
ConfiguracaoNotificacao, Comunicacao).

Índices compostos `Index(fields=['tenant', <ordering>])` adicionados em todo
model com `Meta.ordering`; models sem ordering ficam com o índice implícito da
FK em `tenant_id`. Campo `tenant` declarado com `related_name='+'` (sem reverse
accessor em `Client`).

Migrations geradas (uma por app):

- `communications/0004_chatmensagem_tenant_chatmensagemleitura_tenant_and_more.py`
- `costs/0003_alerta_tenant_categoria_tenant_custo_tenant_and_more.py`
- `documents/0002_comentario_tenant_documento_tenant_and_more.py`
- `projects/0003_historicostatusprojeto_tenant_membroprojeto_tenant_and_more.py`
- `risks/0002_historicorisco_tenant_risco_tenant_and_more.py`
- `tasks/0003_atribuicaotarefa_tenant_comentariotarefa_tenant_and_more.py`
- `teams/0002_equipe_tenant_membroequipe_tenant_and_more.py`

Comandos executados:

```bash
docker exec planify-postgres psql -U planify -d planify -c "<contagem: 0 linhas>"
printf '1\n1\n%.0s' $(seq 40) | ./venv/bin/python manage.py makemigrations \
  projects tasks teams risks costs documents communications
./venv/bin/python manage.py check          # sem issues
./venv/bin/python manage.py migrate         # 7 migrations OK
```

Validação (gate R2):

- `manage.py check`: sem issues. `migrate`: as 7 migrações aplicaram em banco limpo.
- Schema conferido: 28 colunas `tenant_id` NOT NULL (`bigint`) — 26 de negócio +
  `tenantmembership`/`tenantinvitation` pré-existentes; 28 FKs apontando para
  `customers_client`.
- `projects_projeto`: índice `(tenant_id, criado_em DESC)`, índice da FK
  `(tenant_id)`, e `uniq_projeto_titulo_por_tenant UNIQUE (tenant_id, titulo)`;
  o `unique` global em `titulo` deixou de existir.

Pendências/ressalvas:

- **Isolamento ainda desligado (R1→R4):** a coluna existe mas nenhum filtro a usa
  ainda. Isolamento só volta na R4 (manager/queryset central). **Não fazer deploy.**
- Validação funcional "título repetido entre tenants distintos" não foi exercida
  (0 tenants/dados); está garantida estruturalmente pela constraint
  `(tenant_id, titulo)` e será coberta no e2e da R8 (dois tenants).
- `Sprint` órfã (projeto nullable): uniqueness por tenant não garantida — ver acima.
- Serializers/views/admin ainda não setam nem expõem `tenant`; ajuste no create e
  no manager é da R3/R4. `pytest` segue vermelho até R8.

Próximo passo: Fase R3 (resolução de tenant por `TenantMembership` ativa, sem subdomínio).

### Fase R3: Resolução de tenant por membership (sem subdomínio)

Data local: 2026-06-03

Branch: `Dev-tenant`

Status: concluída.

Objetivo: definir o tenant da request sem host/subdomínio. Com o `django-tenants`
removido na R1, `request.tenant` deixou de ser setado (caía no bypass público).
Agora vem da `TenantMembership` **ativa** do usuário autenticado.

Arquivos principais alterados:

- `customers/tenancy.py` (novo): `resolve_request_tenant(request)` → `(Client, membership)`.
  Usuário normal: tenant da membership ativa; superuser: tenant explícito via header
  `X-Tenant-ID` (ou query `?tenant=`); anônimo: `(None, None)`.
- `users/middleware.py`: `PermissionMiddleware._set_request_tenant` seta
  `request.tenant`/`request.tenant_id`/`request._tenant_membership` logo após a auth
  (antes do bypass de superuser). `check_tenant_membership` reescrito: removido o
  ramo de bypass por `schema_name == PUBLIC`; para prefixos protegidos, sem vínculo
  ativo → 403.
- `customers/querysets.py`: `get_request_membership` usa o cache
  `request._tenant_membership`; `apply_tenant_rls`/`tenant_users_queryset` trocaram
  `schema_name == PUBLIC` por `request.tenant is None` → **`none()`** (inverte o
  bypass perigoso da janela R1→R3 para negação por padrão). Removido o import de
  `settings`.
- `customers/permissions.py`: removido `_is_public_schema`; `IsTenantMember`/
  `HasTenantRole` agora liberam só superuser, senão exigem membership ativa.
- `customers/emails.py` + `customers/views.py`: URL de aceite de convite montada por
  `FRONTEND_URL` + `TENANT_INVITATION_ACCEPT_PATH` (token), sem `tenant.domains`
  (removido na R1) nem `schema_name` (corrige `AttributeError` latente); resposta do
  aceite não devolve mais `domain`.
- `planify/settings.py`: `FRONTEND_URL` (default `http://localhost:5173`);
  `PUBLIC_SCHEMA_NAME` mantido só como referência vestigial (sem uso no código).

Validação (gate R3): script ad-hoc descartável via `django.test.Client` (middleware
real + JWT), banco de dev. **9/9 OK**:

- `resolve_request_tenant`: usuário com membership → seu `Client`; sem membership →
  `None`; superuser sem header → `None`; superuser com `X-Tenant-ID` válido → tenant
  alvo; com id inexistente → `None`.
- E2E middleware em `/api/projects/`: membro (owner) → `200`; usuário sem membership
  → `403`; superuser (bypass) → `200`; anônimo (sem token) → `401`.
- `manage.py check`: sem issues.

Pendências/ressalvas:

- **Filtro real por `tenant_id` ainda é R4.** Hoje um usuário com papel amplo
  (owner/admin/manager/viewer) passa o gate e o `apply_tenant_rls` devolve o
  queryset **inteiro** (todos os tenants) — o `WHERE tenant_id = X` central entra na
  R4. Sem deploy até lá.
- Viewsets de negócio ainda não setam `tenant` no `perform_create` (R4). Criar
  recurso de negócio via API ainda falharia (FK `tenant` NOT NULL) — coberto na R4/R8.
- `TENANT_INVITATION_URL_SCHEME` ficou sem uso (era para subdomínio); mantido por ora.
- Management commands (`create_dev_tenant`, `provision_tenant`, `migrate_legacy_data`)
  e `seed_data.py` ainda usam `schema_name`/`Domain` — R6/R9. `pytest` vermelho até R8.

Próximo passo: Fase R4 (isolamento centralizado em manager/queryset + RLS sobre `tenant_id`).

### Fase R4: Isolamento centralizado (manager/queryset) + RLS

Data local: 2026-06-03

Branch: `Dev-tenant`

Status: concluída. **Marco: isolamento por `tenant_id` restabelecido.**

Objetivo: garantir que **nenhuma** query de negócio escape do filtro por
`tenant_id`, de forma central — em vez de depender de cada call site lembrar de
filtrar. A auditoria (varredura dos 7 apps + `core`) encontrou **~90 chamadas
`.objects` diretas** fora dos viewsets (serializers, dashboards, exports, métodos
de model, admin) que não passavam por nenhum filtro de tenant.

Decisão de arquitetura (com o usuário): **híbrido em duas camadas**, mantendo
`tenant_id` **inteiro** (não UUID):

- **`TenantManager` (manager default dos 26 models) = limite duro automático.**
  Em runtime, dentro de uma request, toda query `Model.objects...` ganha
  `WHERE tenant_id = <atual>` sem intervenção do call site. É o que fecha os ~90
  escapes (validação de unicidade de serializer, dashboards, exports, etc.).
- **RLS por papel preservada por cima** (`apply_member_rls`): `member` continua
  vendo só os recursos ligados a ele (autoria/atribuição/membership). É
  autorização de leitura intra-tenant, não isolamento físico.

O RLS **nativo do PostgreSQL** (a garantia no banco, independente da app) é a
**Fase R7**, decidida para vir logo em seguida como rede de segurança.

Arquivos principais alterados/criados:

- `customers/context.py` (novo): contexto de tenant por thread
  (`activate`/`deactivate`/`is_active`/`get_tenant_id`/`is_bypass` + context
  manager `scope()` para scripts/testes/R6). Estados: inativo (fora de request →
  sem filtro), ativo+bypass (superuser global/`/admin/` → sem filtro), ativo com
  `tenant_id` (filtra), ativo sem tenant e sem bypass (deny → `none()`).
- `customers/managers.py` (novo): `TenantManager.get_queryset` consulta o contexto
  e aplica `filter(tenant_id=...)`/`none()`. `use_in_migrations=False` (não gera
  migration). O `_base_manager` do Django permanece um `Manager` simples
  não-filtrado, preservando cascade de delete, validação de forms e resolução de
  FKs internas.
- `customers/scoping.py` (novo): `pre_save` que carimba `tenant_id` a partir do
  contexto quando ausente (cobre `serializer.save()`, `perform_create`,
  `.objects.create()`, admin e shell em `scope()`); registry dos 26 models.
  Conectado em `customers/apps.py::CustomersConfig.ready()`.
- Os 7 `models.py` (`projects`/`tasks`/`teams`/`risks`/`costs`/`documents`/
  `communications`): `objects = TenantManager()` nos **26 models** de negócio.
- `customers/querysets.py`: `apply_tenant_rls` passou a aplicar o filtro de tenant
  **explicitamente** (`_scope_to_tenant`) antes do narrowing por papel — porque o
  viewset usa `queryset = Model.objects.all()` de nível de classe, avaliado no
  import (sem contexto) e apenas clonado pelo DRF por request; o manager não
  re-filtra esse caminho. Superuser sem tenant → global; com `X-Tenant-ID` → escopa.
- `users/middleware.py`: `PermissionMiddleware` ativa o contexto (deny-by-default)
  no início da request, escopa após resolver o tenant (bypass para `/admin/` e
  superuser-global), e **limpa** em `process_response`/`process_exception` (evita
  vazamento entre requests por reuso de thread).

Limitação conhecida (endereçada pela R7): `queryset=` de **campo de serializer**
(`PrimaryKeyRelatedField`) declarado no nível de classe também é avaliado no
import; um pk cross-tenant poderia validar como FK. O `WITH CHECK` das policies
nativas da R7 é o backstop definitivo para escrita cross-tenant. Os caminhos de
leitura/listagem/detalhe e de create estão cobertos pela R4.

Comandos/validação:

```bash
./venv/bin/python manage.py check                      # sem issues
./venv/bin/python manage.py makemigrations --check --dry-run  # No changes detected
./venv/bin/python scripts/e2e_r4_tenant_isolation.py   # 16/16
```

`scripts/e2e_r4_tenant_isolation.py` (novo, descartável até a R8): dois tenants no
mesmo schema com **dados homônimos** (mesmo título em tenants distintos), exercendo
o stack HTTP real (middleware + JWT + manager + `apply_tenant_rls`) via
`django.test.Client`. **16/16 asserções OK**:

- alice (owner alpha) só vê projetos de alpha; detalhe de projeto de beta → 404.
- bob (owner beta) só vê beta.
- mallory (`member` alpha) só vê o projeto em que é membro (RLS de papel sobre o
  limite de tenant); não vê outro projeto de alpha nem nada de beta.
- root (superuser) sem header vê todos os tenants; com `X-Tenant-ID=alpha`/`beta`
  vê só o tenant indicado.
- alice cria projeto com título que **só existe em beta** → `201` (unicidade
  escopada pelo manager) e o projeto + o `MembroProjeto` auto-criado nascem
  carimbados com `tenant=alpha`.
- carimbo fora de HTTP via `context.scope(beta)` → `tenant=beta`.
- "filtro esquecido": `Projeto.objects.filter(titulo=...)` dentro de `scope(alpha)`
  conta só o de alpha.

Pendências/ressalvas:

- **`pytest` segue vermelho até a R8** (`tests/tenant_base.py` importa
  `TenantTestCase` no nível de módulo). Esperado e documentado. A suíte e os
  `scripts/e2e_*.py` antigos (django-tenants) serão reescritos na R8.
- Limitação dos `queryset=` de serializer no nível de classe (acima) → R7.
- `admin` opera em modo global (bypass) para staff/superuser, como antes; RLS por
  tenant no admin não é objetivo da R4.
- Sem deploy até a R7 fechar a rede de segurança no banco (recomendado), embora a
  R4 já restabeleça o isolamento na aplicação.

Próximo passo: Fase R7 (RLS nativo do PostgreSQL: `ENABLE`+`FORCE ROW LEVEL
SECURITY`, policies SELECT/INSERT/UPDATE/DELETE sobre `tenant_id`,
`SET LOCAL app.current_tenant` por transação, role `app_user` sem bypass + role de
migration com `BYPASSRLS`).

> Ordem ajustada (decisão do usuário, 2026-06-03): executar **R5 → R6 → R7**.

### Fase R5: Customização por tenant (config/feature-flags)

Data local: 2026-06-03

Branch: `Dev-tenant`

Status: concluída.

Objetivo: permitir regras de negócio diferentes por empresa **sem** schema físico
separado, via configuração/feature-flags por tenant.

Decisão de arquitetura: **um model dedicado `TenantSettings` (1-1 com `Client`)**
com dois campos JSON livres e extensíveis (em vez de colunas fixas ou JSON no
próprio `Client`), priorizando flexibilidade sem migration a cada nova flag:

- `features` (`chave -> booleano`): liga/desliga funcionalidades.
- `config` (`chave -> valor`): parâmetros arbitrários.

Arquivos:

- `customers/models.py`: model `TenantSettings` + métodos `is_feature_enabled`,
  `set_feature`, `get_config`. `migrations/0005_tenantsettings.py`.
- `customers/config.py` (novo): **ponto único de leitura** —
  `get_tenant_settings(tenant)` (cria com defaults na 1ª leitura; `None`-safe) e
  `tenant_feature_enabled(tenant, key, default)`. `register_tenant_settings()`
  conecta um `post_save` em `Client` que cria as settings de todo tenant novo;
  registrado em `customers/apps.py::ready()`.
- `customers/admin.py`: `TenantSettingsAdmin`.

`TenantSettings` é model de **infra de tenancy** (chaveado por `Client`), não de
negócio: usa o `Manager` padrão (não o `TenantManager`) e não tem `tenant_id`.

Validação (shell, PostgreSQL real): criar `Client` → `TenantSettings` criada
automaticamente; `set_feature`/`get_config` persistem e são lidos pelo ponto único;
`tenant_feature_enabled` honra default; `get_tenant_settings(None)` → `None`;
`Client.delete()` cascateia e remove as settings. `manage.py check` sem issues;
`migrate` aplicou `0005`.

Pendências/ressalvas:

- Não há flags de produto concretas ainda; a infra está pronta para consumo
  pontual no código de negócio via o ponto único (sem espalhar regras).
- Schema físico separado por empresa permanece **exceção dura** (contrato/lei),
  fora deste mecanismo.

Próximo passo: Fase R6 (migração de dados dos schemas legados para o shared).

### Fase R6: Migração de dados (schemas → shared)

Data local: 2026-06-03

Branch: `Dev-tenant`

Status: concluída.

Objetivo: trazer os dados para o schema único com `tenant_id` populado e tornar o
seed compatível com o shared schema. Como a R1 já recriou o banco de dev como
schema único (os schemas de tenant do django-tenants não existem mais) e a base
legada real é o SQLite single-tenant (só 1 superusuário, sem negócio), o trabalho
foi **reescrever os dois utilitários** para o novo alvo.

Arquivos:

- `seed_data.py`: removido `django_tenants.utils`; tenant resolvido por
  `Client` (env `SEED_TENANT`, default `Demo`, `get_or_create` — dispara o
  `post_save` que cria as `TenantSettings` da R5). Identidade (usuários +
  memberships) na fase compartilhada; dados de negócio gravados dentro de
  `customers.context.scope(tenant_id=...)`, de modo que o `pre_save` da R4 carimba
  `tenant_id` em cada create e o `TenantManager` escopa as leituras.
- `customers/management/commands/migrate_legacy_data.py`: removido
  `schema_context`/`get_public_schema_name`; tudo grava no `default`. `--schema`
  → `--tenant` (id ou nome do `Client`). Negócio é carimbado com `tenant_id`
  explicitamente; idempotência por PK **no tenant destino**; **colisão de PK
  cross-tenant aborta** (no shared schema o espaço de PK é global — preservar PK
  que já pertence a outro tenant colidiria; importar para um banco com negócio de
  outros tenants exigiria remapear FKs de negócio, fora do escopo atual).
  Inspeções via `_base_manager` (não-filtrado), independentes de contexto.

Validação (PostgreSQL real):

```bash
./venv/bin/python manage.py check                              # sem issues
./venv/bin/python manage.py migrate_legacy_data --users-only --dry-run \
    --legacy-db backups/db.sqlite3.codex-task-01-baseline      # lidos=1 criados=1
./venv/bin/python seed_data.py                                 # seed completo
```

- Seed do tenant `Demo`: **504 linhas de negócio**, **0 com `tenant_id` nulo**,
  **0 fora do `Demo`** (carimbo correto em todos os caminhos de create); 7
  memberships; `TenantSettings` criada automaticamente. `Projeto.objects` dentro
  de `scope(Demo)` == `_base_manager` (consistente).
- `migrate_legacy_data --users-only --dry-run`: 1 usuário legado, satélites 0,
  RBAC pulado.

Pendências/ressalvas:

- O e2e antigo `scripts/e2e_migrate_legacy.py` ainda é django-tenants; sua
  reescrita (e a suíte `tests/`) é a **R8**. `pytest` segue vermelho até lá.
- Migração de **media** (arquivos) não exercida (sem binários no acervo);
  particionamento físico de `MEDIA_ROOT` por tenant segue como item de operação.
- RBAC legado permanece fora do escopo automático (decisão de arquitetura aberta).

Próximo passo: Fase R7 (RLS nativo do PostgreSQL — rede de segurança no banco).

### Fase R7: RLS nativo do PostgreSQL

Data local: 2026-06-03

Branch: `Dev-tenant`

Status: concluída.

Objetivo: segunda camada de isolamento **no banco**, independente da aplicação —
mesmo uma query sem `WHERE tenant_id` não vaza entre tenants. Decisão do usuário:
"backend controla identidade; banco garante isolamento".

Decisões e como o ambiente moldou a solução:

- A conexão padrão (`planify`) é **superuser** (`rolsuper=true`), então **ignora
  RLS** sempre. Para o RLS valer, a app web deve conectar com uma role sem
  privilégio: `manage.py setup_rls` cria **`app_user`** (LOGIN, NOSUPERUSER,
  NOBYPASSRLS) com CRUD em `public`. Operação: migrations/seed/testes seguem por
  `planify` (bypass, nada quebra); a **web** roda com `POSTGRES_USER=app_user`.
- RLS aplicada só às **26 tabelas de negócio**. As `customers_*`
  (`tenantmembership`/`tenantinvitation`/`tenantsettings`) têm coluna `tenant_id`
  mas **ficam fora**: a resolução do tenant lê `TenantMembership` *antes* de a GUC
  existir; aplicar RLS nelas travaria login/bypass.

Arquivos:

- `customers/migrations/0006_native_rls.py`: `RunPython` que, para cada uma das 26
  tabelas, faz `ENABLE`+`FORCE ROW LEVEL SECURITY` e cria a policy `tenant_isolation`
  (`FOR ALL`) com `USING` e `WITH CHECK` iguais ao predicado da GUC. Reversível.
- `customers/rls.py`: `TenantDatabaseRLSMiddleware` (após o `PermissionMiddleware`)
  envolve a request em `transaction.atomic()` e faz
  `set_config('app.current_tenant', <v>, true)` (escopo de transação). Valor `<v>`
  espelha o contexto R4: `''` (bypass superuser/admin), `str(tenant_id)`, ou `-1`
  (deny/fail-closed). `current_guc_value()`.
- `customers/management/commands/setup_rls.py`: cria/atualiza `app_user` + grants
  (idempotente; roda pela conexão dona `planify`).
- `planify/settings.py`: middleware adicionado ao `MIDDLEWARE`.

Predicado da policy (GUC `app.current_tenant`, `tenant_id` bigint):

```sql
current_setting('app.current_tenant', true) = ''                 -- global (superuser/admin)
OR tenant_id = NULLIF(current_setting('app.current_tenant', true), '')::bigint
-- '' => todas; '<id>' => só o tenant; '-1'/ausente => nenhuma (fail-closed)
```

Validação (`scripts/e2e_r7_native_rls.py`, conectando como `app_user` via psycopg):
**7/7 OK** — GUC=A vê só A (query crua sem WHERE), GUC=B só B, `''` vê todos,
`-1` e sessão sem GUC não veem nada (fail-closed), e `UPDATE` movendo linha de A
para B é bloqueado pelo `WITH CHECK`. `pg_policies`: 26 policies `tenant_isolation`;
`projects_projeto` com `relrowsecurity`+`relforcerowsecurity`;
`customers_tenantmembership` sem RLS.

Pendências/ressalvas:

- Para **ativar em runtime**, rodar a web com `POSTGRES_USER=app_user` (+ senha);
  documentar em README/.env.example fica para a R10. Sob `planify` o RLS é inócuo
  (a camada R4 segue isolando na app).
- Toda request passa a abrir uma transação (`atomic`) para o `SET LOCAL`; aceitável.
- `app_user` recebe CRUD em todo `public`; refino de privilégios por tabela é
  endurecimento futuro (R11/observabilidade-segurança).

Próximo passo: R8 (testes/e2e na nova base) e R10 (docs/onboarding) — fora do
pedido atual (R5→R6→R7).

### Fase R8: Testes

Data local: 2026-06-03

Branch: `Dev-tenant`

Status: concluída.

Objetivo: ressuscitar a suíte `pytest` (vermelha desde a R1, pois a base importava
`TenantTestCase` do `django-tenants`) e reescrever os e2e para o shared schema —
sem schema/host/`Domain`.

Arquivos:

- `backend/tests/tenant_base.py` (reescrito): sem `django_tenants`. Usa
  `rest_framework.test.APITestCase` (transação revertida por teste). O tenant de
  teste é uma linha `customers.Client`; `create_member` cria `User` +
  `TenantMembership` ativa; o `APIClient` é autenticado por **JWT Bearer** (sem
  host — o tenant é resolvido pela membership). A base **mantém o contexto de
  tenant ativo** (`customers.context.activate`) durante o teste para que os
  `Model.objects.create(...)` diretos do `setUp`/teste sejam carimbados com
  `tenant_id`; um `_ContextRestoringClient` reativa o escopo do tenant após cada
  request (o `PermissionMiddleware` desativa o contexto em `process_response`),
  cobrindo criação de objetos antes **e** depois de chamadas HTTP.
- `backend/scripts/e2e_invitations.py` (reescrito): `provision_tenant` por
  `--name`; sem `HTTP_HOST`/schema; cleanup por `Client.name` (cascateia
  memberships/convites/negócio) + e-mails.
- `backend/scripts/e2e_migrate_legacy.py` (reescrito): sem `schema_context`/
  `Domain`. Constrói o SQLite legado com o schema atual (incl. `customers_client`
  p/ satisfazer a FK `tenant` na origem), popula carimbando um tenant de origem
  fictício e com **PKs altos** (`PK_BASE=90_000_000`) para não colidir com o seed
  `Demo` do banco de dev (o comando preserva PK); asserções lidas com o tenant
  destino escopado por `context.scope`; `--tenant <nome>`.
- `backend/scripts/e2e_cross_tenant.py` **removido** — redundante com
  `e2e_r4_tenant_isolation.py` (isolamento cross-tenant por `tenant_id`, 16/16).
- `backend/tests/README.txt` atualizado para o stack shared schema.

Validação (PostgreSQL real):

```bash
./venv/bin/pytest tests/ --create-db          # 27 passed
./venv/bin/python scripts/e2e_r4_tenant_isolation.py   # 16/16
./venv/bin/python scripts/e2e_r7_native_rls.py         # 7/7
./venv/bin/python scripts/e2e_invitations.py           # 13/13
./venv/bin/python scripts/e2e_migrate_legacy.py        # 23/23
```

Pendências/ressalvas:

- Rodar a suíte com a role **dona** do banco (não `app_user`): a RLS nativa é
  inócua para ela e não atrapalha a criação de fixtures.
- Autorização a nível de objeto (ex.: `member` editar só a tarefa atribuída a ele)
  segue como refinamento de produto sobre a base de isolamento — fora da R8.

### Fase R9: Provisionamento e convites

Data local: 2026-06-03

Branch: `Dev-tenant`

Status: concluída.

Objetivo: provisionar empresa **sem** schema/domínio. Após a R1 (remoção de
`Domain`/`schema_name`/`auto_create_schema`), os dois management commands ainda
referenciavam esses atributos (imports lazy — não quebravam o `check`, mas
quebrariam em runtime).

Arquivos:

- `customers/management/commands/provision_tenant.py` (reescrito): args agora são
  `--name` + `--owner-email`/`--owner-username`/`--owner-full-name`/
  `--owner-password`. Cria `Client.objects.create(name=...)` (dispara o `post_save`
  que cria as `TenantSettings` da R5), resolve/cria o owner e a
  `TenantMembership(owner)`. Recusa nome de tenant duplicado (o `name` é o
  identificador usado por `migrate_legacy_data --tenant <nome>`) e owner já
  vinculado ("um usuário = uma empresa").
- `customers/management/commands/create_dev_tenant.py` (reescrito): `--name`
  (default `Demo`) + `--owner-username` opcional; sem schema/domínio.

Convites: o fluxo já estava shared-schema desde a R3 — a URL de aceite usa
`FRONTEND_URL` + `TENANT_INVITATION_ACCEPT_PATH` (token), sem subdomínio
(`customers/emails.py`, `customers/views.py`). Nada a alterar aqui.

Validação:

- `manage.py check` sem issues.
- `e2e_invitations.py` 13/13: provisionar (via `provision_tenant`) → convidar →
  inspecionar → aceitar (conta nova + membership) → acessar `/api/projects/` →
  negações (member cria convite 403, reaceite 400, convidar já-vinculado 400,
  outsider 403).
- Smoke `create_dev_tenant --name "R9 Smoke"`: `Client` criado com `TenantSettings`
  auto-criada; removido após o teste.

### Fase R10: Docs e onboarding

Data local: 2026-06-03

Branch: `Dev-tenant`

Status: concluída.

Objetivo: deixar a documentação coerente com o modelo **shared schema + `tenant_id`**
(os docs ainda descreviam schema-per-tenant/subdomínio/`migrate_schemas`).

Arquivos atualizados:

- `docs/multi-tenant-architecture.md`: reescrito para o modelo shared — banner de
  pivô, decisões vigentes, as **três camadas** de isolamento (`TenantManager`, RLS
  de app, RLS nativo), resolução por membership, provisionamento/convites sem
  schema, comandos (`migrate`/`setup_rls`/`provision_tenant --name`), testes/e2e e
  pontos em aberto.
- `ONBOARDING.md`: stack, seção 4 (conceito central → shared + 3 camadas), models
  de `customers` (sem `Domain`, com `TenantSettings`/infra), fluxo de auth, fluxos
  (provision por `--name`), "como rodar" (`migrate` + `setup_rls`, sem subdomínio),
  testes/e2e, comandos, tabela de fases (R0–R10) e armadilhas.
- `backend/readme-backend.md`: tecnologias, instalação/dev (`migrate`), seção
  "PostgreSQL e Tenants (shared schema)" + RLS nativo/`app_user`, seed (`SEED_TENANT`)
  e `migrate_legacy_data --tenant`.
- `backend/tests/README.txt`: stack shared schema (feito junto da R8).

Conclui a re-arquitetura R0–R10. Frentes seguintes (fora do escopo R): autorização
a nível de objeto, Fase 11 (observabilidade/segurança: logs com tenant,
`MEDIA_ROOT` por tenant, refino de privilégios do `app_user`) e Fase 12 (frontend).
