# Planify Backend

Backend da API Planify, desenvolvido com Django, Django REST Framework e autenticação JWT. A API atende os módulos de usuários, projetos, tarefas, equipes, riscos, custos, documentos e comunicações.

## Tecnologias

- Python 3.12
- Django 5.2
- Django REST Framework
- Simple JWT
- Djoser
- PostgreSQL (multi-tenant shared schema por `tenant_id`)
- drf-spectacular

## Estrutura

```text
backend/
├── planify/          # Configurações principais do projeto Django
├── customers/        # Tenants, domínios e memberships
├── core/             # Saúde da API, dashboard e métricas
├── users/            # Usuários, autenticação, perfis e permissões
├── projects/         # Projetos
├── tasks/            # Tarefas, atribuições e comentários
├── teams/            # Equipes, membros e permissões
├── risks/            # Riscos e histórico de riscos
├── costs/            # Custos, categorias, orçamentos e alertas
├── documents/        # Documentos, histórico e comentários
├── communications/   # Mensagens, notificações e configurações
├── tests/            # Testes automatizados da API
├── manage.py
├── requirements.txt
└── pytest.ini
```

## Instalação

Execute os comandos a partir da raiz do repositório:

```bash
cd backend

python -m venv venv
source venv/bin/activate

pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser
```

No Windows, ative o ambiente virtual com:

```bash
venv\Scripts\activate
```

## Execução

Para subir o servidor na porta padrão do Django:

```bash
python manage.py runserver
```

A API ficará disponível em:

```text
http://127.0.0.1:8000/api/
```

Também existe o script local `start_server.sh`, que sobe o backend em `0.0.0.0:8001`:

```bash
./start_server.sh
```

## Endpoints Úteis

| Recurso | URL |
| --- | --- |
| Raiz da API | `GET /api/` |
| Health check | `GET /api/health/` |
| Health check detalhado | `GET /api/health/detailed/` |
| Dashboard | `GET /api/dashboard/` |
| Swagger | `GET /docs/` |
| Swagger alternativo | `GET /swagger/` |
| Redoc | `GET /redoc/` |
| Schema OpenAPI | `GET /api/schema/` |
| Admin Django | `GET /admin/` |

## Autenticação

A autenticação principal usa JWT.

```http
POST /api/auth/token/
POST /api/auth/token/refresh/
```

Exemplo de login:

```bash
curl -X POST http://127.0.0.1:8000/api/auth/token/ \
  -H "Content-Type: application/json" \
  -d '{"username": "seu_usuario", "password": "sua_senha"}'
```

Use o token de acesso nas próximas requisições:

```http
Authorization: Bearer <access_token>
```

## Módulos da API

| Módulo | Prefixo |
| --- | --- |
| Autenticação | `/api/auth/` |
| Usuários | `/api/users/` |
| Projetos | `/api/projects/` |
| Tarefas | `/api/tasks/` |
| Equipes | `/api/teams/` |
| Riscos | `/api/risks/` |
| Custos | `/api/costs/` |
| Documentos | `/api/documents/` |
| Comunicações | `/api/communications/` |

## Desenvolvimento

Comandos comuns:

```bash
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser
python manage.py collectstatic
```

## PostgreSQL e Tenants (shared schema)

O backend usa PostgreSQL com **isolamento multi-tenant por `tenant_id`** num
**único schema** (sem `django-tenants` — removido na R1). Cada empresa é uma linha
`customers.Client`; os 26 models de negócio carregam `tenant_id`. O tenant de cada
request vem da `TenantMembership` ativa do usuário (sem subdomínio). Detalhes em
`../docs/multi-tenant-architecture.md` e `../docs/rearquitetura-shared-schema-plano.md`.

Variáveis principais:

```bash
POSTGRES_DB=planify
POSTGRES_USER=planify
POSTGRES_PASSWORD=planify
POSTGRES_HOST=127.0.0.1
POSTGRES_PORT=15432
```

Subir PostgreSQL local com Docker, a partir da raiz do repositório:

```bash
docker compose up -d postgres
```

Depois rode, em `backend/` (banco único — `migrate`, não `migrate_schemas`):

```bash
python manage.py migrate
```

Para manter uma execução legada temporária com SQLite, use:

```bash
USE_SQLITE=True python manage.py check
```

Esse modo existe apenas para inspeção local. A re-arquitetura multi-tenant deve ser
validada em PostgreSQL.

Criar um tenant local de desenvolvimento (uma linha `Client`):

```bash
python manage.py create_dev_tenant --name Demo
```

Provisionar empresa + owner de forma canônica (superuser):

```bash
python manage.py provision_tenant --name "ACME" --owner-email owner@acme.com
```

### RLS nativo do PostgreSQL (opcional em runtime)

A RLS nativa (`FORCE ROW LEVEL SECURITY` nas 26 tabelas) é a rede de segurança no
banco. Para ativá-la em runtime, crie a role sem bypass e rode a web como ela:

```bash
python manage.py setup_rls                 # cria/atualiza a role app_user
POSTGRES_USER=app_user POSTGRES_PASSWORD=<senha> python manage.py runserver
```

Sob a role dona do banco (`planify`, superuser) a RLS é inócua — migrations, seed e
testes seguem por ela; a camada de aplicação (`TenantManager` + RLS de app) já
isola. Acesse a API por `http://localhost:8000/` (o tenant vem da membership; o
superuser escopa com o header `X-Tenant-ID`).

Gerar novamente o schema OpenAPI:

```bash
python manage.py spectacular --file openapi.json
```

Popular dados de exemplo, quando necessário. O seed exige um `Client` existente:
os usuários/memberships são criados na identidade global e os dados de negócio são
gravados carimbando `tenant_id` do tenant alvo (`SEED_TENANT`, padrão `Demo`).

```bash
# usa o tenant padrão "Demo" (crie-o antes com create_dev_tenant)
python seed_data.py

# ou aponte para outro tenant existente (id ou nome)
SEED_TENANT="ACME" python seed_data.py
```

### Migrar uma base legada (single-tenant) para o shared schema

`migrate_legacy_data` faz o *onboarding* de um SQLite legado: a identidade global
(`users.User`, dedup por e-mail, hash de senha preservado) vai para `users`, e os
dados de negócio são copiados carimbando `tenant_id` do `Client` destino já
provisionado. É idempotente; use `--dry-run` para simular sem gravar.

```bash
# Apenas a identidade global (ex.: caso só haja usuários, sem dados de negócio)
python manage.py migrate_legacy_data --users-only

# Onboarding completo de uma base legada para o tenant "ACME" (provisione-o antes)
python manage.py migrate_legacy_data --legacy-db backups/db.sqlite3.baseline --tenant ACME

# Simulação (não grava nada; só relata contagens)
python manage.py migrate_legacy_data --tenant ACME --dry-run
```

O plano de rollback e a validação estão em
`../docs/backend-multitenant-audit.md` (R6/R8). O caminho de dados de negócio é
coberto por `scripts/e2e_migrate_legacy.py`.

## Testes

O projeto usa `pytest` com `pytest-django`.

```bash
pytest
```

Para executar apenas os testes do backend principal:

```bash
pytest tests
```

Para executar testes de um app específico:

```bash
pytest documents/tests
pytest projects/tests
pytest communications/tests
```

## Configurações de Desenvolvimento

As configurações atuais em `planify/settings.py` estão preparadas para ambiente local:

- `DEBUG=True`
- PostgreSQL via variáveis de ambiente
- CORS liberado para desenvolvimento
- E-mails enviados para o console
- Documentação Swagger/Redoc pública
- Arquivos de mídia servidos pelo Django durante o desenvolvimento

Antes de usar em produção, revise pelo menos:

- `SECRET_KEY`
- `DEBUG`
- `ALLOWED_HOSTS`
- `CORS_ALLOW_ALL_ORIGINS`
- Banco de dados
- Backend de e-mail
- Configurações de arquivos estáticos e mídia
