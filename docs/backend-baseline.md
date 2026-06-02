# Backend Baseline - Codex Task 01

Branch analisada: `Dev-tenant`

Data local da execução: 2026-06-01

## Ambiente

- Diretório do backend: `backend/`
- Python do sistema: `Python 3.12.3`
- Python do virtualenv: `backend/venv/bin/python`, `Python 3.12.3`
- Banco atual: SQLite em `backend/db.sqlite3`
- Configuração ativa do Django: `planify.settings`
- Modelo de usuário customizado: `users.User`
- Frameworks principais: Django, Django REST Framework, Simple JWT, Djoser

## Comandos executados

```bash
./venv/bin/python manage.py check
```

Resultado:

```text
System check identified no issues (0 silenced).
```

```bash
./venv/bin/pytest
```

Resultado: falha na coleta dos testes, antes da execução da suite.

Falhas conhecidas:

- `tests/test_communications_api.py` importa `Project` de `projects.models`.
- `tests/test_costs_api.py` importa `Project` de `projects.models`.
- `tests/test_documents_api.py` importa `Project` de `projects.models`.
- `tests/test_projects_api.py` importa `Project` de `projects.models`.

O model existente em `projects.models` chama-se `Projeto`, não `Project`.

## Backup

Backup local criado:

```text
backend/backups/db.sqlite3.codex-task-01-baseline
```

Tamanho observado:

```text
604K
```

## Endpoints principais atuais

- `GET /api/`
- `api/auth/`
- `api/users/`
- `api/projects/`
- `api/tasks/`
- `api/teams/`
- `api/risks/`
- `api/costs/`
- `api/documents/`
- `api/communications/`
- `api/health/`
- `api/health/detailed/`
- `api/dashboard/`
- `api/projects/<id_projeto>/metrics/`
- `api/user/dashboard/`
- `api/schema/`
- `docs/`
- `swagger/`
- `redoc/`

## Observações para a refatoração

- A autenticação atual deve ser preservada na primeira etapa para reduzir risco.
- O projeto usa `Djoser` e rotas customizadas de `users` no mesmo prefixo `api/auth/`.
- O middleware customizado `users.middleware.PermissionMiddleware` deve ser revisado antes de ativar `django-tenants`.
- `ALLOWED_HOSTS` atualmente aceita apenas `localhost` e `127.0.0.1`; a resolução por subdomínio local exigirá ajuste.
- O banco principal ainda é SQLite; `django-tenants` exigirá PostgreSQL.
