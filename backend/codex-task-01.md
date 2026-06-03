# Codex Task 01: Plano de Refatoração Multi-Tenant do Backend

**Projeto:** Planify

## Objetivo

Planejar e executar, em fases, a refatoração do backend do Planify para uma arquitetura SaaS multi-tenant usando PostgreSQL, `django-tenants` e, em etapa posterior, uma camada de autenticação mais robusta com `django-allauth` e/ou `django-tenant-users`.

**Objetivo técnico:** garantir isolamento forte de dados por empresa, mantendo usuários, permissões, administração, API e testes coerentes com o novo modelo.

## Contexto Atual

### Stack

- Django
- Django REST Framework
- Simple JWT
- Djoser
- SQLite em desenvolvimento

### Domínios

- `users`
- `projects`
- `tasks`
- `teams`
- `risks`
- `costs`
- `documents`
- `communications`
- `core`

### Problema

Os dados estão no mesmo banco/schema sem fronteira formal de tenant/empresa, aumentando o risco de vazamento de dados entre clientes e dificultando backup, auditoria, restauração e manutenção por cliente.

## Decisão Arquitetural

- PostgreSQL como banco principal.
- `django-tenants` para isolamento por schema.
- Um app de tenants, chamado `customers` ou `tenants`.
- Schema `public` para dados compartilhados.
- Um schema por empresa/cliente para dados de negócio.
- Usuário global com associação a uma ou mais empresas.
- Autenticação atual mantida na primeira fase para reduzir risco.
- Avaliação posterior de `django-allauth` e `django-tenant-users`.

## Revisão de Decisão Arquitetural (2026-06-03) — Shared Schema + `tenant_id`

> Esta seção **supersede** a "Decisão Arquitetural" original (schema-per-tenant via
> `django-tenants`) para os dados de negócio. O histórico das Fases 0–8 fica
> preservado como registro do caminho percorrido; a partir daqui o alvo é
> **um único schema compartilhado com coluna `tenant_id`**. O acompanhamento da
> execução é feito pelas fases `R0–R10` (ver "Plano da Re-arquitetura" abaixo) e
> registrado em `docs/backend-multitenant-audit.md`.

**Decisão:** abandonar o isolamento por schema (`django-tenants`) e adotar um
**único schema compartilhado com `tenant_id` em todos os dados de negócio**, com
isolamento garantido por uma **camada central de aplicação** (manager/queryset que
injeta o filtro por `tenant_id` + RLS de aplicação recriada sobre essa coluna), e
PostgreSQL RLS nativo como rede de segurança futura.

**Motivação:**

- **Volume de tenants padronizados.** O produto é um SaaS onde muitas empresas
  usam o mesmo serviço, da mesma forma. Schema-per-tenant infla o banco (cada
  empresa duplica ~30 tabelas + índices + sequences; com milhares de empresas o
  catálogo do PostgreSQL explode e as migrations rodam uma vez por schema).
  Shared schema escala melhor nesse eixo.
- **Menos dependência de infra externa.** Resolver o tenant por subdomínio exige
  DNS/wildcard/certificado por tenant. Resolver por `tenant_id` (derivado da
  `TenantMembership` ativa do usuário autenticado) remove essa dependência.
- **Customização por tenant não exige schema separado.** Regras de negócio
  diferentes por empresa são resolvidas com **config/feature-flags por tenant**
  (settings ligados ao `Client`). Schema físico separado fica como **exceção
  rara**, só sob exigência dura (contrato/lei de separação física dos dados).

**Decisões técnicas fixadas:**

- **`tenant_id` é FK inteiro** para `customers.Client` (mantém os PKs inteiros
  atuais). Escolha deliberada para **reduzir o tamanho da migração** (sem troca de
  PK para UUID). A não-enumerabilidade (UUID) pode ser reavaliada depois, se o id
  de tenant passar a vazar em URL/API.
- **`customers.Client` permanece como registro da empresa (tenant)**;
  `customers.Domain` deixa de ser necessário (sem resolução por host).
- `django-tenants`, `TenantMainMiddleware`, `SHARED_APPS`/`TENANT_APPS` e o router
  de schema são **removidos**; tudo passa a viver num único schema (`public`).
