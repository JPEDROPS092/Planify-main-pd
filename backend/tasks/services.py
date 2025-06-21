"""
Business logic services for the tasks app.
Handles task lifecycle, assignments, and status changes.
"""
from django.db import transaction
from django.utils import timezone
from django.contrib.auth import get_user_model
from .models import Tarefa, AtribuicaoTarefa, ComentarioTarefa, HistoricoStatusTarefa

User = get_user_model()


class TaskService:
    """Service class for task-related business logic."""
    
    @staticmethod
    def create_task_with_assignments(task_data, assignees=None, created_by=None):
        """
        Creates a task and assigns it to specified users.
        """
        with transaction.atomic():
            # Extract assignees from task_data if not provided separately
            if assignees is None:
                assignees = task_data.pop('assignees', [])
            
            # Create the task
            tarefa = Tarefa.objects.create(**task_data)
            
            # Create assignments
            for user in assignees:
                AtribuicaoTarefa.objects.create(
                    tarefa=tarefa,
                    usuario=user,
                    atribuido_por=created_by
                )
            
            return tarefa
    
    @staticmethod
    def change_task_status(tarefa, new_status, changed_by, comment=None):
        """
        Changes task status and creates history record.
        Handles business rules for status transitions.
        """
        if tarefa.status == new_status:
            return tarefa
        
        # Validate status transition
        TaskService._validate_status_transition(tarefa.status, new_status)
        
        with transaction.atomic():
            old_status = tarefa.status
            tarefa.status = new_status
            
            # Set completion date if task is being completed
            if new_status == 'concluida':
                tarefa.data_termino = timezone.now()
            
            tarefa.save()
            
            # Create history record
            HistoricoStatusTarefa.objects.create(
                tarefa=tarefa,
                status_anterior=old_status,
                status_novo=new_status,
                alterado_por=changed_by,
                observacao=comment
            )
            
            # Add comment if provided
            if comment:
                ComentarioTarefa.objects.create(
                    tarefa=tarefa,
                    autor=changed_by,
                    conteudo=f"Status alterado para '{new_status}': {comment}"
                )
            
            return tarefa
    
    @staticmethod
    def _validate_status_transition(current_status, new_status):
        """
        Validates if a status transition is allowed.
        """
        # Define allowed transitions
        allowed_transitions = {
            'pendente': ['em_andamento', 'cancelada'],
            'em_andamento': ['pendente', 'concluida', 'bloqueada'],
            'bloqueada': ['em_andamento', 'cancelada'],
            'concluida': ['em_andamento'],  # Allow reopening
            'cancelada': ['pendente']  # Allow reactivation
        }
        
        if new_status not in allowed_transitions.get(current_status, []):
            raise ValueError(
                f"Transição inválida de '{current_status}' para '{new_status}'"
            )
    
    @staticmethod
    def assign_task(tarefa, usuario, assigned_by):
        """
        Assigns a task to a user.
        """
        # Check if already assigned
        if AtribuicaoTarefa.objects.filter(tarefa=tarefa, usuario=usuario).exists():
            raise ValueError(f"Tarefa já está atribuída ao usuário {usuario}")
        
        return AtribuicaoTarefa.objects.create(
            tarefa=tarefa,
            usuario=usuario,
            atribuido_por=assigned_by
        )
    
    @staticmethod
    def unassign_task(tarefa, usuario):
        """
        Removes a user assignment from a task.
        """
        try:
            assignment = AtribuicaoTarefa.objects.get(tarefa=tarefa, usuario=usuario)
            assignment.delete()
            return True
        except AtribuicaoTarefa.DoesNotExist:
            return False
    
    @staticmethod
    def add_comment(tarefa, autor, conteudo, parent_comment=None):
        """
        Adds a comment to a task.
        """
        return ComentarioTarefa.objects.create(
            tarefa=tarefa,
            autor=autor,
            conteudo=conteudo,
            comentario_pai=parent_comment
        )
    
    @staticmethod
    def estimate_task_completion(tarefa):
        """
        Estimates task completion based on current progress and historical data.
        """
        if tarefa.status == 'concluida':
            return 100
        
        if tarefa.status == 'cancelada':
            return 0
        
        # Simple estimation based on status
        status_progress = {
            'pendente': 0,
            'em_andamento': 50,
            'bloqueada': 25,
        }
        
        return status_progress.get(tarefa.status, 0)
    
    @staticmethod
    def get_task_metrics(tarefa):
        """
        Returns various metrics for a task.
        """
        return {
            'assignees_count': tarefa.atribuicoes.count(),
            'comments_count': tarefa.comentarios.count(),
            'status_changes_count': tarefa.historico_status.count(),
            'days_since_created': (timezone.now().date() - tarefa.criado_em.date()).days,
            'estimated_completion': TaskService.estimate_task_completion(tarefa),
            'is_overdue': (
                tarefa.data_termino_prevista and 
                timezone.now().date() > tarefa.data_termino_prevista and 
                tarefa.status != 'concluida'
            ) if hasattr(tarefa, 'data_termino_prevista') else False
        }
