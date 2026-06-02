# Arquitetura Multi-Tenant - Backend Planify

## Decisões iniciais

- Banco alvo: PostgreSQL.
- Biblioteca de tenancy: `django-tenants`.
- Estratégia de isolamento: schema por empresa.
- Schema compartilhado: `public`.
- App de tenants recomendado: `customers`.
- Model de tenant recomendado: `Client`.
- Model de domínio recomendado: `Domain`.
- Autenticação inicial: manter `users.User`, Djoser e Simple JWT.
- Evolução de autenticação: avaliar `django-allauth` e/ou `django-tenant-users` depois do isolamento por schema estar validado.

## Modelo de escopo

### `SHARED_APPS`

Recomendação inicial:

```python
SHARED_APPS = [
    "django_tenants",
    "customers",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "rest_framework",
    "rest_framework_simplejwt",
    "djoser",
    "corsheaders",
    "django_filters",
    "drf_spectacular",
    "users",
    "core",
]
```

### `TENANT_APPS`

Recomendação inicial:

```python
TENANT_APPS = [
    "projects",
    "tasks",
    "teams",
    "risks",
    "costs",
    "documents",
    "communications",
]
```

`communications` deve passar por revisão detalhada: mensagens e comunicações formais são tenant; preferências de notificação podem ser públicas ou por membership.

## Usuário global e membership

Decisão: manter `users.User` no schema `public` com **identidade global**.

Regra de negócio confirmada: um usuário pertence a **uma única empresa**, mas a **vários projetos** dentro dela. A relação usuário ↔ muitos projetos é resolvida por `projects.MembroProjeto`/`teams.MembroEquipe` dentro do schema do tenant; não é tratada pela tenancy. A relação usuário ↔ empresa é única.

Motivo de manter `User` global mesmo com um usuário por empresa:

- Preserva o fluxo atual de login (um login para toda a plataforma).
- `email`/`username` permanecem únicos globalmente.
- Reduz risco e mudança em relação ao desenho atual.
- "Um usuário por empresa" é modelado como exatamente uma `TenantMembership` ativa por usuário, não como duplicação de identidade por schema.

Aplicação da regra: `customers.TenantMembership` possui `UniqueConstraint(fields=['user'], condition=Q(is_active=True))`, garantindo no máximo um vínculo **ativo** por usuário em toda a plataforma. Vínculos inativos são permitidos para histórico ou troca de empresa. O método `TenantMembership.clean()` reforça a mesma regra com mensagem amigável em admin/forms.

Novo model recomendado no app `customers`:

```python
class TenantMembership(models.Model):
    ROLE_OWNER = "owner"
    ROLE_ADMIN = "admin"
    ROLE_MANAGER = "manager"
    ROLE_MEMBER = "member"
    ROLE_VIEWER = "viewer"

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    tenant = models.ForeignKey(Client, on_delete=models.CASCADE)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("user", "tenant")
```

Roles iniciais:

- `owner`
- `admin`
- `manager`
- `member`
- `viewer`

## Autorização global vs tenant

Decisão formal:

- Apenas `users.User.is_superuser=True` tem acesso operacional global.
- Seed inicial, criação/gestão operacional de tenants e manutenção fora de contexto tenant são responsabilidade de superuser.
- `users.User.role` é legado/global e não deve liberar acesso cross-tenant.
- A autorização dentro de um tenant deve usar `customers.TenantMembership.role`.
- Usuário autenticado sem `TenantMembership` ativa no tenant atual recebe `403`.

Matriz inicial por papel tenant:

| Papel | Permissão inicial |
| --- | --- |
| `owner` | Todas as ações no tenant. |
| `admin` | Todas as ações no tenant. |
| `manager` | Todas as ações nos módulos de negócio do tenant. |
| `member` | Leitura geral e escrita operacional em tarefas, documentos e comunicações. |
| `viewer` | Apenas leitura. |

Essa matriz é deliberadamente inicial. Regras finas por entidade, propriedade do recurso e status do workflow devem ser refinadas na Fase 9, quando a suite de testes multi-tenant for reconstruída.

## Resolução de tenant

Decisão inicial: resolver tenant por subdomínio.

Formato de produção:

```text
empresa.planify.com
```

Formato local recomendado:

```text
empresa.localhost
```

