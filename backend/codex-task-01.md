# Codex Task 01: Plano Multi-Tenant do Backend (Shared Schema)

**Projeto:** Planify

> Modelo vigente: **shared schema + `tenant_id`** (um único schema PostgreSQL; sem
> `django-tenants`/subdomínio). A re-arquitetura **R0–R10 está concluída**
> (2026-06-03). Documentos relacionados:
>
> - `docs/rearquitetura-shared-schema-plano.md` — passo a passo de implementação.
> - `docs/backend-multitenant-audit.md` — auditoria fase-a-fase (inclui o histórico
>   do caminho schema-per-tenant original, que foi superado).
> - `docs/multi-tenant-architecture.md` — desenho da arquitetura atual.

## Objetivo

Backend SaaS multi-tenant com **isolamento forte de dados por empresa** num único
schema PostgreSQL, mantendo usuários, permissões, administração, API e testes
coerentes com o modelo `tenant_id`.

## Arquitetura vigente (shared schema + `tenant_id`)

**Decisão:** isolamento por **`tenant_id`** (FK inteiro para `customers.Client`) em
todos os dados de negócio, garantido por **três camadas**: manager/queryset central
que injeta o filtro por `tenant_id`, RLS de aplicação por papel, e RLS nativo do
PostgreSQL como rede de segurança no banco.

**Decisões técnicas fixadas:**

- **`tenant_id` é FK inteiro** para `customers.Client` (mantém os PKs atuais;
  escolha p/ migração mais leve — UUID reavaliável depois, se o id vazar em URL/API).
- **`customers.Client`** é o registro da empresa (tenant), com `name`, `slug`
  único e `status` (`active`/`suspended`). **Sem** `Domain`, schema por tenant,
  `TenantMainMiddleware`, `SHARED_APPS`/`TENANT_APPS` ou router.
- **Tenant da request vem da `TenantMembership` ativa** do usuário autenticado (sem
  subdomínio). Superuser é administrador do SaaS e não tem bypass nas APIs de
  negócio tenant-scoped.
- **Isolamento centralizado num manager/queryset default** — "auditar queries"
  significa garantir que nada escape do filtro (`.objects` cru, `raw()`, agregações
  soltas), **não** espalhar `WHERE tenant_id = ?` manualmente.
- **Customização por empresa via config/feature-flags** (`TenantSettings` ligado ao
  `Client`); schema físico separado só como **exceção dura** (contrato/lei).

**Motivação do modelo shared (vs schema-per-tenant):**

- **Volume de tenants padronizados.** SaaS com muitas empresas usando o serviço da
  mesma forma; schema-per-tenant infla o catálogo do PostgreSQL (cada empresa
  duplica ~30 tabelas + índices + sequences; migrations rodam por schema).
- **Menos dependência de infra.** Resolver por `tenant_id` (via membership) remove
  a necessidade de DNS/wildcard/certificado por tenant.
- **Customização sem schema separado**, via config/feature-flags por tenant.

## Estado: re-arquitetura R0–R10 (CONCLUÍDA)

> Checklist autoritativo. Cada fase seguiu o protocolo: executar → validar →
> registrar em `docs/backend-multitenant-audit.md`. Branch: `Dev-tenant`.

### Fase R0 — Registro da decisão ✅

- [x] Fixar decisões: `tenant_id` inteiro, manager central, sem subdomínio,
      customização por config/feature-flags.

### Fase R1 — Desativar `django-tenants` (banco único) ✅

- [x] Remover `django_tenants` de `INSTALLED/SHARED/TENANT_APPS`,
      `TenantMainMiddleware`, `TENANT_MODEL`/`TENANT_DOMAIN_MODEL`, `DATABASE_ROUTERS`.
- [x] Consolidar tudo num único schema (`public`).
- [x] `Client` deixa de herdar `TenantMixin`/`auto_create_schema`; `Domain` removido.
- [x] Critério: `manage.py check` + `migrate` em banco limpo.

### Fase R2 — `tenant_id` nos models de negócio ✅

