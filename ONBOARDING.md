# Planify — Guia de Onboarding para Desenvolvedores

> Documento de entrada para quem acabou de chegar ao projeto. Explica **o que é**,
> **como está hoje**, **como roda**, as **regras de negócio**, os **fluxos**, os
> **schemas** e a **stack**. Leia isto primeiro; depois aprofunde nos docs
> referenciados ao longo do texto.
>
> Última atualização: 2026-06-03 · Branch de trabalho atual: `Dev-tenant`
>
> **Arquitetura atual: shared schema + `tenant_id`** (um único schema PostgreSQL;
> sem `django-tenants`/subdomínio). O projeto começou com schema-per-tenant e foi
> repensado nas fases **R0–R10** (ver seção 4 e `docs/rearquitetura-shared-schema-plano.md`).

---

## 1. O que é o Planify

Planify é um **SaaS de gerenciamento de projetos de P&D** (Pesquisa &
Desenvolvimento). Cobre projetos, tarefas (com Kanban), equipes, riscos, custos,
documentos e comunicação, com autenticação e controle de acesso por papel.

O projeto está em meio a uma **refatoração grande para multi-tenant** (uma
empresa = um schema PostgreSQL isolado). Entender essa refatoração é o que mais
importa para trabalhar no backend hoje — veja a seção 4.

---

## 2. Stack

### Backend (`backend/`)
- **Python 3.12**, **Django 5.2**, **Django REST Framework**
- **Multi-tenant shared schema**: isolamento por **`tenant_id`** (FK para
  `customers.Client`) num único schema, com manager central + RLS de aplicação +
  RLS nativo do PostgreSQL. **Sem `django-tenants`** (removido na R1).
- **PostgreSQL 16** (via Docker) — banco principal; SQLite só como fallback legado
- **Simple JWT** (access 7d, refresh 30d, rotação + blacklist) + **Djoser** (gestão de conta/senha)
- **drf-spectacular** — OpenAPI/Swagger
- **pytest + pytest-django** — testes (exigem PostgreSQL)

### Frontend (`frontend/`)
- **Nuxt 3** (Vue 3, TypeScript), **Pinia** (estado), **Tailwind CSS** + **shadcn-nuxt** / **reka-ui**
- **axios** + cliente gerado do OpenAPI (`openapi-typescript-codegen` → `lib/api-client`)
- `@nuxtjs/color-mode` (tema claro/escuro), `vuedraggable`/`sortablejs` (Kanban)

### Infra / Dev
- **Docker Compose** (`compose.yml`) sobe o PostgreSQL local em `127.0.0.1:15432`
- Docs do produto em **Docusaurus** (`docs/`)

---

## 3. Estrutura do repositório

```
Planify-main-pd/
├── ONBOARDING.md            # este arquivo
├── README.md                # visão de produto
├── BACKLOG.md               # backlog geral (produto)
├── compose.yml              # PostgreSQL local (docker)
├── docs/                    # docs de arquitetura/decisões (LEIA — ver abaixo)
│   ├── multi-tenant-architecture.md      # desenho do multi-tenant
│   ├── backend-multitenant-audit.md      # RASTREADOR de progresso por fase
│   ├── adr-0001-auth-multitenant.md      # decisão de autenticação
│   └── database-review.md                # mapa de models por escopo
├── backend/
│   ├── planify/             # settings, urls raiz, wsgi/asgi
│   ├── customers/           # ★ app multi-tenant (Client, Membership, Invitation, Settings; manager/RLS)
│   ├── users/               # ★ usuário global + auth + middleware de permissão
│   ├── core/                # ★ shared: dashboards, health, docs
│   ├── projects/ tasks/ teams/ risks/ costs/ documents/ communications/  # apps de NEGÓCIO (tenant)
│   ├── tests/               # suíte pytest (tenant-aware)
│   ├── scripts/             # testes e2e em script (ver seção 11)
│   ├── seed_data.py         # popular dados de exemplo
│   ├── codex-task-01.md     # PLANO em 12 fases da refatoração multi-tenant
│   └── readme-backend.md    # setup/execução do backend
└── frontend/
    ├── pages/ components/ layouts/   # UI (Nuxt)
    ├── stores/              # Pinia (auth, projects, tasks, ...)
    ├── services/ plugins/   # cliente HTTP / interceptors
    └── lib/api-client/      # cliente gerado do OpenAPI
```

