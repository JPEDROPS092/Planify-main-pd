# API Test execution

## Resultados:

**Passou:** 22/30

---

## Preparação
Autenticar como admin no Swagger. Utilizando o botão Authorize.

---

## Template
`METHOD /api/route/`

#### REQ_BODY: 

    Nobody

#### RESPONSE: **CODE** - Resumo

    Response body

#### OBSERVAÇÕES:


---

## Listar projetos
`GET /api/projects/`: **200** - Retornou os projetos cadastrados.

#### REQ_BODY:

    Nobody

#### RESPONSE:

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

---

## Criar um projeto
`POST /api/projects/`: **201**: Criou um projeto teste.

#### REQ_BODY: 

    {
    "titulo": "Projeto teste",
    "descricao": "Projeto criado para teste apenas",
    "data_inicio": "2025-06-10",
    "data_fim": "2025-11-10",
    "status": "PLANEJADO",
    "prioridade": "BAIXA",
    "arquivado": true
    }

#### RESPONSE:

    {
    "id": 13,
    "titulo": "Projeto teste",
    "descricao": "Projeto criado para teste apenas",
    "data_inicio": "2025-06-10",
    "data_fim": "2025-11-10",
    "status": "PLANEJADO",
    "status_display": "Planejado",
    "prioridade": "BAIXA",
    "prioridade_display": "Baixa",
    "criado_por": 2,
    "criador_username": "admin",
    "criador_nome": "",
    "criado_em": "2025-06-10T11:37:50.196259-03:00",
    "atualizado_em": "2025-06-10T11:37:50.196278-03:00",
    "arquivado": true,
    "membros": [
        {
        "id": 3,
        "usuario_id": 2,
        "username": "admin",
        "full_name": "",
        "papel": "ADMIN",
        "papel_display": "ADMIN"
        }
    ],
    "sprints_count": 0,
    "tasks_count": 0,
    "progresso": 0,
    "dias_restantes": 153,
    "atrasado": false
    }

---

## Obter detalhes de um projeto
`GET /api/projects/13/`: **200** - Resumo

#### REQ_BODY: 

    Nobody

#### RESPONSE:

    {
    "id": 13,
    "titulo": "Projeto teste",
    "descricao": "Projeto criado para teste apenas",
    "data_inicio": "2025-06-10",
    "data_fim": "2025-11-10",
    "status": "PLANEJADO",
    "status_display": "Planejado",
    "prioridade": "BAIXA",
    "prioridade_display": "Baixa",
    "criado_por": 2,
    "criador_username": "admin",
    "criador_nome": "",
    "criado_em": "2025-06-10T11:37:50.196259-03:00",
    "atualizado_em": "2025-06-10T11:37:50.196278-03:00",
    "arquivado": true,
    "membros": [
        {
        "id": 3,
        "usuario_id": 2,
        "username": "admin",
        "full_name": "",
        "papel": "ADMIN",
        "papel_display": "ADMIN"
        }
    ],
    "sprints_count": 0,
    "tasks_count": 0,
    "progresso": 0,
    "dias_restantes": 153,
    "atrasado": false
    }

---

## Obter detalhes de um projeto
`PUT /api/projetos/13/`: **200** - O projeto foi atualizado

#### REQ_BODY: 

    {
    "titulo": "Projeto teste acaba de ser atualizado",
    "descricao": "Fizemos uma atualização nesse projeto",
    "data_inicio": "2025-06-10",
    "data_fim": "2025-11-30",
    "status": "EM_ANDAMENTO",
    "prioridade": "BAIXA",
    "arquivado": true
    }

#### RESPONSE:

    {
    "id": 13,
    "titulo": "Projeto teste acaba de ser atualizado",
    "descricao": "Fizemos uma atualização nesse projeto",
    "data_inicio": "2025-06-10",
    "data_fim": "2025-11-30",
    "status": "EM_ANDAMENTO",
    "status_display": "Em Andamento",
    "prioridade": "BAIXA",
    "prioridade_display": "Baixa",
    "criado_por": 2,
    "criador_username": "admin",
    "criador_nome": "",
    "criado_em": "2025-06-10T11:37:50.196259-03:00",
    "atualizado_em": "2025-06-10T11:41:21.965514-03:00",
    "arquivado": true,
    "membros": [
        {
        "id": 3,
        "usuario_id": 2,
        "username": "admin",
        "full_name": "",
        "papel": "ADMIN",
        "papel_display": "ADMIN"
        }
    ],
    "sprints_count": 0,
    "tasks_count": 0,
    "progresso": 0,
    "dias_restantes": 173,
    "atrasado": false
    }

---

## Atualizando projeto criado
`PATCH /api/projects/13/`: **200** - Atualizado apenas o atributo "prioridade" do projeto 13

#### REQ_BODY: 

    {
    "prioridade": "ALTA"
    }

#### RESPONSE:

    {
    "id": 13,
    "titulo": "Projeto teste acaba de ser atualizado",
    "descricao": "Fizemos uma atualização nesse projeto",
    "data_inicio": "2025-06-10",
    "data_fim": "2025-11-30",
    "status": "EM_ANDAMENTO",
    "status_display": "Em Andamento",
    "prioridade": "ALTA",
    "prioridade_display": "Alta",
    "criado_por": 2,
    "criador_username": "admin",
    "criador_nome": "",
    "criado_em": "2025-06-10T11:37:50.196259-03:00",
    "atualizado_em": "2025-06-10T11:43:39.462070-03:00",
    "arquivado": true,
    "membros": [
        {
        "id": 3,
        "usuario_id": 2,
        "username": "admin",
        "full_name": "",
        "papel": "ADMIN",
        "papel_display": "ADMIN"
        }
    ],
    "sprints_count": 0,
    "tasks_count": 0,
    "progresso": 0,
    "dias_restantes": 173,
    "atrasado": false
    }

---

## Excluir projeto criado
`DELETE /api/projects/13/`: **204** - Sem mensagem de resposta, mas obtive código de sucesso 

#### REQ_BODY: 

    Nobody

#### RESPONSE:

    No Response body

---

