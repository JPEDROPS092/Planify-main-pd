# Arquitetura Multi-Tenant — Backend Planify

> **Modelo atual (a partir de 2026-06-03): shared schema + `tenant_id`.**
> O projeto começou com **schema-per-tenant** (`django-tenants`); a estratégia foi
> revista nas fases **R0–R10** (plano em `docs/rearquitetura-shared-schema-plano.md`,
> acompanhamento em `docs/backend-multitenant-audit.md`). Hoje há **um único schema
> PostgreSQL** e cada linha de negócio carrega `tenant_id`. As referências a
> `Domain`, `schema_name`, `migrate_schemas` e subdomínio descrevem o **modelo
> antigo** e não valem mais. O histórico do desenho schema-per-tenant ficou
> preservado no git.

## Decisões vigentes

- **Banco:** PostgreSQL, **um único schema** (`public`); SQLite só p/ inspeção legada.
- **Isolamento:** `tenant_id` inteiro (FK para `customers.Client`) em **todos** os
  26 models de negócio, com filtro **central** (não por schema).
- **App de tenancy:** `customers`. Model de empresa: `Client` (sem `Domain`/schema).
- **Resolução de tenant:** **sem subdomínio** — vem da `TenantMembership` ativa do
  usuário autenticado. Superuser informa o tenant via header `X-Tenant-ID`.
- **Identidade:** `users.User` global (login único; `email`/`username` únicos
  globalmente). Autorização dentro do tenant por `TenantMembership.role`.
- **Customização por empresa:** `customers.TenantSettings` (feature-flags/config);
  schema físico separado é **exceção dura** (contrato/lei), não o caminho padrão.
- **Autenticação:** `users.User` + Djoser + Simple JWT (ver `docs/adr-0001-auth-multitenant.md`).

## Camadas de isolamento (defesa em profundidade)

O isolamento por `tenant_id` é garantido em **três camadas**:

1. **`TenantManager` (app)** — manager default dos 26 models de negócio
   (`customers/managers.py`). Em runtime, dentro de uma request, injeta
   `WHERE tenant_id = <atual>` em **toda** query `.objects` automaticamente,
   conforme o **contexto de tenant da thread** (`customers/context.py`). Cobre as
   dezenas de `.objects` diretas (dashboards, serializers, exports, métodos de
   model) que não passam pelo viewset. O carimbo de `tenant_id` no create é feito
   por um `pre_save` (`customers/scoping.py`).
2. **RLS de aplicação por papel (app)** — `customers/querysets.py`
   (`apply_tenant_rls`/`apply_member_rls`). Aplica o limite de tenant
   **explicitamente** na camada de viewset (o `queryset` de classe é avaliado no
   import, sem contexto) e narrowa por papel: `owner/admin/manager/viewer` veem o
   tenant inteiro; `member` vê só recursos ligados a ele (autoria/atribuição/
   membership); sem membership ativa → vazio; superuser → bypass.
3. **RLS nativo do PostgreSQL (banco)** — `ENABLE`+`FORCE ROW LEVEL SECURITY` +
   policy `tenant_isolation` nas 26 tabelas (`customers/migrations/0006_native_rls`),
   dirigida pela GUC `app.current_tenant` (setada por transação pelo
   `TenantDatabaseRLSMiddleware`, `customers/rls.py`). É a rede de segurança no
   banco: mesmo uma query sem filtro de aplicação não vaza entre tenants. Vale
   quando a app conecta como a role **`app_user`** (sem `BYPASSRLS`, criada por
   `manage.py setup_rls`); sob a role dona/superuser do banco o RLS é inócuo e a
   camada de aplicação segue isolando.

## Usuário global e membership

`users.User` vive na identidade global. Regra de negócio: **um usuário pertence a
uma única empresa** (e a vários projetos dentro dela). Modelado como **no máximo
uma `TenantMembership` ativa** por usuário em toda a plataforma:

- `customers.TenantMembership`: `UniqueConstraint(fields=['user'], condition=Q(is_active=True))`
  + `clean()` com mensagem amigável. Vínculos **inativos** são permitidos
  (histórico/troca de empresa).
- Papéis: `owner`, `admin`, `manager`, `member`, `viewer`.

Ao listar usuários para um tenant, use `customers.querysets.tenant_users_queryset`
(evita vazamento cross-tenant via o `User` compartilhado).

## Autorização global vs tenant

- Apenas `is_superuser=True` tem acesso operacional global (seed, provisionamento,
  manutenção). `users.User.role` é legado/global e **não** concede acesso cross-tenant.
- Autorização dentro do tenant usa `TenantMembership.role`.
- Usuário autenticado sem `TenantMembership` ativa → **403** em rotas tenant-scoped.

