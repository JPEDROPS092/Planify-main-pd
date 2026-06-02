# Auditoria da Refatoração Multi-Tenant do Backend

Este documento deve ser atualizado sempre que uma fase da `backend/codex-task-01.md` for concluída ou quando uma fase avançar com ressalvas relevantes.

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
| Fase 5: Classificação e Movimentação dos Apps | Parcial validada | `SHARED_APPS` e `TENANT_APPS` configurados; referências antigas a `Projeto.name` corrigidas; revisão fina de views/admin ainda pendente. |
| Fase 6: Membership, Permissões e Isolamento | Parcial validada | `TenantMembership`, roles, bloqueio `403`, remoção do bypass global por `User.role == ADMIN` e RLS de aplicação em querysets principais validados parcialmente. |
| Fase 7: Refatoração de Autenticação | Concluída inicialmente | ADR `docs/adr-0001-auth-multitenant.md`. Djoser+JWT mantidos; provisionamento de owner por superuser e fluxo de convite implementados e validados (e2e 13/13). |
| Fase 8: Migração de Dados Existentes | Não iniciada | Tenant destino e script de migração ainda pendentes. |
| Fase 9: Testes | Não iniciada | Suite será refeita após contratos multi-tenant. |
| Fase 10: Admin, Docs e Operação | Parcial | README e comando de criação de tenant adicionados; guia completo de operação ainda pendente. |
| Fase 11: Observabilidade e Segurança | Não iniciada | Logs com tenant, auditoria e hardening pendentes. |
| Fase 12: Frontend e Integração | Não iniciada | Integração por subdomínio ainda pendente. |

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

Status: parcial.

Resultado até agora:

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

Pendências:

- Revisar imports diretos entre apps tenant e shared.
- Revisar views, filters e querysets que assumem banco único.
- Validar admin dos apps tenant no schema correto.

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

- Bug pré-existente fora do escopo: `users/views.py::reset_password` usa
  `User.objects.make_random_password()` (removido no Django 5.1; projeto no 5.2).
  Trocar por `get_random_string`.
- Restrição/curadoria do cadastro público (`registro.vue`) é decisão de produto.
- Integração de frontend (tela de gestão de convites, rota de aceite, baseURL
  por subdomínio) fica para a Fase 12, conforme plano de migração na ADR.