## Adicionar membro ao projeto Teste 1
`METHOD /api/projects/12/adicionar_membro/`: **500** - Usuário não adicionado. Erro na Key

#### REQ_BODY: 

    {
    "usuario": 2,
    "papel": "GERENTE"
    }

#### RESPONSE:

    KeyError at /api/projects/projetos/12/adicionar_membro/
    'projeto'

    ...

    Traceback (most recent call last):
    File "/home/luizf/source/Planify-main-pd/backend/venv/lib/python3.12/site-packages/django/core/handlers/exception.py", line 55, in inner
        #### RESPONSE = get_#### RESPONSE(request)
                ^^^^^^^^^^^^^^^^^^^^^
    File "/home/luizf/source/Planify-main-pd/backend/venv/lib/python3.12/site-packages/django/core/handlers/base.py", line 197, in _get_#### RESPONSE
        #### RESPONSE = wrapped_callback(request, *callback_args, **callback_kwargs)
                ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
    File "/home/luizf/source/Planify-main-pd/backend/venv/lib/python3.12/site-packages/django/views/decorators/csrf.py", line 65, in _view_wrapper
        return view_func(request, *args, **kwargs)
            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
    File "/home/luizf/source/Planify-main-pd/backend/venv/lib/python3.12/site-packages/rest_framework/viewsets.py", line 125, in view
        return self.dispatch(request, *args, **kwargs)
            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
    File "/home/luizf/source/Planify-main-pd/backend/venv/lib/python3.12/site-packages/rest_framework/views.py", line 509, in dispatch
        #### RESPONSE = self.handle_exception(exc)
                ^^^^^^^^^^^^^^^^^^^^^^^^^^
    File "/home/luizf/source/Planify-main-pd/backend/venv/lib/python3.12/site-packages/rest_framework/views.py", line 469, in handle_exception
        self.raise_uncaught_exception(exc)
        ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
    File "/home/luizf/source/Planify-main-pd/backend/venv/lib/python3.12/site-packages/rest_framework/views.py", line 480, in raise_uncaught_exception
        raise exc
        ^^^^^^^^^
    File "/home/luizf/source/Planify-main-pd/backend/venv/lib/python3.12/site-packages/rest_framework/views.py", line 506, in dispatch
        #### RESPONSE = handler(request, *args, **kwargs)
                ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
    File "/home/luizf/source/Planify-main-pd/backend/projects/views.py", line 186, in adicionar_membro
        if serializer.is_valid():
        ^^^^^^^^^^^^^^^^^^^^^
    File "/home/luizf/source/Planify-main-pd/backend/venv/lib/python3.12/site-packages/rest_framework/serializers.py", line 227, in is_valid
        self._validated_data = self.run_validation(self.initial_data)
                            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
    File "/home/luizf/source/Planify-main-pd/backend/venv/lib/python3.12/site-packages/rest_framework/serializers.py", line 428, in run_validation
        self.run_validators(value)
        ^^^^^^^^^^^^^^^^^^^^^^^^^^
    File "/home/luizf/source/Planify-main-pd/backend/venv/lib/python3.12/site-packages/rest_framework/serializers.py", line 461, in run_validators
        super().run_validators(to_validate)
        ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
    File "/home/luizf/source/Planify-main-pd/backend/venv/lib/python3.12/site-packages/rest_framework/fields.py", line 560, in run_validators
        validator(value, self)
        ^^^^^^^^^^^^^^^^^^^^^^
    File "/home/luizf/source/Planify-main-pd/backend/venv/lib/python3.12/site-packages/rest_framework/validators.py", line 148, in __call__
        self.enforce_required_fields(attrs, serializer)
        ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
    File "/home/luizf/source/Planify-main-pd/backend/venv/lib/python3.12/site-packages/rest_framework/validators.py", line 109, in enforce_required_fields
        if serializer.fields[field_name].source not in attrs
        ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
    File "/home/luizf/source/Planify-main-pd/backend/venv/lib/python3.12/site-packages/rest_framework/utils/serializer_helpers.py", line 172, in __getitem__
        return self.fields[key]
            ^^^^^^^^^^^^^^^^

    Exception Type: KeyError at /api/projects/projetos/12/adicionar_membro/
    Exception Value: 'projeto'
    Raised during: projects.views.ProjetoViewSet

    ...

---

## Arquiva ou desarquiva um projeto
`POST /api/projects/12/archive/`: **200** - O projeto foi arquivado
 
#### REQ_BODY: 

    {

    }

#### RESPONSE:

    {
    "arquivado": true
    }   

#### OBSERVAÇÕES:
Corpo da requisição é necessário?

---

## Lista os membros do projeto
`GET /api/projects/12/membros`: **200** - Foi exibido apenas o admin

#### REQ_BODY: 

    Nobody

#### RESPONSE:

    [   
        {
            "id": 2,
            "usuario_id": 2,
            "username": "admin",
            "full_name": "",
            "papel": "ADMIN",
            "papel_display": "ADMIN"
        }
    ]

#### OBSERVAÇÕES:
Esse projeto foi criado anteriormente pelo admin. O admin foi exibido por ser o criador do projeto?

---

## Remover membro do projeto
`DELETE /api/projects/projetos/12/remover_membro/?membro_id=2`: **400** - Impossível remover criador do projeto

#### REQ_BODY: 

    Nobody

#### RESPONSE:

    {
    "detail": "Não é possível remover o criador do projeto."
    }

#### OBSERVAÇÕES:
Infelizmente não há outros membros nesse projeto para testar. E a adição de membros falhou

---

## Listar meus projetos
`GET /api/projects/my_projects`: **CODE** - Resumo

#### REQ_BODY: 

    Nobody