**Onde está o backlog/estado real:** `docs/backend-multitenant-audit.md` é a fonte
de verdade do progresso. `backend/codex-task-01.md` é o plano. `BACKLOG.md` e
`backend/Backlogbackend.md` são backlog de produto (mais antigos, menos confiáveis
quanto ao estado atual do multi-tenant).

---

## 4. Arquitetura multi-tenant (o conceito central)

Documento completo: `docs/multi-tenant-architecture.md`. Plano da re-arquitetura:
`docs/rearquitetura-shared-schema-plano.md`.

### Modelo de isolamento: shared schema + `tenant_id`
- **Um único schema PostgreSQL** para tudo (não há schema por empresa).
- Cada linha de **dados de negócio** carrega **`tenant_id`** (FK para
  `customers.Client`) — presente nos **26 models** dos 7 apps de negócio (R2).
- O tenant da request **não** vem do host/subdomínio: vem da **`TenantMembership`
  ativa** do usuário autenticado (R3). Superuser informa o tenant via header
  `X-Tenant-ID`.

### Três camadas de isolamento (defesa em profundidade)
1. **`TenantManager`** (`customers/managers.py`) — manager default dos 26 models;
   injeta `WHERE tenant_id = <atual>` em **toda** query `.objects` de runtime,
   guiado pelo **contexto de tenant da thread** (`customers/context.py`). O carimbo
   de `tenant_id` no create é um `pre_save` (`customers/scoping.py`). (R4)
2. **RLS de aplicação por papel** (`customers/querysets.py`:
   `apply_tenant_rls`/`apply_member_rls`) — limita ao tenant na camada de viewset e
   narrowa por papel. (R4)
3. **RLS nativo do PostgreSQL** (`migrations/0006_native_rls` + `customers/rls.py`)
   — `FORCE ROW LEVEL SECURITY` + policy por `app.current_tenant` nas 26 tabelas;
   vale quando a web conecta como a role **`app_user`** (`manage.py setup_rls`). (R7)

> A divisão `SHARED_APPS`/`TENANT_APPS` em `settings.py` permanece **só como
> documentação** — o `INSTALLED_APPS` efetivo é único e não depende mais dela.

### Identidade global vs autorização por tenant
- `users.User` vive no **`public`** (identidade global; `email`/`username` únicos
  globalmente; login único na plataforma).
- A autorização **dentro** de um tenant usa `customers.TenantMembership.role`,
  **não** o `users.User.role` (legado/global).
- **Só `is_superuser=True`** tem acesso operacional global (seed, provisionamento).

---

## 5. Regras de negócio essenciais

1. **Um usuário = uma empresa.** Um usuário pertence a no máximo **uma**
   `TenantMembership` **ativa** em toda a plataforma. Garantido por
   `UniqueConstraint(fields=['user'], condition=Q(is_active=True))` +
   `TenantMembership.clean()`. Vínculos **inativos** são permitidos (histórico /
   troca de empresa). Dentro da empresa, o usuário participa de **vários**
   projetos/equipes.

2. **Papéis de tenant** (`TenantMembership.role`): `owner`, `admin`, `manager`,
   `member`, `viewer`. Matriz inicial:
   | Papel | Permissão |
   |---|---|
   | `owner`/`admin` | tudo no tenant |
   | `manager` | tudo nos módulos de negócio |
   | `member` | leitura geral + escrita operacional (tarefas, documentos, comunicações) |
   | `viewer` | apenas leitura |