- `TenantMembership` continua sendo a fonte do vínculo usuário↔empresa e do papel;
  o `tenant_id` da request vem da membership **ativa** do usuário (sem subdomínio).
  Superuser informa o tenant explicitamente (header/param) para operação global.
- A "RLS de aplicação" (`apply_tenant_rls`/`apply_member_rls`) é **recriada** sobre
  `tenant_id` (hoje ela assume o isolamento físico por schema).
- O isolamento é **centralizado num manager/queryset default**; "auditar as
  queries" significa garantir que nenhuma query escape desse filtro
  (`.objects` cru, `raw()`, agregações soltas) — **não** espalhar `WHERE
  tenant_id = ?` manualmente (caminho que vaza ao esquecer um ponto).

## Resultado Esperado

- Cada empresa terá seu próprio schema no PostgreSQL.
- Projetos, tarefas, equipes, riscos, custos, documentos e comunicações ficarão isolados por tenant.
- Usuários poderão acessar apenas tenants permitidos.
- APIs resolverão o tenant por domínio/subdomínio.
- Testes cobrirão criação de tenant, migrações, autenticação e isolamento de dados.
- O admin Django funcionará respeitando o contexto de tenant.
- A documentação explicará como criar, migrar, testar e operar tenants.

## Fases

### Fase 0: Preparação e Baseline

**Checklist**

- [ ] Criar branch específica para a refatoração.
- [ ] Rodar `python manage.py check` e registrar estado atual.
- [ ] Rodar testes existentes com `pytest` e registrar falhas atuais.
- [ ] Gerar backup do `backend/db.sqlite3`.
- [ ] Exportar dump dos dados atuais, se existirem dados importantes.
- [ ] Confirmar versão do Python e dependências atuais.
- [ ] Registrar endpoints principais que precisam continuar funcionando.
- [ ] Registrar modelos customizados de usuário, permissão e perfis.

**Entregáveis**

- Relatório curto do estado atual.
- Lista de falhas conhecidas antes da refatoração.
- Backup local do banco atual.

### Fase 1: Review Completo do Banco e dos Domínios

**Checklist**

- [ ] Mapear todos os models por app.
- [ ] Listar campos, tipos, `ForeignKey`, `ManyToMany`, `OneToOne` e constraints.
- [ ] Identificar models de negócio.
- [ ] Identificar models de autenticação, permissão e configuração global.
- [ ] Identificar models que podem ficar no schema `public`.
- [ ] Identificar models que devem ficar dentro de cada tenant.
- [ ] Criar mapa textual ou diagrama ER dos relacionamentos.
- [ ] Identificar dependências circulares e relacionamentos entre apps.
- [ ] Identificar modelos que apontam para `settings.AUTH_USER_MODEL`.
- [ ] Classificar cada tabela como global/pública, tenant ou híbrida.

**Entregáveis**

- Documento `docs/database-review.md`.
- Tabela de models por escopo: public, tenant ou híbrido.
- Lista de riscos de migração.

### Fase 2: Desenho da Nova Arquitetura

**Checklist**

- [ ] Definir `SHARED_APPS` e `TENANT_APPS`.
- [ ] Definir `INSTALLED_APPS` compatibilizado com `django-tenants`.
- [ ] Decidir nome do app de tenants: `customers` ou `tenants`.
- [ ] Decidir nomes dos models: `Client`, `Tenant`, `Domain`.
- [ ] Escolher resolução de tenant por subdomínio, como `empresa.planify.com`.
- [ ] Definir comportamento local: `empresa.localhost` ou host customizado.
- [ ] Decidir se usuário continua global e pode pertencer a várias empresas.
- [ ] Definir roles por tenant: `owner`, `admin`, `manager`, `member`, `viewer`.

**Entregáveis**

- Documento `docs/multi-tenant-architecture.md`.
- Decisão formal sobre usuário global vs usuário por tenant.
- Decisão formal sobre subdomínios.

### Fase 3: Migração para PostgreSQL

**Checklist**

- [ ] Adicionar dependências de PostgreSQL, como `psycopg` ou `psycopg2-binary`.
- [ ] Criar banco local PostgreSQL para desenvolvimento.
- [ ] Configurar `DATABASES` via variáveis de ambiente.
- [ ] Remover dependência direta de SQLite da configuração principal.
- [ ] Rodar `python manage.py migrate` em banco PostgreSQL limpo.
- [ ] Rodar `python manage.py check` e testes.
- [ ] Documentar setup PostgreSQL no README do backend.