#### RESPONSE:

    {
    "count": 2,
    "next": null,
    "previous": null,
    "results": [
        {
        "id": 12,
        "titulo": "string",
        "descricao": "string",
        "data_inicio": "2025-06-10",
        "data_fim": "2025-06-10",
        "status": "PLANEJADO",
        "status_display": "Planejado",
        "prioridade": "BAIXA",
        "prioridade_display": "Baixa",
        "criado_por": 2,
        "criador_username": "admin",
        "criador_nome": "",
        "criado_em": "2025-06-10T11:21:08.240436-03:00",
        "atualizado_em": "2025-06-10T12:57:29.790752-03:00",
        "arquivado": true,
        "membros": [
            {
            "id": 2,
            "usuario_id": 2,
            "username": "admin",
            "full_name": "",
            "papel": "ADMIN",
            "papel_display": "ADMIN"
            }
        ],
        "sprints_count": 0,
        "tasks_count": 0,
        "progresso": 0,
        "dias_restantes": 0,
        "atrasado": false
        },
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
        "criado_por": 2,
        "criador_username": "admin",
        "criador_nome": "",
        "criado_em": "2025-06-10T11:15:06.440284-03:00",
        "atualizado_em": "2025-06-10T11:15:06.440309-03:00",
        "arquivado": false,
        "membros": [
            {
            "id": 1,
            "usuario_id": 2,
            "username": "admin",
            "full_name": "",
            "papel": "ADMIN",
            "papel_display": "ADMIN"
            }
        ],
        "sprints_count": 0,
        "tasks_count": 0,
        "progresso": 0,
        "dias_restantes": 182,
        "atrasado": false
        }
    ]
    }

---

## Criar nova sprint
`POST /api/projects/sprints/`

#### REQ_BODY: 

    {
    "projeto": 12,
    "nome": "Sprint 4",
    "descricao": "Terminar backend. Apresentar alteração no frontent",
    "data_inicio": "2025-06-02",
    "data_fim": "2025-06-16",
    "status": "EM_ANDAMENTO"
    }

#### RESPONSE: **201** - Sprint foi criada com sucesso

    {
    "id": 31,
    "projeto": 12,
    "projeto_nome": "string",
    "nome": "Sprint 4",
    "descricao": "Terminar backend. Apresentar alteração no frontent",
    "data_inicio": "2025-06-02",
    "data_fim": "2025-06-16",
    "status": "EM_ANDAMENTO",
    "status_display": "Em Andamento",
    "criado_por": 2,
    "criado_em": "2025-06-10T13:26:26.707655-03:00",
    "tasks_count": 0,
    "completed_tasks_count": 0,
    "progresso": 0
    }

#### OBSERVAÇÕES:

---

## Listar sprints
`GET /api/projects/sprints/`

#### REQ_BODY: 

    Nobody

#### RESPONSE: **200** - Strings listadas com sucesso (após alteração)

    {
    "count": 57,
    "next": "http://127.0.0.1:8000/api/projects/sprints/?page=2",
    "previous": null,
    "results": [
        {
        "id": 6,
        "projeto": 2,
        "projeto_nome": "Plataforma de Machine Learning",
        "nome": "Sprint 3",
        "descricao": "Sprint 3 do projeto Plataforma de Machine Learning",
        "data_inicio": "2025-07-26",
        "data_fim": "2025-08-25",
        "status": "EM_ANDAMENTO",
        "status_display": "Em Andamento",
        "criado_por": 2,
        "criado_em": "2025-06-05T15:22:09.481432-03:00",
        "tasks_count": 3,
        "completed_tasks_count": 1,
        "progresso": 33
        },
        {
        "id": 6,
        "projeto": 2,
        "projeto_nome": "Plataforma de Machine Learning",
        "nome": "Sprint 3",
        "descricao": "Sprint 3 do projeto Plataforma de Machine Learning",
        "data_inicio": "2025-07-26",
        "data_fim": "2025-08-25",
        "status": "EM_ANDAMENTO",
        "status_display": "Em Andamento",
        "criado_por": 2,
        "criado_em": "2025-06-05T15:22:09.481432-03:00",
        "tasks_count": 3,
        "completed_tasks_count": 1,
        "progresso": 33
        },
        {
        "id": 6,
        "projeto": 2,
        "projeto_nome": "Plataforma de Machine Learning",
        "nome": "Sprint 3",
        "descricao": "Sprint 3 do projeto Plataforma de Machine Learning",
        "data_inicio": "2025-07-26",
        "data_fim": "2025-08-25",
        "status": "EM_ANDAMENTO",
        "status_display": "Em Andamento",
        "criado_por": 2,
        "criado_em": "2025-06-05T15:22:09.481432-03:00",
        "tasks_count": 3,
        "completed_tasks_count": 1,
        "progresso": 33
        },
        {
        "id": 21,
        "projeto": 7,
        "projeto_nome": "Aplicação de Análise de Dados",
        "nome": "Sprint 3",
        "descricao": "Sprint 3 do projeto Aplicação de Análise de Dados",
        "data_inicio": "2025-07-16",
        "data_fim": "2025-08-15",
        "status": "CONCLUIDO",
        "status_display": "Concluído",
        "criado_por": 2,
        "criado_em": "2025-06-05T15:22:09.587756-03:00",
        "tasks_count": 2,
        "completed_tasks_count": 1,
        "progresso": 50
        },
        {
        "id": 21,
        "projeto": 7,
        "projeto_nome": "Aplicação de Análise de Dados",
        "nome": "Sprint 3",
        "descricao": "Sprint 3 do projeto Aplicação de Análise de Dados",
        "data_inicio": "2025-07-16",
        "data_fim": "2025-08-15",
        "status": "CONCLUIDO",
        "status_display": "Concluído",
        "criado_por": 2,
        "criado_em": "2025-06-05T15:22:09.587756-03:00",
        "tasks_count": 2,
        "completed_tasks_count": 1,
        "progresso": 50
        },
        {
        "id": 12,
        "projeto": 4,
        "projeto_nome": "Sistema de Automação Industrial",
        "nome": "Sprint 3",
        "descricao": "Sprint 3 do projeto Sistema de Automação Industrial",
        "data_inicio": "2025-07-11",
        "data_fim": "2025-08-10",
        "status": "EM_ANDAMENTO",
        "status_display": "Em Andamento",
        "criado_por": 2,
        "criado_em": "2025-06-05T15:22:09.524359-03:00",
        "tasks_count": 3,
        "completed_tasks_count": 1,
        "progresso": 33
        },
        {
        "id": 12,
        "projeto": 4,
        "projeto_nome": "Sistema de Automação Industrial",
        "nome": "Sprint 3",
        "descricao": "Sprint 3 do projeto Sistema de Automação Industrial",
        "data_inicio": "2025-07-11",
        "data_fim": "2025-08-10",
        "status": "EM_ANDAMENTO",
        "status_display": "Em Andamento",
        "criado_por": 2,
        "criado_em": "2025-06-05T15:22:09.524359-03:00",
        "tasks_count": 3,
        "completed_tasks_count": 1,
        "progresso": 33
        },
        {
        "id": 12,
        "projeto": 4,
        "projeto_nome": "Sistema de Automação Industrial",
        "nome": "Sprint 3",
        "descricao": "Sprint 3 do projeto Sistema de Automação Industrial",
        "data_inicio": "2025-07-11",
        "data_fim": "2025-08-10",
        "status": "EM_ANDAMENTO",
        "status_display": "Em Andamento",
        "criado_por": 2,
        "criado_em": "2025-06-05T15:22:09.524359-03:00",
        "tasks_count": 3,
        "completed_tasks_count": 1,
        "progresso": 33
        },
        {
        "id": 30,
        "projeto": 10,
        "projeto_nome": "Aplicação Móvel Corporativa",
        "nome": "Sprint 3",
        "descricao": "Sprint 3 do projeto Aplicação Móvel Corporativa",
        "data_inicio": "2025-07-03",
        "data_fim": "2025-08-02",
        "status": "EM_ANDAMENTO",
        "status_display": "Em Andamento",
        "criado_por": 2,
        "criado_em": "2025-06-05T15:22:09.654191-03:00",
        "tasks_count": 2,
        "completed_tasks_count": 1,
        "progresso": 50
        },
        {
        "id": 30,
        "projeto": 10,
        "projeto_nome": "Aplicação Móvel Corporativa",
        "nome": "Sprint 3",
        "descricao": "Sprint 3 do projeto Aplicação Móvel Corporativa",
        "data_inicio": "2025-07-03",
        "data_fim": "2025-08-02",
        "status": "EM_ANDAMENTO",
        "status_display": "Em Andamento",
        "criado_por": 2,
        "criado_em": "2025-06-05T15:22:09.654191-03:00",
        "tasks_count": 2,
        "completed_tasks_count": 1,
        "progresso": 50
        }
    ]
    }


