# tasks/serializers.py

from rest_framework import serializers
from .models import (
    Tarefa,
    AtribuicaoTarefa,
    ComentarioTarefa,
    HistoricoStatusTarefa,
    Sprint,
)
from users.serializers import UserSerializer

# --- Serializers para Actions Customizadas ---


class AssignUserSerializer(serializers.Serializer):
    """Serializer para atribuir/remover um usuário de uma tarefa."""

    usuario_id = serializers.IntegerField(
        required=True, help_text="ID do usuário a ser manipulado."
    )

    class Meta:
        ref_name = "TasksAssignUser"


class AddCommentSerializer(serializers.Serializer):
    """Serializer para adicionar um comentário a uma tarefa."""

    texto = serializers.CharField(
        required=True, allow_blank=False, help_text="Conteúdo do comentário."
    )

    class Meta:
        ref_name = "TasksAddComment"


class UpdateStatusSerializer(serializers.Serializer):
    """Serializer para atualizar o status de uma tarefa."""

    status = serializers.ChoiceField(choices=Tarefa.STATUS_CHOICES, required=True)
    comentario = serializers.CharField(
        required=False,
        allow_blank=True,
        help_text="Comentário opcional sobre a mudança de status.",
    )

    class Meta:
        ref_name = "TasksUpdateStatus"


class AssociarSprintSerializer(serializers.Serializer):
    """Serializer para a action de associar uma tarefa a uma sprint."""

    sprint_id = serializers.IntegerField(
        allow_null=True,
        required=True,
        help_text="ID da sprint para associar. Envie 'null' para desassociar.",
    )

    def validate_sprint_id(self, value):
        """Valida se a sprint existe (se não for nula)."""
        if value is not None and not Sprint.objects.filter(id=value).exists():
            raise serializers.ValidationError("A Sprint com o ID fornecido não existe.")
        return value

    class Meta:
        ref_name = "TasksAssociarSprint"


# --- Serializers de Modelo ---


class ComentarioTarefaSerializer(serializers.ModelSerializer):
    autor = UserSerializer(read_only=True)

    class Meta:
        model = ComentarioTarefa
        fields = ["id", "tarefa", "autor", "texto", "criado_em"]
        read_only_fields = ["id", "autor", "criado_em"]


class HistoricoStatusTarefaSerializer(serializers.ModelSerializer):
    alterado_por = UserSerializer(read_only=True)

    class Meta:
        model = HistoricoStatusTarefa
        fields = [
            "id",
            "tarefa",
            "status_anterior",
            "novo_status",
            "alterado_por",
            "alterado_em",
        ]
        read_only_fields = ["id", "alterado_em"]


class AtribuicaoTarefaSerializer(serializers.ModelSerializer):
    usuario = UserSerializer(read_only=True)
    atribuido_por = UserSerializer(read_only=True)

    class Meta:
        model = AtribuicaoTarefa
        fields = ["id", "tarefa", "usuario", "atribuido_em", "atribuido_por"]
        read_only_fields = ["id", "atribuido_em"]


class TarefaListSerializer(serializers.ModelSerializer):
    """Serializer otimizado para listas de tarefas."""

    atribuicoes = AtribuicaoTarefaSerializer(many=True, read_only=True)

    class Meta:
        model = Tarefa
        fields = [
            "id",
            "titulo",
            "projeto",
            "sprint",
            "status",
            "prioridade",
            "data_termino",
            "atribuicoes",
        ]


class TarefaSerializer(serializers.ModelSerializer):
    """Serializer detalhado para uma única tarefa."""

    criado_por = UserSerializer(read_only=True)
    atribuicoes = AtribuicaoTarefaSerializer(many=True, read_only=True)

    class Meta:
        model = Tarefa
        fields = [
            "id",
            "titulo",
            "descricao",
            "projeto",
            "sprint",
            "data_inicio",
            "data_termino",
            "prioridade",
            "status",
            "criado_por",
            "criado_em",
            "atualizado_em",
            "atribuicoes",
        ]
        read_only_fields = [
            "id",
            "criado_por",
            "criado_em",
            "atualizado_em",
            "atribuicoes",
        ]