**Entregáveis**

- Backend funcionando em PostgreSQL.
- README atualizado.
- Testes ou checks executados contra PostgreSQL.

### Fase 4: Introdução do django-tenants

**Checklist**

- [ ] Instalar `django-tenants`.
- [ ] Criar app `customers` ou `tenants`.
- [ ] Criar model de tenant herdando `TenantMixin`.
- [ ] Criar model de domínio herdando `DomainMixin`.
- [ ] Configurar `TENANT_MODEL`, `TENANT_DOMAIN_MODEL` e `DATABASE_ROUTERS`.
- [ ] Configurar middleware `TenantMainMiddleware`.
- [ ] Separar `SHARED_APPS`, `TENANT_APPS` e `INSTALLED_APPS`.
- [ ] Rodar migrações shared e tenant.
- [ ] Criar tenant de desenvolvimento e validar acesso.

**Entregáveis**

- Tenant inicial criado.
- Projeto sobe com middleware de tenant.
- Admin acessível no contexto correto.
- Comandos de migração documentados.

### Fase 5: Classificação e Movimentação dos Apps

**Checklist**

- [ ] Mover apps globais para `SHARED_APPS`.
- [ ] Mover apps de negócio para `TENANT_APPS`.
- [ ] Revisar imports e referências entre apps shared e tenant.
- [ ] Ajustar serializers e views que assumem banco único.
- [ ] Ajustar admin que registra models tenant.
- [ ] Revisar signals, managers e querysets.

**Entregáveis**

- Apps organizados entre shared e tenant.
- Admin sem erro de registro ou schema.
- API principal funcionando dentro de um tenant.

### Fase 6: Membership, Permissões e Isolamento

**Checklist**

- [ ] Criar modelo de membership usuário-tenant.
- [ ] Definir roles por tenant.
- [ ] Adaptar middleware/permissões para validar membership no tenant atual.
- [ ] Garantir que usuário autenticado sem acesso ao tenant receba `403`.
- [ ] Garantir que usuário autenticado em tenant A não acesse tenant B.
- [ ] Revisar permissões DRF e serializers que expõem usuários.

**Entregáveis**

- Usuário com acesso controlado por tenant.
- Testes de acesso negado entre tenants.
- Permissões documentadas.

### Fase 7: Refatoração de Autenticação

**Checklist**

- [ ] Revisar fluxos atuais de login, cadastro, reset e troca de senha.
- [ ] Mapear endpoints Djoser usados pelo frontend.
- [ ] Decidir se Djoser será mantido ou removido.
- [ ] Avaliar `django-allauth` e/ou `django-tenant-users`.
- [ ] Definir convites para entrada em tenant.
- [ ] Definir fluxo de primeiro usuário owner do tenant.
- [ ] Definir estratégia futura para SSO/SAML/OIDC.

**Entregáveis**

- ADR sobre estratégia de auth.
- Plano de migração de endpoints do frontend.
- Implementação incremental sem quebrar login atual.

### Fase 8: Migração de Dados Existentes

**Checklist**

- [ ] Definir tenant destino para dados atuais.
- [ ] Criar script de migração de dados.
- [ ] Migrar usuários globais.
- [ ] Migrar dados de negócio para schema do tenant destino.
- [ ] Validar contagens antes/depois por tabela.
- [ ] Validar integridade referencial.
- [ ] Validar arquivos de media/documentos e históricos.

**Entregáveis**

- Script de migração versionado.
- Relatório de contagens antes/depois.
- Plano de rollback.

### Fase 9: Testes

**Checklist**

- [ ] Criar tenant em teste; criar dois tenants em teste.
- [ ] Verificar schema ativo por request.
- [ ] Garantir que listagem de tenant A não retorna dados do tenant B.
- [ ] Garantir isolamento: tarefas, custos, riscos e documentos.
- [ ] Usuário membro acessa tenant permitido; não membro recebe `403`.
- [ ] Testes de regressão: Projects, Tasks, Teams, Risks, Costs, Documents, Communications, Users.

**Entregáveis**

- Suite de testes multi-tenant.
- Cobertura mínima para isolamento entre tenants.
- Documentação de como rodar testes tenant.