#### OBSERVAÇÕES:
Tive que fazer uma alteração em `@/backend/projects/views.py` para funcionar: *Importar FloatField*. 

---

## Listar sprints (Teste 2)
`GET /api/projects/sprints/?ativa=true`

#### REQ_BODY: 

    Nobody

#### RESPONSE: **200** - Strings listadas com sucesso (após alteração)

    {
    "count": 15,
    "next": "http://127.0.0.1:8000/api/projects/sprints/?ativa=true&page=2",
    "previous": null,
    "results": [
        {
        "id": 15,
        "projeto": 5,
        "projeto_nome": "Blockchain para Rastreabilidade",
        "nome": "Sprint 3",
        "descricao": "Sprint 3 do projeto Blockchain para Rastreabilidade",
        "data_inicio": "2025-06-08",
        "data_fim": "2025-07-08",
        "status": "EM_ANDAMENTO",
        "status_display": "Em Andamento",
        "criado_por": 2,
        "criado_em": "2025-06-05T15:22:09.545157-03:00",
        "tasks_count": 3,
        "completed_tasks_count": 0,
        "progresso": 0
        },
        {
        "id": 15,
        "projeto": 5,
        "projeto_nome": "Blockchain para Rastreabilidade",
        "nome": "Sprint 3",
        "descricao": "Sprint 3 do projeto Blockchain para Rastreabilidade",
        "data_inicio": "2025-06-08",
        "data_fim": "2025-07-08",
        "status": "EM_ANDAMENTO",
        "status_display": "Em Andamento",
        "criado_por": 2,
        "criado_em": "2025-06-05T15:22:09.545157-03:00",
        "tasks_count": 3,
        "completed_tasks_count": 0,
        "progresso": 0
        },
        {
        "id": 15,
        "projeto": 5,
        "projeto_nome": "Blockchain para Rastreabilidade",
        "nome": "Sprint 3",
        "descricao": "Sprint 3 do projeto Blockchain para Rastreabilidade",
        "data_inicio": "2025-06-08",
        "data_fim": "2025-07-08",
        "status": "EM_ANDAMENTO",
        "status_display": "Em Andamento",
        "criado_por": 2,
        "criado_em": "2025-06-05T15:22:09.545157-03:00",
        "tasks_count": 3,
        "completed_tasks_count": 0,
        "progresso": 0
        },
        {
        "id": 3,
        "projeto": 1,
        "projeto_nome": "Sistema de Monitoramento IoT",
        "nome": "Sprint 3",
        "descricao": "Sprint 3 do projeto Sistema de Monitoramento IoT",
        "data_inicio": "2025-06-04",
        "data_fim": "2025-07-04",
        "status": "PLANEJADO",
        "status_display": "Planejado",
        "criado_por": 2,
        "criado_em": "2025-06-05T15:22:09.460784-03:00",
        "tasks_count": 1,
        "completed_tasks_count": 0,
        "progresso": 0
        },
        {
        "id": 29,
        "projeto": 10,
        "projeto_nome": "Aplicação Móvel Corporativa",
        "nome": "Sprint 2",
        "descricao": "Sprint 2 do projeto Aplicação Móvel Corporativa",
        "data_inicio": "2025-06-03",
        "data_fim": "2025-07-03",
        "status": "EM_ANDAMENTO",
        "status_display": "Em Andamento",
        "criado_por": 2,
        "criado_em": "2025-06-05T15:22:09.650016-03:00",
        "tasks_count": 1,
        "completed_tasks_count": 1,
        "progresso": 100
        },
        {
        "id": 31,
        "projeto": 12,
        "projeto_nome": "string",
        "nome": "Sprint 4",
        "descricao": "Terminar backend. Apresentar alteração no frontent",
        "data_inicio": "2025-06-02",
        "data_fim": "2025-06-16",
        "status": "EM_ANDAMENTO",
        "status_display": "Em Andamento",
        "criado_por": 2,
        "criado_em": "2025-06-10T13:26:26.707655-03:00",
        "tasks_count": 0,
        "completed_tasks_count": 0,
        "progresso": 0
        },
        {
        "id": 26,
        "projeto": 9,
        "projeto_nome": "Plataforma de E-commerce",
        "nome": "Sprint 2",
        "descricao": "Sprint 2 do projeto Plataforma de E-commerce",
        "data_inicio": "2025-05-31",
        "data_fim": "2025-06-30",
        "status": "CONCLUIDO",
        "status_display": "Concluído",
        "criado_por": 2,
        "criado_em": "2025-06-05T15:22:09.628853-03:00",
        "tasks_count": 2,
        "completed_tasks_count": 0,
        "progresso": 0
        },
        {
        "id": 26,
        "projeto": 9,
        "projeto_nome": "Plataforma de E-commerce",
        "nome": "Sprint 2",
        "descricao": "Sprint 2 do projeto Plataforma de E-commerce",
        "data_inicio": "2025-05-31",
        "data_fim": "2025-06-30",
        "status": "CONCLUIDO",
        "status_display": "Concluído",
        "criado_por": 2,
        "criado_em": "2025-06-05T15:22:09.628853-03:00",
        "tasks_count": 2,
        "completed_tasks_count": 0,
        "progresso": 0
        },
        {
        "id": 24,
        "projeto": 8,
        "projeto_nome": "Sistema de Gestão de Recursos",
        "nome": "Sprint 3",
        "descricao": "Sprint 3 do projeto Sistema de Gestão de Recursos",
        "data_inicio": "2025-05-30",
        "data_fim": "2025-06-29",
        "status": "PLANEJADO",
        "status_display": "Planejado",
        "criado_por": 2,
        "criado_em": "2025-06-05T15:22:09.611808-03:00",
        "tasks_count": 1,
        "completed_tasks_count": 0,
        "progresso": 0
        },
        {
        "id": 4,
        "projeto": 2,
        "projeto_nome": "Plataforma de Machine Learning",
        "nome": "Sprint 1",
        "descricao": "Sprint 1 do projeto Plataforma de Machine Learning",
        "data_inicio": "2025-05-27",
        "data_fim": "2025-06-26",
        "status": "CONCLUIDO",
        "status_display": "Concluído",
        "criado_por": 2,
        "criado_em": "2025-06-05T15:22:09.473442-03:00",
        "tasks_count": 1,
        "completed_tasks_count": 1,
        "progresso": 100
        }
    ]
    }


