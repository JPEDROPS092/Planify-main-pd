# API Test execution

## Preparação
Autenticar como admin no Swagger. Utilizando o botão Authorize.

## Template 
`METHOD /route/`: **CODE** - Resumo

## Projects
`GET /projects/`: **200** - Retornou os projetos cadastrados.

BODY: -

RESPONSE:

    {
    "count": 11,
    "next": "http://127.0.0.1:8000/api/projects/projetos/?page=2",
    "previous": null,
    "results": [
        {
        "id": 11,
        "titulo": "Planify",
        "descricao": "Projeto desenvolvimento de sistema de gerenciamento",
        "data_inicio": "2025-06-09",
        "data_fim": "2025-12-09",
        "status": "EM_ANDAMENTO",
        "status_display": "Em Andamento",
        "prioridade": "ALTA",
        "prioridade_display": "Alta",
        "criado_em": "2025-06-10T11:15:06.440284-03:00",
        "atualizado_em": "2025-06-10T11:15:06.440309-03:00",
        "arquivado": false,
        "membros_count": 1,
        "tasks_count": 0,
        "progresso": 0,
        "criador_username": "admin",
        "atrasado": false
        },
        . . .


`POST /projects/`: **200**: Retornou os projetos cadastrados.

BODY: -

RESPONSE:

``