3. **RLS de aplicação** (além do isolamento físico por schema): em
   `customers/querysets.py` (`apply_tenant_rls`, `apply_member_rls`,
   `tenant_users_queryset`). `member` enxerga apenas recursos ligados a ele
   (autoria/atribuição/membership de projeto-equipe); papéis altos veem o tenant
   inteiro; sem membership ativa → queryset vazio; superuser → bypass.

4. **Quem cria empresa:** **superuser provisiona** o tenant e designa o 1º
   `owner` (não há self-service de criação de empresa). O `owner`/`admin` então
   **convida** os demais membros.

5. **Convites** (`customers.TenantInvitation`): token opaco, expiração
   configurável, papéis convidáveis `admin/manager/member/viewer` (owner é
   provisionado, nunca convidado), no máximo 1 convite pendente por
   `(tenant, email)`.

6. **Models em português.** Atenção: os nomes reais são `Projeto` (não
   `Project`), `Tarefa`, `Equipe`, `Risco`, `Custo`, etc., com campos `titulo`,
   `data_inicio`, `data_fim`, `criado_por`… Código/testes antigos que usavam
   nomes em inglês foram corrigidos — não recrie esse padrão.

---

## 6. Schemas / modelo de dados (resumo por app)

> Detalhamento e classificação public/tenant em `docs/database-review.md`.

### `users` (SHARED · public)
- **`User`** (custom, `AUTH_USER_MODEL`): `email`/`username` únicos, `role`
  legado (`ADMIN`, `PROJECT_MANAGER`, …), bloqueio por tentativas, política de
  senha. **`UserProfile`** (1-1, tema/notificações), **`AccessProfile` /
  `Permission` / `UserAccessProfile`** (RBAC legado global), **`PasswordHistory`**,
  **`AccessAttempt`**.

### `customers` — o coração do multi-tenant
- **`Client`** (= tenant; `models.Model` simples, `name`). Sem `schema_name`; o
  model `Domain` foi **removido** (R1).
- **`TenantMembership`** (user × tenant × role × is_active).
- **`TenantInvitation`** (convite por token).
- **`TenantSettings`** (1-1 com `Client`; `features`/`config` JSON — customização
  por empresa, R5). Ponto único de leitura: `customers.config`.
- Infra de isolamento: `managers.py` (`TenantManager`), `context.py` (contexto de
  thread), `scoping.py` (carimbo no create), `querysets.py` (RLS de app),
  `rls.py` + `setup_rls` (RLS nativo), `tenancy.py` (resolução por membership).

### Apps de negócio (cada model tem `tenant_id`)
- **`projects`**: `Projeto` (FK `criado_por`→User; FK circular nullable
  `custos`→`costs.Custo`), `MembroProjeto`, `HistoricoStatusProjeto`, `Sprint`.
- **`tasks`**: `Tarefa` (→`Projeto`/`Sprint`/User), `AtribuicaoTarefa`,
  `ComentarioTarefa`, `HistoricoStatusTarefa`.
- **`teams`**: `Equipe`, `MembroEquipe`, `PermissaoEquipe`.
- **`risks`**: `Risco` (matriz probabilidade×impacto → `nivel_risco`),
  `HistoricoRisco`.
- **`costs`**: `Categoria`, `Custo` (→`Projeto`/`Tarefa`), `OrcamentoProjeto`,
  `OrcamentoTarefa`, `Alerta`.
- **`documents`**: `Documento` (versionado), `HistoricoDocumento`, `Comentario`.
- **`communications`**: `ChatMensagem`, `ChatMensagemLeitura`, `Notificacao`,
  `ConfiguracaoNotificacao` (1-1 por usuário), `Comunicacao` (M2M
  `destinatarios`→User).

> **Dependência circular conhecida:** `projects.Projeto.custos ↔ costs.Custo`.
> Importa em migrações de dados (resolvida com gravação diferida no comando de
> migração — ver seção 11).

---

## 7. Autenticação e autorização (fluxo)