#### OBSERVAÇÕES:
Aqui apareceu a sprint que eu criei

---

## Obter detalhes da sprint (teste 1)
`GET /api/projects/sprints/12/`

#### REQ_BODY: 

    Nobody

#### RESPONSE: **500** - Erro: Mais de uma sprint retornada

    MultipleObjectsReturned at /api/projects/sprints/12/
    get() returned more than one Sprint -- it returned 3!

#### OBSERVAÇÕES:
A listagem mostra do teste anterior mostra que algumas Sprints estão repetidas

---

## Obter detalhes da sprint (Teste 2)
`GET /api/projects/sprints/31/`

#### REQ_BODY: 

    Nobody

#### RESPONSE: **200** - Sprint retornada

    {
    "id": 31,
    "projeto": 12,
    "projeto_nome": "string",
    "nome": "Sprint 4",
    "descricao": "Terminar backend. Apresentar alteração no frontent",
    "data_inicio": "2025-06-02",
    "data_fim": "2025-06-16",
    "status": "EM_ANDAMENTO",
    "status_display": "Em Andamento",
    "criado_por": 2,
    "criado_em": "2025-06-10T13:26:26.707655-03:00",
    "tasks_count": 0,
    "completed_tasks_count": 0,
    "progresso": 0
    }

#### OBSERVAÇÕES:
A listagem mostra do teste anterior mostra que algumas Sprints estão repetidas

---

## Atualizar sprints
`PUT /api/projects/sprints/31/`

#### REQ_BODY: 

    {
    "projeto": 12,
    "nome": "Sprint 4 atualizada",
    "descricao": "atualizaçao",
    "data_inicio": "2025-06-10",
    "data_fim": "2025-06-20",
    "status": "PLANEJADO"
    }

#### RESPONSE: **200** - Sprint atualizada

    {
    "id": 31,
    "projeto": 12,
    "projeto_nome": "string",
    "nome": "Sprint 4 atualizada",
    "descricao": "atualizaçao",
    "data_inicio": "2025-06-10",
    "data_fim": "2025-06-20",
    "status": "PLANEJADO",
    "status_display": "Planejado",
    "criado_por": 2,
    "criado_em": "2025-06-10T13:26:26.707655-03:00",
    "tasks_count": 0,
    "completed_tasks_count": 0,
    "progresso": 0
    }

#### OBSERVAÇÕES:

---

## Atualizar sprint parcialmente
`PATCH /api/projects/sprints/31/`

#### REQ_BODY: 

    {
    "status": "CANCELADO"
    }

#### RESPONSE: **CODE** - Resumo

    {
    "id": 31,
    "projeto": 12,
    "projeto_nome": "string",
    "nome": "Sprint 4 atualizada",
    "descricao": "atualizaçao",
    "data_inicio": "2025-06-10",
    "data_fim": "2025-06-20",
    "status": "CANCELADO",
    "status_display": "Cancelado",
    "criado_por": 2,
    "criado_em": "2025-06-10T13:26:26.707655-03:00",
    "tasks_count": 0,
    "completed_tasks_count": 0,
    "progresso": 0
    }

#### OBSERVAÇÕES:

---

## Excluir sprint
`DELETE /api/projects/sprints/{id}/`

#### REQ_BODY: 

    Nobody

#### RESPONSE: **204** - Sem mensagem e resposta, mas código positivo

    No Response body

#### OBSERVAÇÕES:

---

## Resumo da sprint
`GET /api/projects/sprints/32/resumo/`

#### REQ_BODY: 

    Nobody

#### RESPONSE: **500** - Erro de atributo

    AttributeError at /api/projects/sprints/32/resumo/
    type object 'Tarefa' has no attribute 'PRIORIDADE_CHOICES'