- [x] `tenant = FK(customers.Client, CASCADE)` `NOT NULL` nos 26 models de
      `projects/tasks/teams/risks/costs/documents/communications` (banco vazio →
      single-step; backfill real é a R6).
- [x] Índices compostos `Index(['tenant', <ordering>])`; `Projeto.titulo` →
      `UniqueConstraint(['tenant','titulo'])` (demais uniques já tenant-safe via FK pai).

### Fase R3 — Resolução de tenant por membership (sem subdomínio) ✅

- [x] `customers/tenancy.resolve_request_tenant` + `PermissionMiddleware._set_request_tenant`
      definem `request.tenant`/`tenant_id` pela `TenantMembership` ativa.
- [x] Superuser sem membership não acessa APIs de negócio tenant-scoped; o antigo
      `X-Tenant-ID` não concede bypass de tenant.
- [x] `querysets.py`/`permissions.py`/`middleware.py` sem `schema_name`; sem tenant
      resolvido → `none()`/403. URL de convite por `FRONTEND_URL` + token.

### Fase R4 — Isolamento centralizado (manager/queryset) + RLS ✅

- [x] `TenantManager` (manager default dos 26 models) filtra por `tenant_id` via
      contexto de thread (`customers/context.py`); `pre_save` (`scoping.py`)
      carimba `tenant_id` no create; mixin de viewset.
- [x] `apply_tenant_rls`/`apply_member_rls` recriados sobre `tenant_id`.
- [x] ~90 escapes `.objects` auditados; cobertos pelo manager. `e2e_r4` 16/16.

### Fase R5 — Customização por tenant ✅

- [x] Model `TenantSettings` (1-1 com `Client`, JSON `features`/`config`); ponto
      único `customers.config`; auto-criação via `post_save`.

### Fase R6 — Migração de dados (legado → shared) ✅

- [x] `seed_data.py` e `migrate_legacy_data` reescritos p/ o shared schema (carimbo
      de `tenant_id`, sem `schema_context`). Seed: 504 linhas, 0 nulos.

### Fase R7 — PostgreSQL RLS nativo (rede de segurança) ✅

- [x] `FORCE ROW LEVEL SECURITY` + policy por `app.current_tenant` nas 26 tabelas
      (`migrations/0006`); `TenantDatabaseRLSMiddleware`; role `app_user`
      (`setup_rls`). `e2e_r7` 7/7.

### Fase R8 — Testes ✅

- [x] `tests/tenant_base.py` reescrito sem `django-tenants` (`Client` +
      `TenantMembership` + JWT; tenant por membership). `pytest tests/` 27 passed.
- [x] e2e reescritos: `e2e_invitations.py` 13/13, `e2e_migrate_legacy.py` 23/23;
      `e2e_cross_tenant.py` removido (substituído por `e2e_r4_tenant_isolation.py`).

### Fase R9 — Provisionamento e convites ✅

- [x] `provision_tenant` (`--name`) e `create_dev_tenant` criam só a linha `Client`
      (+ `TenantSettings`) + owner + membership, sem schema/`Domain`. Convites já
      sem subdomínio (R3). Validado por `e2e_invitations.py`.

### Fase R10 — Docs e onboarding ✅

- [x] `ONBOARDING.md`, `readme-backend.md`, `docs/multi-tenant-architecture.md` e
      `tests/README.txt` atualizados para o modelo shared schema + `tenant_id`.

## Trabalho restante (próximas frentes)

### Autorização a nível de objeto

- [ ] Refinar regras por entidade sobre a base de isolamento já estabelecida
      (ex.: `member` editar **apenas** a tarefa atribuída a ele, não qualquer
      tarefa do projeto que acessa). Decisão de produto, coberta por testes novos.

### Fase 11 — Observabilidade e Segurança

> Sem schema/migrations por tenant; o tenant é uma dimensão (`tenant_id`).

- [ ] Logs com `tenant_id` (filtro de logging que injeta o tenant do contexto da
      request — `customers.context.get_tenant_id`).