Alternativa local caso DNS/browser gere atrito:

```text
empresa.planify.local
```

Nesse caso, documentar entrada em `/etc/hosts` para cada tenant local.

## Middleware e permissões

Ordem conceitual:

1. `django_tenants.middleware.main.TenantMainMiddleware` resolve o schema atual pelo host.
2. Autenticação DRF/Simple JWT identifica o usuário global.
3. Permissão customizada valida se o usuário possui `TenantMembership` ativa no tenant atual.
4. Permissão customizada valida a ação pelo `TenantMembership.role`.

Comportamento esperado:

- Usuário autenticado e membro do tenant: acesso permitido conforme role.
- Usuário autenticado sem membership no tenant atual: `403`.
- Usuário não autenticado em endpoint privado: `401`.
- Superuser tem acesso global para manutenção e seed inicial.

## RLS de aplicação nas queries

Além do isolamento físico por schema do `django-tenants`, a API deve aplicar uma camada de filtro por papel e relacionamento do usuário nas queries de negócio.

Decisão atual:

- `owner`, `admin`, `manager` e `viewer` podem ler o conjunto completo de dados do tenant.
- `viewer` continua limitado a métodos seguros pela camada de permissão.
- `member` lê apenas recursos ligados ao próprio usuário por autoria, atribuição, destinatário ou membership de projeto/equipe.
- Usuário sem `TenantMembership` ativa no tenant recebe queryset vazio nas views protegidas.
- `is_superuser=True` mantém bypass operacional global.

Implementação inicial:

- Helper central: `customers.querysets.apply_tenant_rls`.
- Mixin para ViewSets: `customers.querysets.TenantRLSQuerysetMixin`.
- ViewSets principais dos apps `projects`, `tasks`, `teams`, `risks`, `costs`, `documents` e `communications` aplicam RLS em `get_queryset`.
- Queries manuais em actions e relatórios devem chamar `apply_tenant_rls` explicitamente antes de agregações, `values`, `exclude` ou serialização.

Ressalva:

- Esta é uma camada de RLS de aplicação, não PostgreSQL Row Level Security nativo.
- PostgreSQL RLS nativo pode ser avaliado depois que os contratos de autorização e os relacionamentos finais estiverem estabilizados.

## Ordem técnica recomendada

1. Introduzir configuração de PostgreSQL via variáveis de ambiente. Status: validado localmente com Docker.
2. Criar app `customers` com `Client`, `Domain` e `TenantMembership`. Status: concluído inicialmente.
3. Configurar `django-tenants`, `SHARED_APPS`, `TENANT_APPS`, `TENANT_MODEL`, `TENANT_DOMAIN_MODEL` e router. Status: concluído inicialmente.
4. Validar `migrate_schemas --shared`, `check` e fluxo básico em PostgreSQL. Status: validado localmente.
5. Criar tenant local de desenvolvimento. Status: validado com `demo.localhost`.
6. Rodar migrações shared e tenant. Status: validado para schemas `public` e `demo`.
7. Revisar views/serializers para garantir que consultas executem no schema resolvido. Status: em andamento.
8. Criar testes com dois tenants e dados homônimos para validar isolamento.

## Validação local realizada

- PostgreSQL local via Docker Compose em `127.0.0.1:15432`.
- `python manage.py check` sem erros.
- `python manage.py migrate_schemas --shared` aplicado no schema `public`.
- `python manage.py create_dev_tenant --schema demo --name Demo --domain demo.localhost` criou o schema tenant.
- `python manage.py migrate_schemas --tenant --schema demo --check` retornou status `0`.
- Tabelas compartilhadas confirmadas no schema `public`: auth/admin/session, `users` e `customers`.
- Tabelas de negócio confirmadas no schema `demo`: `projects`, `tasks`, `teams`, `risks`, `costs`, `documents` e `communications`.

## Pontos de atenção antes de implementar

- Resolver a divergência `Project` vs `Projeto` nos testes existentes.
- Revisar a dependência cruzada `Projeto -> Custo` e `Custo -> Projeto`.
- Definir se `AccessProfile` permanece global ou vira role por tenant via `TenantMembership`.
- Definir particionamento de arquivos em `MEDIA_ROOT` por tenant.
- Definir estratégia para dados existentes: tenant destino único ou migração por regras externas.