#### OBSERVAÇÕES:
Foi criada uma nova sprint para esse teste

---

## Listar tarefas da sprint
`GET /api/projects/sprints/32/tarefas/`

#### REQ_BODY: 

    Nobody

#### RESPONSE: **500** - Erro de campo

    FieldError at /api/projects/sprints/32/tarefas/
    Invalid field name(s) given in select_related: 'responsavel'. Choices are: projeto, sprint, criado_por, atualizado_por, orcamento

#### OBSERVAÇÕES:

---

## Listar histórico de status

`GET /api/projects/historico-status-projeto/`

#### REQ_BODY: 

    Nobody

#### RESPONSE: **200** - A lista de alterações de status está vazia

    {
    "count": 0,
    "next": null,
    "previous": null,
    "results": []
    }

#### OBSERVAÇÕES:

**Realizado antes deste teste:**
`PATCH /api/projects/12/` 

BODY: 

    {
    "status": "CANCELADO"
    }

RESP: **200**

---

## Obter detalhe de alteração de status
`GET /api/projects/historico-status-projeto/12/`

#### REQ_BODY: 

    Nobody

#### RESPONSE: **404** - Não encontrado

    {
    "detail": "Não encontrado."
    }

#### OBSERVAÇÕES:
A lista geral de históricos de status está vazia

---

## Resumo de alterações por projeto
`GET /api/projects/historico-status-projeto/resumo_por_projeto/`

#### REQ_BODY: 

    Nobody

#### RESPONSE: **200** - Nada retornado

    []

#### OBSERVAÇÕES:

---

## Visualizar Dashboard do projeto
`GET /api/projects/12/dashboard/?projeto_id=12`

#### REQ_BODY: 

    Nobody

#### RESPONSE: **200** - Informações retornadas

    {
    "projeto": {
        "id": 12,
        "titulo": "string",
        "descricao": "string",
        "data_inicio": "2025-06-10",
        "data_fim": "2025-06-10",
        "status": "CANCELADO",
        "status_display": "Cancelado",
        "prioridade": "BAIXA",
        "prioridade_display": "Baixa",
        "criado_por": 2,
        "criador_username": "admin",
        "criador_nome": "",
        "criado_em": "2025-06-10T11:21:08.240436-03:00",
        "atualizado_em": "2025-06-10T14:18:04.626968-03:00",
        "arquivado": true,
        "membros": [
        {
            "id": 2,
            "usuario_id": 2,
            "username": "admin",
            "full_name": "",
            "papel": "ADMIN",
            "papel_display": "ADMIN"
        }
        ],
        "sprints_count": 1,
        "tasks_count": 0,
        "progresso": 0,
        "dias_restantes": 0,
        "atrasado": true
    },
    "sprints": [
        {
        "id": 32,
        "projeto": 12,
        "projeto_nome": "string",
        "nome": "Sprint 4 recriada",
        "descricao": "Terminar backend. Apresentar alteração no frontent",
        "data_inicio": "2025-06-02",
        "data_fim": "2025-06-16",
        "status": "EM_ANDAMENTO",
        "status_display": "Em Andamento",
        "criado_por": 2,
        "criado_em": "2025-06-10T14:13:32.417059-03:00",
        "tasks_count": 0,
        "completed_tasks_count": 0,
        "progresso": 0
        }
    ],
    "kanban": {
        "A_FAZER": [],
        "EM_ANDAMENTO": [],
        "FEITO": []
    },
    "gantt": [],
    "estatisticas": {
        "total_tarefas": 0,
        "tarefas_concluidas": 0,
        "tarefas_em_andamento": 0,
        "tarefas_a_fazer": 0,
        "tarefas_atrasadas": 0,
        "progresso": 0
    },
    "proximos_prazos": [],
    "membros": [
        {
        "id": 2,
        "username": "admin",
        "nome_completo": "",
        "papel": "ADMIN",
        "tarefas_total": 0,
        "tarefas_concluidas": 0
        }
    ]
    }

#### OBSERVAÇÕES:
Retirar necessidade do parâmetro na query

---

## Exportar dados do projeto
`GET /api/projects/12/exportar/?format=json&include_costs=false&include_project=true&include_risks=false&include_tasks=true&include_team=false`

#### REQ_BODY: 

    Nobody

#### RESPONSE: **500** - Erro ao pedir informação em JSON

    AttributeError at /api/projects/12/exportar/
    'Projeto' object has no attribute 'gerente'

#### OBSERVAÇÕES:
Ao pedir para exportar o mesmo projeto em CSV, ocorreu erro 404.

---

## Visualização Gantt do projeto
`GET /api/projects/12/gantt/?projeto_id=12`

#### REQ_BODY: 

    Nobody

#### RESPONSE: **200** - Retornou informações das sprints

    {
    "projeto": {
        "id": "projeto_12",
        "titulo": "Projeto: string",
        "inicio": "2025-06-10",
        "fim": "2025-06-10",
        "tipo": "projeto",
        "progresso": 0,
        "status": "CANCELADO"
    },
    "sprints": [
        {
        "id": "sprint_32",
        "titulo": "Sprint: Sprint 4 recriada",
        "inicio": "2025-06-02",
        "fim": "2025-06-16",
        "tipo": "sprint",
        "progresso": 50,
        "status": "EM_ANDAMENTO"
        }
    ],
    "tarefas": []
    }

#### OBSERVAÇÕES:

---

## Criar tarefa no projeto
`POST /api/projects/12/tarefas/criar/?projeto_id=12`

#### REQ_BODY: 

    {
    "titulo": "tarefa 1",
    "descricao": "tarefa criada para teste",
    "data_inicio": "2025-06-11",
    "data_termino": "2025-07-11",
    "prioridade": "ALTA",
    "status": "A_FAZER",
    "responsaveis": [
        0
    ]
    }