Ordem de defesa em uma requisição à API:

1. **`users.middleware.PermissionMiddleware`** (`users/middleware.py`): autentica
   o JWT (`Authorization: Bearer`), resolve a **`TenantMembership` ativa** (ou
   `X-Tenant-ID` p/ superuser), seta `request.tenant`/`tenant_id` e **ativa o
   contexto de tenant da thread** (deny-by-default; bypass p/ `/admin/` e
   superuser-global). Para caminhos tenant-scoped
   (`TENANT_MEMBERSHIP_REQUIRED_PATH_PREFIXES`), sem vínculo → **403**. Rotas em
   `PUBLIC_PATHS` (login, refresh, register, aceite de convite) ficam liberadas.
   Limpa o contexto em `process_response`/`process_exception`.
2. **`customers.rls.TenantDatabaseRLSMiddleware`**: abre transação e faz
   `SET LOCAL app.current_tenant` p/ a RLS nativa do PostgreSQL.
3. **DRF + Simple JWT** + **permissões por view** (`customers/permissions.py`):
   `IsTenantMember`, `HasTenantRole.with_roles(...)`, `IsTenantReader`.
4. **`TenantManager` + RLS** (`apply_tenant_rls`) filtram por `tenant_id` e papel.

Resumo de respostas: não autenticado em rota privada → **401**; autenticado sem
membership no tenant → **403**; membro → conforme papel.

**Endpoints de auth** (`/api/auth/`): `token/` (login), `token/refresh/`,
endpoints Djoser de conta/senha. Decisão registrada em
`docs/adr-0001-auth-multitenant.md` (mantém Djoser+JWT; allauth/SSO ficam p/ depois).

---

## 8. Principais fluxos

- **Login (frontend):** `stores/auth.ts` → `POST /api/auth/token/` → guarda
  access/refresh (Pinia + `useState`) → `GET /api/auth/users/me/` → injeta
  `Bearer` via interceptor (`plugins/api.ts`).
- **Provisionar empresa (superuser):**
  `manage.py provision_tenant --name "ACME" --owner-email owner@acme.com`
  (cria a linha `Client` + `TenantSettings` + conta/owner + membership; sem
  schema/domínio).
- **Convidar membro (owner/admin):** `POST /api/tenant/invitations/` (e-mail +
  role) → e-mail com link no **domínio único** do app (`FRONTEND_URL`); o tenant é
  resolvido pelo **token**, não pelo host.
- **Aceitar convite (público):** `GET /api/invitations/<token>/` (inspeção) →
  `POST /api/invitations/<token>/accept/` (cria conta nova **ou** vincula conta
  existente sem vínculo ativo).
- **Migrar base legada → shared schema:** `manage.py migrate_legacy_data
  --tenant <id|nome>` (ver seção 11).

---

## 9. Como rodar localmente

Detalhes em `backend/readme-backend.md`. Resumo:

### Backend
```bash
# 1) PostgreSQL local
docker compose up -d postgres            # sobe planify-postgres em 127.0.0.1:15432

cd backend
python -m venv venv && source venv/bin/activate   # (já existe ./venv no repo)
pip install -r requirements.txt
cp .env.example .env                      # USE_SQLITE=False; aponta p/ o Postgres

# 2) Migrações (banco único — migrate normal, NÃO migrate_schemas)
python manage.py migrate
python manage.py createsuperuser          # operador global (provisiona empresas)
python manage.py create_dev_tenant --name Demo   # cria a linha Client "Demo"

# 3) (opcional) RLS nativo: cria a role app_user p/ a web conectar sem bypass
python manage.py setup_rls

# 4) (opcional) dados de exemplo no tenant Demo
python seed_data.py                       # exige um Client; default SEED_TENANT=Demo

# 5) Subir a API
python manage.py runserver
```

Acesse a API em **`http://localhost:8000/`** (sem subdomínio por tenant). O tenant
de cada request é resolvido pela `TenantMembership` ativa do usuário autenticado;
o superuser opera global (ou escopa com o header `X-Tenant-ID`).

