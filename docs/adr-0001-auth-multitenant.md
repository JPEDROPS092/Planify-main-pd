# ADR 0001 — Estratégia de Autenticação Multi-Tenant (Fase 7)

- Status: Aceita
- Data: 2026-06-01
- Branch: `Dev-tenant`
- Contexto: Fase 7 do plano `backend/codex-task-01.md`.

## Contexto

Com o isolamento por schema (`django-tenants`) e a camada de membership/RLS
estabilizados na Fase 6, a Fase 7 trata da estratégia de autenticação e do
ciclo de vida de acesso de usuários em um cenário multi-tenant: como uma
empresa ganha seu primeiro responsável e como os demais membros entram.

A stack atual é: `users.User` global (schema `public`, `email`/`username`
únicos globalmente), Simple JWT (access 7d, refresh 30d, rotação + blacklist),
Djoser para gestão de usuário/senha, e `PermissionMiddleware` central que já
exige `TenantMembership` ativa para os prefixos tenant-scoped.

Lacunas identificadas antes desta fase:

- O cadastro não cria `TenantMembership` (usuário entra sem acesso a tenant).
- Não havia fluxo formal de "primeiro owner" (apenas o `create_dev_tenant`).
- Não havia fluxo de convite de membros.

## Decisões

### 1. Manter Djoser + Simple JWT (não migrar agora)

Seguimos a recomendação do próprio plano: estabilizar o multi-tenant com a
auth atual antes de trocar a base. `django-allauth`/`django-tenant-users`
ficam como avaliação futura.

**Motivos:** menor risco; não quebra o frontend (que já consome
`/api/auth/token/` e endpoints Djoser); a identidade global e o login único já
atendem ao modelo "um usuário = uma empresa"; a autorização por tenant já está
resolvida via `TenantMembership` + RLS, independente da biblioteca de auth.

### 2. Provisionamento de tenant e primeiro owner: responsabilidade do superuser

Confirmado o modelo operacional: **o superuser provisiona** o tenant (schema +
`Client` + `Domain`) **e designa o owner**; o **owner popula e gerencia a
própria empresa**, inclusive convidando os demais membros. Não há self-service
de criação de empresa no cadastro público.

Implementado pelo management command `customers/provision_tenant`:

- cria `Client` + `Domain` (primário);
- cria a conta do owner (ou designa uma existente sem vínculo ativo);
- cria `TenantMembership(role=owner)`;
- ao criar conta nova, gera/aceita uma senha e exige troca no primeiro login
  quando a senha foi autogerada;
- respeita a regra "um usuário = uma empresa" (recusa owner já vinculado).

`create_dev_tenant` é mantido para conveniência de desenvolvimento;
`provision_tenant` é o caminho canônico de operação.

### 3. Fluxo de convite (owner/admin → membros)

O convite é uma ação **dentro do tenant**, feita por `owner`/`admin`. Modelado
por `customers.TenantInvitation` (modelo compartilhado, schema `public`, pois
envolve identidade global + empresa).

- Papéis convidáveis: `admin`, `manager`, `member`, `viewer` (o `owner` é
  provisionado, nunca convidado).
- Token opaco (`secrets.token_urlsafe`), expiração configurável
  (`TENANT_INVITATION_TTL_DAYS`, default 7 dias).
- No máximo um convite **pendente** por `(tenant, email)` (constraint parcial).
- O e-mail de convite aponta para o **domínio do próprio tenant** (subdomínio),
  caindo já no contexto correto.

Aceite (público, sem autenticação — o token comprova a posse do e-mail):

- **E-mail novo:** o aceite cria a conta (`username`/`full_name`/`password`) e
  a `TenantMembership` ativa, em uma transação.
- **E-mail já existente sem vínculo ativo** (ex.: troca de empresa): o aceite
  apenas cria a `TenantMembership` (o token é a prova; senha não é exigida nem
  alterada).