| Papel | Permissão |
| --- | --- |
| `owner`/`admin` | Tudo no tenant. |
| `manager` | Tudo nos módulos de negócio. |
| `member` | Leitura geral + escrita operacional (tarefas, documentos, comunicações). |
| `viewer` | Apenas leitura. |

## Fluxo de uma request (ordem de defesa)

1. **`users.middleware.PermissionMiddleware`**: autentica o JWT, resolve a
   `TenantMembership` ativa (ou `X-Tenant-ID` p/ superuser), seta
   `request.tenant`/`request.tenant_id` e **ativa o contexto de tenant da thread**
   (deny-by-default; bypass p/ `/admin/` e superuser-global). Para prefixos
   tenant-scoped (`TENANT_MEMBERSHIP_REQUIRED_PATH_PREFIXES`), sem vínculo → **403**.
   Limpa o contexto em `process_response`/`process_exception`.
2. **`customers.rls.TenantDatabaseRLSMiddleware`**: abre a transação e faz
   `SET LOCAL app.current_tenant` (espelha o contexto da camada 1) p/ a RLS nativa.
3. **DRF + Simple JWT** + permissões por view (`customers/permissions.py`:
   `IsTenantMember`, `HasTenantRole.with_roles(...)`, `IsTenantReader`).
4. **`TenantManager` + `apply_tenant_rls`** filtram as queries por `tenant_id` e papel.

Respostas: não autenticado em rota privada → **401**; autenticado sem membership →
**403**; membro → conforme papel.

## Provisionamento e convites

- **Provisionar empresa (superuser):** `manage.py provision_tenant --name "ACME"
  --owner-email owner@acme.com` cria a linha `Client` (dispara o `post_save` que
  cria as `TenantSettings`), a conta/owner e a `TenantMembership(owner)`. Não há
  schema nem `Domain`. `create_dev_tenant` é o atalho de dev.
- **Convidar (owner/admin):** `POST /api/tenant/invitations/` (`customers.TenantInvitation`,
  token opaco). O e-mail leva ao **domínio único** do app (`FRONTEND_URL` +
  `TENANT_INVITATION_ACCEPT_PATH`); o tenant é resolvido pelo **token**, não pelo host.
- **Aceitar (público):** `GET /api/invitations/<token>/` (inspeção) e
  `POST /api/invitations/<token>/accept/` (cria conta nova **ou** vincula conta
  existente sem vínculo ativo, respeitando "um usuário = uma empresa").

## Migração de dados legados

`manage.py migrate_legacy_data` faz onboarding de um SQLite single-tenant legado
para o shared schema: identidade global → `users` (dedup por e-mail, hash
preservado); negócio → tabelas compartilhadas **carimbando `tenant_id`** com o
`Client` destino (`--tenant <id|nome>`). Preserva PKs e remapeia FKs de usuário;
idempotente; `--dry-run` simula. Ver `docs/backend-multitenant-audit.md` (R6/R8).

## Comandos (shared schema)

```bash
python manage.py migrate                 # banco único (NÃO migrate_schemas)
python manage.py create_dev_tenant --name Demo
python manage.py provision_tenant --name "ACME" --owner-email owner@acme.com
python manage.py setup_rls               # cria a role app_user (RLS nativo)
python seed_data.py                      # SEED_TENANT (default "Demo")
```

## Testes e validação

- **pytest** (`tests/`, base `tests/tenant_base.py`): sem `django-tenants`; cria
  `Client` + `TenantMembership` + JWT; tenant resolvido por membership; exercita o
  caminho HTTP real. `pytest tests/ --create-db` (1ª vez) / `--reuse-db`.
- **e2e** (`scripts/`, PostgreSQL real, idempotentes):
  `e2e_r4_tenant_isolation.py` (isolamento cross-tenant por `tenant_id`),
  `e2e_r7_native_rls.py` (RLS nativo via `app_user`), `e2e_invitations.py`
  (provisionamento + convites), `e2e_migrate_legacy.py` (migração de dados).

## Pontos em aberto

- **RBAC legado** (`AccessProfile`/`Permission`/`UserAccessProfile`): segue global,
  fora do escopo de migração automática; decisão "global vs por tenant" em aberto.
- **`MEDIA_ROOT` por tenant**: particionamento físico de arquivos é item de
  operação/segurança (Fase 11).
- **Autorização a nível de objeto** (ex.: `member` editar só a tarefa atribuída a
  ele): refinamento de produto sobre a base de isolamento já estabelecida.
- **Refino de privilégios do `app_user`** por tabela (hardening, Fase 11).