> ⚠️ Use **`migrate`** (banco único), **não** `migrate_schemas` (era do
> `django-tenants`, removido na R1). Para ativar a RLS nativa em runtime, rode a
> web conectando como `app_user` (`POSTGRES_USER=app_user`); sob a role dona do
> banco a RLS é inócua e a camada de aplicação segue isolando. SQLite só serve p/
> inspeção legada (`USE_SQLITE=True`).

### Frontend
```bash
cd frontend
npm install
cp .env.example .env                      # NUXT_PUBLIC_API_BASE_URL=http://127.0.0.1:8000
npm run dev                               # Nuxt em http://localhost:3000
# Regenerar o cliente da API a partir do OpenAPI:
npm run generate:api
```

---

## 10. API e documentação

- Swagger/OpenAPI: `http://<host>:8000/api/docs/` (e `/redoc/`, `/api/schema/`).
- Famílias de rotas (raiz em `backend/planify/urls.py`):
  `/api/auth/*`, `/api/projects/*`, `/api/tasks/*`, `/api/teams/*`,
  `/api/risks/*`, `/api/costs/*`, `/api/documents/*`, `/api/communications/*`,
  `/api/dashboard/`, `/api/user/dashboard/`, `/api/tenant/invitations/*`,
  `/api/invitations/<token>/*`, `/api/users/*`.
- Paginação DRF: `PAGE_SIZE = 10` (cuidado em testes: prefira asserções por
  existência, não contagem exata).

---

## 11. Testes e validação

### pytest (suíte canônica — exige PostgreSQL)
```bash
cd backend
pytest tests/ --create-db      # 1ª vez
pytest tests/ --reuse-db       # demais execuções
```
Base tenant-aware em `tests/tenant_base.py`: `TenantAPITestCase` cria um `Client`
de teste + usuário com membership + `APIClient` autenticado por **JWT** (sem host;
o tenant é resolvido pela membership). Exercita o caminho HTTP real, não
`force_authenticate`. Rode com a role **dona** do banco (não `app_user`).

### Scripts e2e (PostgreSQL real, idempotentes, com teardown)
```bash
python scripts/e2e_r4_tenant_isolation.py   # isolamento cross-tenant por tenant_id (16/16)
python scripts/e2e_r7_native_rls.py         # RLS nativo via app_user (7/7)
python scripts/e2e_invitations.py           # provisionamento + convites (13/13)
python scripts/e2e_migrate_legacy.py        # migração de dados legados (23/23)
```

---

## 12. Comandos de gestão úteis (`manage.py`)

- `migrate` — migrações do banco único (substitui o antigo `migrate_schemas`).
- `create_dev_tenant --name <nome>` — cria tenant de desenvolvimento (conveniência).
- `provision_tenant --name <nome> --owner-email <e>` — caminho **canônico** de
  provisionar empresa + owner (superuser).
- `setup_rls` — cria/atualiza a role `app_user` (sem `BYPASSRLS`) p/ a RLS nativa.
- `migrate_legacy_data --tenant <id|nome>` — onboarding de base single-tenant
  legada (SQLite) p/ o shared schema: identidade → `users`, negócio carimbado com
  `tenant_id`, com `--dry-run`, relatório de contagens e idempotência (ver R6/R8).
- `create_access_profiles` — semeia RBAC legado global.
- `seed_data.py` — dados de exemplo (script na raiz do backend, não é `manage.py`).

---

## 13. Estado atual da refatoração (fases)

Fonte de verdade: `docs/backend-multitenant-audit.md`. As **Fases 0–8** descrevem o
caminho schema-per-tenant original (histórico). A re-arquitetura **shared schema**
está nas fases **R0–R10**:

| Fase | Tema | Status |
|---|---|---|
| R0 | Registro da decisão (shared schema) | ✅ Concluída |
| R1 | Desativar `django-tenants` (banco único) | ✅ Concluída |
| R2 | `tenant_id` nos 26 models de negócio | ✅ Concluída |
| R3 | Resolução de tenant por membership (sem subdomínio) | ✅ Concluída |
| R4 | Isolamento central (`TenantManager`) + RLS de app | ✅ Concluída |
| R5 | Customização por tenant (`TenantSettings`) | ✅ Concluída |
| R6 | Migração de dados (schemas → shared) | ✅ Concluída |
| R7 | RLS nativo do PostgreSQL (`app_user`) | ✅ Concluída |
| **R8** | Testes/e2e na base shared | ✅ Concluída |
| **R9** | Provisionamento/convites sem schema/domínio | ✅ Concluída |
| **R10** | Docs e onboarding | ✅ Concluída |

**Próximas frentes naturais:** autorização a nível de objeto (ex.: `member` editar
só a tarefa atribuída a ele), Fase 11 (observabilidade/segurança: logs com tenant,
`MEDIA_ROOT` por tenant, refino de privilégios do `app_user`) e Fase 12 (integração
frontend — baseURL única, tela de convites, aceite; corrigir bugs conhecidos em
`frontend/plugins/api.ts`: `os.BACKEND_URL` → `runtimeConfig`; `authStore.token`
→ `authStore.accessToken`).

---

## 14. Armadilhas / convenções (leia antes de codar)

- **Models em PT-BR** (`Projeto`/`Tarefa`/…); campos `titulo`, `data_inicio`,
  `data_fim`, `criado_por`. Não use `Project`/`name`/`start_date`.
- **Todo model de negócio tem `tenant_id`** (FK p/ `Client`). O `TenantManager`
  filtra/carimba automaticamente **dentro de uma request**; fora de request (shell,
  scripts, seed) não há filtro — use `customers.context.scope(tenant_id=...)` para
  escopar e carimbar manualmente.
- **`queryset` de classe** (atributo de viewset / `queryset=` de campo de
  serializer) é avaliado no import, **sem** contexto → o manager não re-filtra. Por
  isso o `apply_tenant_rls` aplica o `filter(tenant=...)` explícito; a RLS nativa é
  o backstop de escrita cross-tenant.
- **Sempre aplicar RLS** (`apply_tenant_rls`/`apply_member_rls`) em queries
  manuais antes de agregar/serializar; ViewSets usam o mixin de RLS.
- **Usuário é global**: ao listar usuários para um tenant, use
  `tenant_users_queryset(request)` (evita vazamento cross-tenant via `User`).
- **`migrate`, não `migrate_schemas`.** PostgreSQL é obrigatório. Para a RLS nativa
  valer em runtime, conecte como `app_user`.
- **Acesse o app por `localhost:8000`** (sem subdomínio); o tenant vem da membership.
- **Convenção de commits do repo:** trabalho em fases na branch `Dev-tenant`,
  com validação registrada no audit doc a cada fase.

---

## 15. Glossário

- **Tenant / `Client`**: uma empresa = um schema PostgreSQL isolado.
- **`Domain`**: host que resolve para um tenant (ex.: `acme.localhost`).
- **`TenantMembership`**: vínculo usuário↔empresa com papel; no máx. 1 ativo/usuário.
- **`public`**: schema compartilhado (identidade, tenants).
- **RLS de aplicação**: filtro por papel/relacionamento nas queries (não é o RLS
  nativo do PostgreSQL).
- **owner**: 1º responsável da empresa (provisionado por superuser).
- **superuser**: operador global da plataforma (bypass total).

---

### Por onde começar a ler o código
1. `docs/multi-tenant-architecture.md` (conceito) →
2. `backend/customers/` (`models.py`, `querysets.py`, `permissions.py`) →
3. `backend/users/middleware.py` (gate de membership) →
4. um app de negócio, ex. `backend/projects/` (`models.py`, `views.py`) →
5. `docs/backend-multitenant-audit.md` (o que já foi feito e por quê).
