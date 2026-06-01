# Planify Backend

Backend da API Planify, desenvolvido com Django, Django REST Framework e autenticação JWT. A API atende os módulos de usuários, projetos, tarefas, equipes, riscos, custos, documentos e comunicações.

## Tecnologias

- Python 3.9+
- Django 5.2.1
- Django REST Framework 3.14
- Simple JWT
- Djoser
- drf-spectacular
- SQLite em desenvolvimento

## Estrutura

```text
backend/
├── planify/          # Configurações principais do projeto Django
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

Gerar novamente o schema OpenAPI:

```bash
python manage.py spectacular --file openapi.json
```

Popular dados de exemplo, quando necessário:

```bash
python seed_data.py
```

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
- Banco SQLite em `backend/db.sqlite3`
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