- **E-mail com vínculo ativo:** recusado (regra "um usuário = uma empresa"),
  tanto na criação do convite quanto no aceite (defesa pela constraint do
  banco).

### 4. Matriz de papéis (inalterada)

Permanece a matriz da Fase 6 (`owner`/`admin`/`manager`/`member`/`viewer`),
aplicada por `PermissionMiddleware` (gate por prefixo) e pelas permissões DRF
`IsTenantMember`/`HasTenantRole` (gate por view). A gestão de convites usa
`HasTenantRole.with_roles('owner', 'admin')`.

### 5. SSO/SAML/OIDC (futuro)

Fora de escopo agora. A adoção futura de `django-allauth` é o caminho natural
para social login/OIDC; SAML corporativo entraria por provider dedicado. A
decisão fica condicionada a demanda real e à estabilização dos contratos atuais.

## Endpoints adicionados

Gestão (tenant-scoped, `owner`/`admin`, sob `/api/tenant/` — prefixo protegido):

- `GET  /api/tenant/invitations/` — lista convites do tenant atual.
- `POST /api/tenant/invitations/` — cria convite (`email`, `role`) e envia e-mail.
- `GET  /api/tenant/invitations/{id}/` — detalhe.
- `POST /api/tenant/invitations/{id}/revoke/` — revoga convite pendente.
- `POST /api/tenant/invitations/{id}/resend/` — reenvia e-mail.

Público (sem autenticação, em `PUBLIC_PATHS`):

- `GET  /api/invitations/{token}/` — inspeção para a tela de aceite.
- `POST /api/invitations/{token}/accept/` — aceite do convite.

## Plano de migração do frontend

Não há mudança **obrigatória** imediata (login e reset seguem iguais). Para
habilitar o fluxo completo:

1. **Convite (área da empresa):** tela de gestão consumindo
   `/api/tenant/invitations/` (listar/criar/revogar/reenviar). Disponível só
   para owner/admin.
2. **Aceite (rota pública):** rota `/{TENANT_INVITATION_ACCEPT_PATH}` (default
   `/convite/{token}`) que chama `GET /api/invitations/{token}/` para renderizar
   e `POST .../accept/` para concluir; redireciona ao login do subdomínio do
   tenant ao final (campo `domain` no retorno).
3. **baseURL por subdomínio:** resolver o host/tenant ao montar `OpenAPI.BASE`
   (tratado em detalhe na Fase 12). Corrigir os bugs já existentes do
   `plugins/api.ts` (`os.BACKEND_URL` → `runtimeConfig`; `authStore.token` →
   `authStore.accessToken`).
4. **Cadastro público:** avaliar restringir/remover `registro.vue` em favor do
   convite, alinhado ao modelo "superuser provisiona, owner convida".

## Pendências e follow-ups

- **Bug pré-existente (corrigido):**
  `users/views.py::UserViewSet.reset_password` usava
  `User.objects.make_random_password()`, removido no Django 5.1 (o projeto está
  no 5.2) — o endpoint quebraria em runtime. Trocado por
  `django.utils.crypto.get_random_string(12)`.
- Aceite de usuário existente assume verificação de e-mail pela posse do link;
  se/quando houver verificação de e-mail formal, alinhar.
- Restrição/curadoria do cadastro público (item 4 acima) é decisão de produto.
- Autorização a nível de objeto (refinamento por entidade) segue como item da
  fase futura, conforme registrado na Fase 6.

## Validação

- `python manage.py check`: sem issues.
- `makemigrations customers`: `0003_tenantinvitation`; `migrate_schemas --shared` aplicado.
- `scripts/e2e_invitations.py`: 13/13 (provisionamento via command, criação de
  convite por owner, inspeção pública, aceite criando conta + membership,
  acesso do convidado, negação de member criando convite, reaceite, convite a
  usuário já vinculado, e negação de usuário sem vínculo).
- Regressão: `scripts/e2e_cross_tenant.py` 9/9; `pytest tests/` 27 passed.