#### RESPONSE: **201** - Tarefa criada com sucesso

    {
    "id": 51,
    "titulo": "tarefa 1",
    "descricao": "tarefa criada para teste",
    "projeto": 12,
    "sprint": null,
    "data_inicio": "2025-06-11",
    "data_termino": "2025-07-11",
    "prioridade": "ALTA",
    "status": "A_FAZER",
    "criado_por": {
        "username": "admin",
        "email": "admin@planify.com",
        "full_name": "",
        "role": "TEAM_MEMBER",
        "profile": null,
        "id": 2,
        "is_active": true,
        "date_joined": "2025-06-05T15:22:06.191229-03:00",
        "access_profiles": []
    },
    "criado_em": "2025-06-11T12:44:17.348890-03:00",
    "atualizado_em": "2025-06-11T12:44:17.348908-03:00",
    "atribuicoes": [
        {
        "id": 51,
        "tarefa": 51,
        "usuario": 2,
        "usuario_nome": "",
        "atribuido_em": "2025-06-11T12:44:17.352982-03:00",
        "atribuido_por": 2,
        "atribuido_por_nome": ""
        }
    ],
    "responsaveis": [
        {
        "usuario__id": 2,
        "usuario__username": "admin",
        "usuario__full_name": ""
        }
    ]
    }

#### OBSERVAÇÕES:
O corpo de requisição padrão está errado: `data_termino` estava como `data_fim` e prioridade estava com valor "PENDENTE", o qual não é aceito.

---

## Criar múltiplas tarefas no projeto
`POST /api/projects/12/tarefas/criar-multiplas/?projeto_id=12`

#### REQ_BODY: 

    {
    "tarefas": [
        {
        "titulo": "primeira tarefa",
        "descricao": "Primeira tarefa do lote",
        "data_inicio": "2025-07-11",
        "data_termino": "2025-06-11",
        "prioridade": "BAIXA",
        "status": "A_FAZER",
        "responsaveis": [
            0
        ]
        },
        {
        "titulo": "segunda tarefa",
        "descricao": "Segunda tarefa do lote",
        "data_inicio": "2025-07-11",
        "data_termino": "2025-08-11",
        "prioridade": "BAIXA",
        "status": "A_FAZER",
        "responsaveis": [
            0
        ]
        }
    ]
    }

#### RESPONSE: **201** - Tarefas criadas com sucesso

    {
    "tarefas_criadas": [
        {
        "id": 54,
        "titulo": "primeira tarefa",
        "descricao": "Primeira tarefa do lote",
        "projeto": 12,
        "sprint": null,
        "data_inicio": "2025-07-11",
        "data_termino": "2025-06-11",
        "prioridade": "BAIXA",
        "status": "A_FAZER",
        "criado_por": {
            "username": "admin",
            "email": "admin@planify.com",
            "full_name": "",
            "role": "TEAM_MEMBER",
            "profile": null,
            "id": 2,
            "is_active": true,
            "date_joined": "2025-06-05T15:22:06.191229-03:00",
            "access_profiles": []
        },
        "criado_em": "2025-06-11T12:48:26.619639-03:00",
        "atualizado_em": "2025-06-11T12:48:26.619656-03:00",
        "atribuicoes": [
            {
            "id": 54,
            "tarefa": 54,
            "usuario": 2,
            "usuario_nome": "",
            "atribuido_em": "2025-06-11T12:48:26.620498-03:00",
            "atribuido_por": 2,
            "atribuido_por_nome": ""
            }
        ],
        "responsaveis": [
            {
            "usuario__id": 2,
            "usuario__username": "admin",
            "usuario__full_name": ""
            }
        ]
        },
        {
        "id": 55,
        "titulo": "segunda tarefa",
        "descricao": "Segunda tarefa do lote",
        "projeto": 12,
        "sprint": null,
        "data_inicio": "2025-07-11",
        "data_termino": "2025-08-11",
        "prioridade": "BAIXA",
        "status": "A_FAZER",
        "criado_por": {
            "username": "admin",
            "email": "admin@planify.com",
            "full_name": "",
            "role": "TEAM_MEMBER",
            "profile": null,
            "id": 2,
            "is_active": true,
            "date_joined": "2025-06-05T15:22:06.191229-03:00",
            "access_profiles": []
        },
        "criado_em": "2025-06-11T12:48:26.622748-03:00",
        "atualizado_em": "2025-06-11T12:48:26.622765-03:00",
        "atribuicoes": [
            {
            "id": 55,
            "tarefa": 55,
            "usuario": 2,
            "usuario_nome": "",
            "atribuido_em": "2025-06-11T12:48:26.623418-03:00",
            "atribuido_por": 2,
            "atribuido_por_nome": ""
            }
        ],
        "responsaveis": [
            {
            "usuario__id": 2,
            "usuario__username": "admin",
            "usuario__full_name": ""
            }
        ]
        }
    ],
    "total_criadas": 2,
    "erros": []
    }

#### OBSERVAÇÕES:

---

## Visualização Kanban do projeto
`GET /api/projects/12/kanban/?projeto_id=12`

#### REQ_BODY: 

    Nobody