- [ ] Auditoria de ações sensíveis (criar/remover membership, provisionar tenant,
      aceitar convite) carimbando o tenant.
- [ ] Revisar CORS, `ALLOWED_HOSTS`, cookies, JWT e HTTPS para produção.
- [ ] Rate limiting (por usuário e/ou por tenant).
- [ ] **Rodar a web como `app_user`** em produção (RLS nativo ativo); manter
      migrations/seed pela role dona. Documentar a separação de credenciais.
- [ ] Refino de privilégios do `app_user` por tabela (hoje CRUD em todo `public`).
- [ ] Particionamento de `MEDIA_ROOT` por tenant (documentos/anexos).
- [ ] Backup do banco único + export/delete por `tenant_id` para offboarding.

### Fase 12 — Frontend e Integração (EM ANDAMENTO)

> baseURL única (sem subdomínio): o tenant vem do JWT/membership no backend.

- [x] baseURL única + bugs do `frontend/plugins/api.ts` corrigidos
      (`os.BACKEND_URL` → `runtimeConfig.public.apiBaseUrl`; `authStore.token` →
      `authStore.accessToken`). Feito junto da migração do frontend para o cliente
      OpenAPI gerado (`lib/api-client` + adaptadores finos em `services/api`).
- [x] Rota pública de aceite por token **no backend** (já existe e roteada):
      `GET /api/invitations/<token>/` (`InvitationDetailView`) +
      `POST /api/invitations/<token>/accept/` (`InvitationAcceptView`); gestão via
      `TenantInvitationViewSet` em `/api/tenant/invitations/`.
- [ ] Login: tenant implícito (membership ativa); tratar `403` "sem vínculo" e `401`
      na UX do frontend.
- [ ] Frontend: tela de gestão de convites (owner/admin) consumindo
      `/api/tenant/invitations/`.
- [ ] Frontend: tela pública de aceite por token (inspeção + aceite).
- [ ] Instalar deps de build faltantes do frontend: `chart.js` e `date-fns`
      (importadas em reports/communication/`DateRangePicker.vue`, mas ausentes do
      `package.json` → quebram o build dessas páginas).
- [ ] Regenerar o cliente OpenAPI (passou a incluir os recursos recém-roteados na
      higiene de API abaixo: `sprints`, `historico-status`, `comunicacoes`); testar
      convite → aceite → login → criar projeto/tarefa.
- [ ] (Opcional) Painel superuser: operações de plataforma sem acesso livre aos
      dados de negócio do tenant.

> **Higiene de API (feito 2026-06-03, habilita a regeneração do cliente):** viewsets
> órfãos roteados — `SprintViewSet`→`/api/projects/sprints/`,
> `HistoricoStatusProjetoViewSet`→`/api/projects/historico-status/` (ambos antes do
> prefixo vazio do `ProjetoViewSet`), `ComunicacaoViewSet`→`/api/communications/comunicacoes/`.
> Imports mortos removidos de `projects/urls.py` (dashboard/kanban/gantt/export
> APIViews, duplicados pelas `@action` do `ProjetoViewSet`). **Pendente:**
> `UserAccessProfileViewSet` exige rota aninhada (`/users/{user_pk}/access-profiles/`)
> — decisão de design; os 3 arquivos `*_views.py` órfãos viraram código morto.

## Critérios de aceite (re-arquitetura — atingidos)

- [x] `manage.py check` e `migrate` (banco único) verdes.
- [x] `tenant_id NOT NULL` em todos os models de negócio; uniques por tenant.
- [x] Nenhuma query de negócio escapa do filtro central por `tenant_id`.
- [x] Dois tenants coexistem; dados de A não aparecem para B (`e2e_r4`/`e2e_r7`).
- [x] `member` restrito aos próprios recursos; superuser opera com tenant explícito.
- [x] Provisionamento/convites funcionam sem schema/subdomínio.
- [x] Suíte e e2e verdes (`pytest tests/` 27; e2e r4/r7/invitations/migrate).
- [x] Docs (ONBOARDING/readme/arquitetura) atualizados.
