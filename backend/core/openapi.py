from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiResponse, OpenApiExample
from drf_spectacular.types import OpenApiTypes

# Schemas para views que não têm serializers definidos
dashboard_schema = {
    "type": "object",
    "properties": {
        "total_projetos": {"type": "integer"},
        "projetos_ativos": {"type": "integer"},
        "projetos_concluidos": {"type": "integer"},
        "projetos_atrasados": {"type": "integer"},
        "total_tarefas": {"type": "integer"},
        "tarefas_pendentes": {"type": "integer"},
        "tarefas_em_andamento": {"type": "integer"},
        "tarefas_concluidas": {"type": "integer"},
        "tarefas_atrasadas": {"type": "integer"}
    }
}

projeto_dashboard_schema = {
    "type": "object",
    "properties": {
        "id": {"type": "integer"},
        "titulo": {"type": "string"},
        "descricao": {"type": "string"},
        "data_inicio": {"type": "string", "format": "date"},
        "data_fim": {"type": "string", "format": "date"},
        "status": {"type": "string", "enum": ["PLANEJAMENTO", "EM_ANDAMENTO", "CONCLUIDO", "PAUSADO", "CANCELADO"]},
        "progresso": {"type": "number", "format": "float"},
        "total_tarefas": {"type": "integer"},
        "tarefas_concluidas": {"type": "integer"},
        "dias_restantes": {"type": "integer"},
        "membros": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "id": {"type": "integer"},
                    "nome": {"type": "string"},
                    "email": {"type": "string"},
                    "papel": {"type": "string"}
                }
            }
        }
    }
}

gantt_schema = {
    "type": "object",
    "properties": {
        "projeto": {"type": "integer"},
        "titulo": {"type": "string"},
        "tarefas": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "id": {"type": "integer"},
                    "titulo": {"type": "string"},
                    "data_inicio": {"type": "string", "format": "date"},
                    "data_fim": {"type": "string", "format": "date"},
                    "progresso": {"type": "number", "format": "float"},
                    "dependencias": {
                        "type": "array",
                        "items": {"type": "integer"}
                    }
                }
            }
        }
    }
}

kanban_schema = {
    "type": "object",
    "properties": {
        "projeto": {"type": "integer"},
        "titulo": {"type": "string"},
        "colunas": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "status": {"type": "string"},
                    "titulo": {"type": "string"},
                    "tarefas": {
                        "type": "array",
                        "items": {
                            "type": "object",
                            "properties": {
                                "id": {"type": "integer"},
                                "titulo": {"type": "string"},
                                "descricao": {"type": "string"},
                                "prioridade": {"type": "string"},
                                "responsaveis": {
                                    "type": "array",
                                    "items": {
                                        "type": "object",
                                        "properties": {
                                            "id": {"type": "integer"},
                                            "nome": {"type": "string"}
                                        }
                                    }
                                }
                            }
                        }
                    }
                }
            }
        }
    }
}

export_schema = {
    "type": "object",
    "properties": {
        "projeto": {"type": "integer"},
        "formato": {"type": "string", "enum": ["pdf", "excel", "csv"]},
        "url_download": {"type": "string"}
    }
}

tarefa_create_schema = {
    "type": "object",
    "properties": {
        "titulo": {"type": "string"},
        "descricao": {"type": "string"},
        "data_inicio": {"type": "string", "format": "date"},
        "data_fim": {"type": "string", "format": "date"},
        "prioridade": {"type": "string", "enum": ["BAIXA", "MEDIA", "ALTA"]},
        "status": {"type": "string", "enum": ["PENDENTE", "EM_ANDAMENTO", "CONCLUIDA", "BLOQUEADA"]},
        "responsaveis": {
            "type": "array",
            "items": {"type": "integer"}
        }
    },
    "required": ["titulo", "projeto", "data_inicio", "data_fim", "prioridade", "status"]
}

tarefas_bulk_create_schema = {
    "type": "object",
    "properties": {
        "tarefas": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "titulo": {"type": "string"},
                    "descricao": {"type": "string"},
                    "data_inicio": {"type": "string", "format": "date"},
                    "data_fim": {"type": "string", "format": "date"},
                    "prioridade": {"type": "string", "enum": ["BAIXA", "MEDIA", "ALTA"]},
                    "status": {"type": "string", "enum": ["PENDENTE", "EM_ANDAMENTO", "CONCLUIDA", "BLOQUEADA"]},
                    "responsaveis": {
                        "type": "array",
                        "items": {"type": "integer"}
                    }
                },
                "required": ["titulo", "data_inicio", "data_fim", "prioridade", "status"]
            }
        }
    },
    "required": ["tarefas"]
}

health_check_schema = {
    "type": "object",
    "properties": {
        "status": {"type": "string"},
        "database": {"type": "string"},
        "version": {"type": "string"}
    }
}
