from rest_framework import serializers
from drf_spectacular.utils import extend_schema_serializer, OpenApiExample

class TarefaKanbanSerializer(serializers.Serializer):
    id = serializers.IntegerField(help_text="ID da tarefa")
    titulo = serializers.CharField(help_text="Título da tarefa")
    descricao = serializers.CharField(help_text="Descrição da tarefa")
    status = serializers.CharField(help_text="Status atual da tarefa")
    prioridade = serializers.CharField(help_text="Prioridade da tarefa")
    data_inicio = serializers.DateField(help_text="Data de início da tarefa")
    data_fim = serializers.DateField(help_text="Data de término prevista da tarefa")
    responsaveis = serializers.ListField(
        child=serializers.DictField(),
        help_text="Lista de usuários responsáveis pela tarefa"
    )

class ColunaKanbanSerializer(serializers.Serializer):
    status = serializers.CharField(help_text="Status das tarefas nesta coluna")
    titulo = serializers.CharField(help_text="Título da coluna")
    tarefas = TarefaKanbanSerializer(many=True, help_text="Lista de tarefas nesta coluna")

class KanbanResponseSerializer(serializers.Serializer):
    projeto = serializers.IntegerField(help_text="ID do projeto")
    titulo = serializers.CharField(help_text="Título do projeto")
    colunas = ColunaKanbanSerializer(many=True, help_text="Colunas do quadro Kanban")

class TarefaGanttSerializer(serializers.Serializer):
    id = serializers.IntegerField(help_text="ID da tarefa")
    titulo = serializers.CharField(help_text="Título da tarefa")
    data_inicio = serializers.DateField(help_text="Data de início da tarefa")
    data_fim = serializers.DateField(help_text="Data de término prevista da tarefa")
    progresso = serializers.FloatField(help_text="Percentual de conclusão da tarefa")
    dependencias = serializers.ListField(
        child=serializers.IntegerField(),
        help_text="IDs das tarefas das quais esta tarefa depende"
    )

class GanttResponseSerializer(serializers.Serializer):
    projeto = serializers.IntegerField(help_text="ID do projeto")
    titulo = serializers.CharField(help_text="Título do projeto")
    tarefas = TarefaGanttSerializer(many=True, help_text="Tarefas do projeto para visualização Gantt")

class ProjetoDashboardResponseSerializer(serializers.Serializer):
    projeto = serializers.DictField(help_text="Detalhes do projeto")
    sprints = serializers.ListField(help_text="Lista de sprints do projeto")
    tarefas_kanban = serializers.DictField(help_text="Tarefas agrupadas por status para visualização Kanban")
    metricas = serializers.DictField(help_text="Métricas do projeto")
    atividades_recentes = serializers.ListField(help_text="Atividades recentes no projeto")

class ErrorResponseSerializer(serializers.Serializer):
    detail = serializers.CharField(help_text="Mensagem de erro detalhada")

class TarefaCreateSerializer(serializers.Serializer):
    titulo = serializers.CharField(help_text="Título da tarefa")
    descricao = serializers.CharField(help_text="Descrição da tarefa", required=False, allow_null=True)
    data_inicio = serializers.DateField(help_text="Data de início da tarefa")
    data_fim = serializers.DateField(help_text="Data de término prevista da tarefa")
    prioridade = serializers.ChoiceField(
        choices=["BAIXA", "MEDIA", "ALTA"],
        help_text="Prioridade da tarefa"
    )
    status = serializers.ChoiceField(
        choices=["PENDENTE", "EM_ANDAMENTO", "CONCLUIDA", "BLOQUEADA"],
        help_text="Status inicial da tarefa"
    )
    responsaveis = serializers.ListField(
        child=serializers.IntegerField(),
        help_text="IDs dos usuários responsáveis pela tarefa",
        required=False
    )

class TarefasBulkCreateSerializer(serializers.Serializer):
    tarefas = TarefaCreateSerializer(many=True, help_text="Lista de tarefas a serem criadas em lote")

class ExportResponseSerializer(serializers.Serializer):
    url = serializers.URLField(help_text="URL para download do arquivo exportado")
    formato = serializers.CharField(help_text="Formato do arquivo exportado")
