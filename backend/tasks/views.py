# tasks/views.py

from typing import Type
from django.db.models.query import QuerySet
from rest_framework import viewsets, status, permissions, filters, serializers
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from django.utils import timezone
from drf_spectacular.utils import extend_schema, extend_schema_view, OpenApiResponse
from drf_spectacular.types import OpenApiTypes

# Importações de modelos e lógicas de negócio
from .models import Tarefa, AtribuicaoTarefa, ComentarioTarefa, HistoricoStatusTarefa
from .filters import TarefaFilter
from .permissions import (
    CanViewTask,
    CanEditTask,
    CanAssignTask,
    CanCommentOnTask,
    CanChangeTaskStatus,
)
from .serializers import (
    TarefaSerializer,
    TarefaListSerializer,
    AtribuicaoTarefaSerializer,
    ComentarioTarefaSerializer,
    HistoricoStatusTarefaSerializer,
    AssignUserSerializer,
    AddCommentSerializer,
    UpdateStatusSerializer,
    AssociarSprintSerializer,
)


@extend_schema_view(
    list=extend_schema(summary="Listar Tarefas", tags=["Tasks"]),
    create=extend_schema(summary="Criar Tarefa", tags=["Tasks"]),
    retrieve=extend_schema(summary="Obter Tarefa", tags=["Tasks"]),
    update=extend_schema(summary="Atualizar Tarefa (Completo)", tags=["Tasks"]),
    partial_update=extend_schema(summary="Atualizar Tarefa (Parcial)", tags=["Tasks"]),
    destroy=extend_schema(summary="Excluir Tarefa", tags=["Tasks"]),
)
class TarefaViewSet(viewsets.ModelViewSet):
    """
    Endpoint para gerenciar Tarefas, suas atribuições, comentários e status.
    Fornece filtragem avançada através de parâmetros de query.
    """

    queryset = Tarefa.objects.all()
    serializer_class = TarefaSerializer
    permission_classes = [permissions.IsAuthenticated, CanEditTask]

    def get_permissions(self):
        """
        Instantiates and returns the list of permissions that this view requires.
        Uses CanViewTask for safe methods (GET) and CanEditTask for unsafe methods.
        """
        if self.action in ['list', 'retrieve']:
            permission_classes = [permissions.IsAuthenticated, CanViewTask]
        else:
            permission_classes = [permissions.IsAuthenticated, CanEditTask]
        return [permission() for permission in permission_classes]

    # Configuração dos backends de filtro, busca e ordenação
    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter,
    ]
    filterset_class = TarefaFilter
    search_fields = ["titulo", "descricao"]
    ordering_fields = ["data_termino", "prioridade", "criado_em", "status"]
    ordering = ["-criado_em"]

    # --- Métodos sobrescritos com Type Hinting correto ---

    def get_serializer_class(self) -> Type[serializers.Serializer]:
        """Retorna o serializer apropriado com base na ação da requisição."""
        if self.action == "list":
            return TarefaListSerializer
        return self.serializer_class

    def get_queryset(self) -> "QuerySet[Tarefa]":
        """Otimiza a consulta ao banco de dados com joins e prefetching."""
        # A lógica de anotação foi movida para o filtro para ser aplicada condicionalmente
        # e evitar sobrecarga em todas as queries.
        return Tarefa.objects.select_related(
            "projeto", "sprint", "criado_por"
        ).prefetch_related("atribuicoes__usuario")

    def perform_create(self, serializer):
        """Define o usuário logado como criador da tarefa."""
        serializer.save(criado_por=self.request.user)

    def perform_update(self, serializer):
        """Define o usuário logado como o último a atualizar a tarefa."""
        serializer.save(atualizado_por=self.request.user)

    # --- Actions Customizadas ---

    @extend_schema(
        summary="Atribuir responsável",
        request=AssignUserSerializer,
        responses={201: AtribuicaoTarefaSerializer},
        tags=["Tasks"],
    )
    @action(
        detail=True,
        methods=["post"],
        permission_classes=[CanAssignTask],
        url_path="assign-user",
    )
    def atribuir_responsavel(self, request, pk=None):
        tarefa = self.get_object()
        serializer = AssignUserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        usuario_id = serializer.validated_data["usuario_id"]

        atribuicao, created = AtribuicaoTarefa.objects.get_or_create(
            tarefa=tarefa,
            usuario_id=usuario_id,
            defaults={"atribuido_por": request.user},
        )
        if not created:
            return Response(
                {"detail": "Usuário já está atribuído a esta tarefa."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        return Response(
            AtribuicaoTarefaSerializer(atribuicao).data, status=status.HTTP_201_CREATED
        )

    @extend_schema(
        summary="Remover responsável",
        request=AssignUserSerializer,
        responses={
            204: OpenApiResponse(description="Responsável removido com sucesso."),
            401: OpenApiResponse(description="Não autorizado."),
            404: OpenApiResponse(description="Atribuição não encontrada."),
        },
        tags=["Tasks"],
    )
    @action(
        detail=True,
        methods=["post"],
        permission_classes=[CanAssignTask],
        url_path="unassign-user",
    )
    def remover_responsavel(self, request, pk=None):
        tarefa = self.get_object()
        serializer = AssignUserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        usuario_id = serializer.validated_data["usuario_id"]

        deleted_count, _ = AtribuicaoTarefa.objects.filter(
            tarefa=tarefa, usuario_id=usuario_id
        ).delete()
        if not deleted_count:
            return Response(
                {"detail": "Atribuição não encontrada."},
                status=status.HTTP_404_NOT_FOUND,
            )

        return Response(status=status.HTTP_204_NO_CONTENT)

    @extend_schema(
        summary="Adicionar comentário",
        request=AddCommentSerializer,
        responses={201: ComentarioTarefaSerializer},
        tags=["Tasks"],
    )
    @action(
        detail=True,
        methods=["post"],
        permission_classes=[CanCommentOnTask],
        url_path="add-comment",
    )
    def adicionar_comentario(self, request, pk=None):
        tarefa = self.get_object()
        serializer = AddCommentSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        comentario = ComentarioTarefa.objects.create(
            tarefa=tarefa, autor=request.user, **serializer.validated_data
        )
        return Response(
            ComentarioTarefaSerializer(comentario).data, status=status.HTTP_201_CREATED
        )

    @extend_schema(
        summary="Associar a uma sprint",
        request=AssociarSprintSerializer,
        responses={200: TarefaSerializer},
        tags=["Tasks"],
    )
    @action(
        detail=True,
        methods=["post"],
        permission_classes=[CanEditTask],
        url_path="associate-sprint",
    )
    def associar_sprint(self, request, pk=None):
        tarefa = self.get_object()
        serializer = AssociarSprintSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        sprint_id = serializer.validated_data.get("sprint_id")

        # Validação adicional para garantir que a sprint pertence ao projeto
        if (
            sprint_id
            and not Sprint.objects.filter(id=sprint_id, projeto=tarefa.projeto).exists()
        ):
            return Response(
                {"detail": "Sprint inválida ou não pertence ao projeto da tarefa."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        tarefa.sprint_id = sprint_id
        tarefa.save(update_fields=["sprint"])
        return Response(self.get_serializer(tarefa).data)

    @extend_schema(
        summary="Atualizar status",
        request=UpdateStatusSerializer,
        responses={200: TarefaSerializer},
        tags=["Tasks"],
    )
    @action(
        detail=True,
        methods=["post"],
        permission_classes=[CanChangeTaskStatus],
        url_path="update-status",
    )
    def atualizar_status(self, request, pk=None):
        tarefa = self.get_object()
        serializer = UpdateStatusSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        novo_status = serializer.validated_data["status"]

        if tarefa.status == novo_status:
            return Response(
                {"detail": "A tarefa já está com este status."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        status_anterior = tarefa.status
        tarefa.status = novo_status
        tarefa.save(update_fields=["status"])

        HistoricoStatusTarefa.objects.create(
            tarefa=tarefa,
            status_anterior=status_anterior,
            novo_status=novo_status,
            alterado_por=request.user,
        )
        return Response(self.get_serializer(tarefa).data)

    @extend_schema(
        summary="Obter histórico de status",
        responses={200: HistoricoStatusTarefaSerializer(many=True)},
        tags=["Tasks"],
    )
    @action(detail=True, methods=["get"], url_path="status-history")
    def historico_status(self, request, pk=None):
        historico = self.get_object().historico_status.order_by("-alterado_em")
        serializer = HistoricoStatusTarefaSerializer(historico, many=True)
        return Response(serializer.data)