### Fase 10: Admin, Docs e Operação

**Checklist**

- [ ] Ajustar Django Admin para contexto multi-tenant.
- [ ] Criar comandos para criar, listar e migrar tenants.
- [ ] Documentar processo de onboarding de nova empresa.
- [ ] Documentar backup/restauração por tenant.
- [ ] Documentar estratégia de domínios.
- [ ] Atualizar Swagger/OpenAPI e README do backend.

**Entregáveis**

- Guia operacional de tenants.
- README atualizado.
- Comandos administrativos documentados.

### Fase 11: Observabilidade e Segurança

**Checklist**

- [ ] Garantir logs com identificador do tenant.
- [ ] Garantir auditoria de ações sensíveis.
- [ ] Revisar CORS, `ALLOWED_HOSTS`, cookies, JWT e HTTPS para produção.
- [ ] Definir rate limiting.
- [ ] Definir backup por tenant.
- [ ] Definir monitoramento de migrations por tenant.

**Entregáveis**

- Checklist de segurança para produção.
- Logs com tenant.
- Plano de backup/restauração.

### Fase 12: Frontend e Integração

**Checklist**

- [ ] Definir como o frontend escolhe ou recebe o tenant.
- [ ] Ajustar URLs por subdomínio.
- [ ] Ajustar login para contexto de empresa.
- [ ] Ajustar armazenamento de token considerando tenant.
- [ ] Ajustar telas de administração de organização.
- [ ] Testar fluxo completo: cadastro, login, criar projeto, criar tarefa.

**Entregáveis**

- Frontend consumindo API tenant-aware.
- Fluxo de troca/acesso de empresa documentado.

## Ordem de Execução

1. Fazer review completo do banco e relacionamentos.
2. Documentar classificação public/tenant/híbrido.
3. Migrar ambiente para PostgreSQL.
4. Introduzir `django-tenants` com tenant mínimo.
5. Separar apps em shared e tenant.
6. Ajustar permissões e membership.
7. Criar testes de isolamento.
8. Migrar dados existentes.
9. Revisar auth e decidir `allauth`/`tenant-users`.
10. Atualizar frontend.
11. Preparar operação, backup e produção.

## Critérios de Aceite

- [ ] `python manage.py check` passa.
- [ ] Migrações shared passam.
- [ ] Migrações tenant passam.
- [ ] Pelo menos dois tenants podem existir simultaneamente.
- [ ] Dados de tenant A não aparecem em tenant B.
- [ ] Usuário sem membership não acessa tenant.
- [ ] Admin funciona no contexto esperado.
- [ ] Swagger/docs continuam acessíveis.
- [ ] Testes principais passam.
- [ ] README e docs operacionais estão atualizados.

## Riscos Principais

- Quebra de autenticação atual.
- Frontend dependendo de endpoints Djoser atuais.
- Models shared importando models tenant.
- Dados históricos sem tenant claro.
- Notificações e permissões misturando escopos.
- Admin Django registrando models no schema errado.
- Testes existentes assumindo banco único.
- Complexidade de migrações em todos os tenants.

## Recomendação Final

Não iniciar pela troca para `django-allauth`. Primeiro estabilizar PostgreSQL e `django-tenants` com a autenticação atual. Depois, com isolamento por tenant validado, executar a refatoração de auth como uma segunda frente controlada.

## Plano da Re-arquitetura para Shared Schema (a partir de 2026-06-03)

> **Plano de execução detalhado (passo a passo, arquivos, validação, riscos) em
> `docs/rearquitetura-shared-schema-plano.md`.** Esta seção é o checklist resumido.

Numeração `R` para distinguir das fases originais (schema-per-tenant). Cada fase
segue o mesmo protocolo: executar → validar → registrar no
`docs/backend-multitenant-audit.md`. O *playbook* de migração de dados segue a
ordem segura: **adicionar coluna nullable → backfill → só então `NOT NULL` + FK**.

### Fase R0 — Registro da decisão