#### RESPONSE: **200** - Retornou as tarefas criadas

    {
    "A_FAZER": [
        {
        "id": 51,
        "titulo": "tarefa 1",
        "descricao": "tarefa criada para teste",
        "projeto": 12,
        "sprint": null,
        "data_inicio": "2025-06-11",
        "data_termino": "2025-07-11",
        "prioridade": "ALTA",
        "status": "A_FAZER",
        "criado_por": {
            "username": "admin",
            "email": "admin@planify.com",
            "full_name": "",
            "role": "TEAM_MEMBER",
            "profile": null,
            "id": 2,
            "is_active": true,
            "date_joined": "2025-06-05T15:22:06.191229-03:00",
            "access_profiles": []
        },
        "criado_em": "2025-06-11T12:44:17.348890-03:00",
        "atualizado_em": "2025-06-11T12:44:17.348908-03:00",
        "atribuicoes": [
            {
            "id": 51,
            "tarefa": 51,
            "usuario": 2,
            "usuario_nome": "",
            "atribuido_em": "2025-06-11T12:44:17.352982-03:00",
            "atribuido_por": 2,
            "atribuido_por_nome": ""
            }
        ],
        "responsaveis": [
            {
            "usuario__id": 2,
            "usuario__username": "admin",
            "usuario__full_name": ""
            }
        ]
        },
        {
        "id": 52,
        "titulo": "multitarefa1",
        "descricao": "Primeira tarefa do lote",
        "projeto": 12,
        "sprint": null,
        "data_inicio": "2025-07-11",
        "data_termino": "2025-06-11",
        "prioridade": "BAIXA",
        "status": "A_FAZER",
        "criado_por": {
            "username": "admin",
            "email": "admin@planify.com",
            "full_name": "",
            "role": "TEAM_MEMBER",
            "profile": null,
            "id": 2,
            "is_active": true,
            "date_joined": "2025-06-05T15:22:06.191229-03:00",
            "access_profiles": []
        },
        "criado_em": "2025-06-11T12:47:37.669648-03:00",
        "atualizado_em": "2025-06-11T12:47:37.669665-03:00",
        "atribuicoes": [
            {
            "id": 52,
            "tarefa": 52,
            "usuario": 2,
            "usuario_nome": "",
            "atribuido_em": "2025-06-11T12:47:37.670524-03:00",
            "atribuido_por": 2,
            "atribuido_por_nome": ""
            }
        ],
        "responsaveis": [
            {
            "usuario__id": 2,
            "usuario__username": "admin",
            "usuario__full_name": ""
            }
        ]
        },
        {
        "id": 53,
        "titulo": "multitarefa1",
        "descricao": "Primeira tarefa do lote",
        "projeto": 12,
        "sprint": null,
        "data_inicio": "2025-07-11",
        "data_termino": "2025-06-11",
        "prioridade": "BAIXA",
        "status": "A_FAZER",
        "criado_por": {
            "username": "admin",
            "email": "admin@planify.com",
            "full_name": "",
            "role": "TEAM_MEMBER",
            "profile": null,
            "id": 2,
            "is_active": true,
            "date_joined": "2025-06-05T15:22:06.191229-03:00",
            "access_profiles": []
        },
        "criado_em": "2025-06-11T12:48:01.311652-03:00",
        "atualizado_em": "2025-06-11T12:48:01.311669-03:00",
        "atribuicoes": [
            {
            "id": 53,
            "tarefa": 53,
            "usuario": 2,
            "usuario_nome": "",
            "atribuido_em": "2025-06-11T12:48:01.312882-03:00",
            "atribuido_por": 2,
            "atribuido_por_nome": ""
            }
        ],
        "responsaveis": [
            {
            "usuario__id": 2,
            "usuario__username": "admin",
            "usuario__full_name": ""
            }
        ]
        },
        {
        "id": 54,
        "titulo": "primeira tarefa",
        "descricao": "Primeira tarefa do lote",
        "projeto": 12,
        "sprint": null,
        "data_inicio": "2025-07-11",
        "data_termino": "2025-06-11",
        "prioridade": "BAIXA",
        "status": "A_FAZER",
        "criado_por": {
            "username": "admin",
            "email": "admin@planify.com",
            "full_name": "",
            "role": "TEAM_MEMBER",
            "profile": null,
            "id": 2,
            "is_active": true,
            "date_joined": "2025-06-05T15:22:06.191229-03:00",
            "access_profiles": []
        },
        "criado_em": "2025-06-11T12:48:26.619639-03:00",
        "atualizado_em": "2025-06-11T12:48:26.619656-03:00",
        "atribuicoes": [
            {
            "id": 54,
            "tarefa": 54,
            "usuario": 2,
            "usuario_nome": "",
            "atribuido_em": "2025-06-11T12:48:26.620498-03:00",
            "atribuido_por": 2,
            "atribuido_por_nome": ""
            }
        ],
        "responsaveis": [
            {
            "usuario__id": 2,
            "usuario__username": "admin",
            "usuario__full_name": ""
            }
        ]
        },
        {
        "id": 55,
        "titulo": "segunda tarefa",
        "descricao": "Segunda tarefa do lote",
        "projeto": 12,
        "sprint": null,
        "data_inicio": "2025-07-11",
        "data_termino": "2025-08-11",
        "prioridade": "BAIXA",
        "status": "A_FAZER",
        "criado_por": {
            "username": "admin",
            "email": "admin@planify.com",
            "full_name": "",
            "role": "TEAM_MEMBER",
            "profile": null,
            "id": 2,
            "is_active": true,
            "date_joined": "2025-06-05T15:22:06.191229-03:00",
            "access_profiles": []
        },
        "criado_em": "2025-06-11T12:48:26.622748-03:00",
        "atualizado_em": "2025-06-11T12:48:26.622765-03:00",
        "atribuicoes": [
            {
            "id": 55,
            "tarefa": 55,
            "usuario": 2,
            "usuario_nome": "",
            "atribuido_em": "2025-06-11T12:48:26.623418-03:00",
            "atribuido_por": 2,
            "atribuido_por_nome": ""
            }
        ],
        "responsaveis": [
            {
            "usuario__id": 2,
            "usuario__username": "admin",
            "usuario__full_name": ""
            }
        ]
        }
    ],
    "EM_ANDAMENTO": [],
    "FEITO": []
    }

#### OBSERVAÇÕES:

---

## Visualização Kanban do projeto
`PATCH /api/projects/12/kanban/?projeto_id=12`

#### REQ_BODY: 

    {
    "projeto": 12,
    "titulo": "Qual e o nome mesmo?",
    "colunas": [
        {
        "status": "EM_ANDAMENTO",
        "titulo": "EM_ANDAMENTO tambem?",
        "tarefas": [
            {
            "id": 51,
            "titulo": "tarefa modificada",
            "descricao": "modificação",
            "status": "EM_ANDAMENTO",
            "prioridade": "BAIXA",
            "data_inicio": "2025-06-11",
            "data_termino": "2025-06-11",
            "responsaveis": [
                {
                "additionalProp1": "oi?",
                "additionalProp2": "string",
                "additionalProp3": "string"
                }
            ]
            }
        ]
        }
    ]
    }

#### RESPONSE: **400** - Bad request. Faltou o ID da tarefa aparentemente??

    {
    "detail": "ID da tarefa e novo status são obrigatórios."
    }

#### OBSERVAÇÕES:
Para que serve essa rota? A descrição parece estar errada