- [x] Documentar o pivô em `codex-task-01.md` (seção "Revisão de Decisão
      Arquitetural") e em `docs/backend-multitenant-audit.md`.
- [x] Fixar decisões: `tenant_id` inteiro, manager central, sem subdomínio,
      customização por config/feature-flags.

### Fase R1 — Desativar `django-tenants` (banco único) ✅

- [x] Remover `django_tenants` de `INSTALLED/SHARED/TENANT_APPS`,
      `TenantMainMiddleware`, `TENANT_MODEL`/`TENANT_DOMAIN_MODEL`, `DATABASE_ROUTERS`.
- [x] Consolidar tudo num único schema (`public`).
- [x] `Client` deixa de herdar `TenantMixin`/`auto_create_schema`; vira registro
      puro da empresa. `Domain` **removido**.
- [x] Critério: `manage.py check` + `migrate` em banco limpo. Validado e
      registrado em `docs/backend-multitenant-audit.md` (Fase R1).

### Fase R2 — `tenant_id` nos models de negócio (passos 1, 2, 3, 4 do playbook) ✅

- [x] **(passo 1)** `Client` como tabela raiz de tenant (já existe; reusado).
- [x] **(passo 2)** `tenant = FK(customers.Client, CASCADE)` em todos os 26 models
      de `projects/tasks/teams/risks/costs/documents/communications`. Banco vazio
      → **single-step `NOT NULL`** (sem nullable→backfill; backfill real fica na R6).
      Decisão: `on_delete=CASCADE` (apaga dados do tenant junto com o `Client`).
- [x] **(passo 3)** Índices compostos `Index(['tenant', <ordering>])` em todo model
      com `Meta.ordering`.
- [x] **(passo 4)** `Projeto.titulo` (único `unique=True` global) →
      `UniqueConstraint(['tenant','titulo'])`. Demais uniques já são tenant-safe via
      FK pai; mantidos. Registrado em `docs/backend-multitenant-audit.md` (Fase R2).

### Fase R3 — Resolução de tenant por membership (sem subdomínio) ✅

- [x] `customers/tenancy.resolve_request_tenant` + `PermissionMiddleware._set_request_tenant`
      definem `request.tenant`/`tenant_id`/`_tenant_membership` a partir da
      `TenantMembership` ativa do usuário autenticado.
- [x] Superuser: tenant explícito via header `X-Tenant-ID` (ou query `?tenant=`).
- [x] `querysets.py`/`permissions.py`/`middleware.py` deixaram de depender de
      `schema_name`/`PUBLIC_SCHEMA_NAME`; sem tenant resolvido → `none()`/403.
- [x] `emails.py`/`views.py`: URL de convite por `FRONTEND_URL` + token (sem
      `.domains`/subdomínio). Validado 9/9. Registrado no audit (Fase R3).

### Fase R4 — Isolamento centralizado (manager/queryset) + RLS (passo 5 do playbook)

- [ ] Manager/QuerySet default que filtra por `tenant_id` da request
      automaticamente; mixin de viewset; set automático de `tenant_id` no create.
- [ ] Recriar `apply_tenant_rls`/`apply_member_rls` sobre `tenant_id`.
- [ ] **(passo 5)** Auditar e eliminar queries que escapam do manager
      (`.objects` cru, `raw()`, agregações soltas).

### Fase R5 — Customização por tenant

- [ ] Model `TenantSettings`/campos no `Client` para config/feature-flags por
      empresa. Schema físico separado só como exceção documentada.

### Fase R6 — Migração de dados (schemas → shared)

- [ ] Trazer dados dos schemas existentes (`demo`) para as tabelas compartilhadas,
      populando `tenant_id`. Custo baixo (sem empresas reais em produção).
- [ ] Adaptar/aposentar `migrate_legacy_data` para o novo alvo.

### Fase R7 — PostgreSQL RLS nativo (rede de segurança)

- [ ] Policies nativas por `tenant_id` como segunda camada, após contratos estáveis.

### Fase R8 — Testes

- [ ] Reescrever base de testes e e2e para isolamento por `tenant_id` (sem
      schema/host): dois tenants, dados homônimos, negação cross-tenant.

### Fase R9 — Provisionamento e convites

- [ ] `provision_tenant` cria só a linha `Client` (sem schema) + owner +
      membership. Fluxo de convites mantido.

### Fase R10 — Docs e onboarding

- [ ] Atualizar `ONBOARDING.md`, `readme-backend.md` e
      `docs/multi-tenant-architecture.md` para o modelo shared.
