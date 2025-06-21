"""
Business logic services for the projects app.
Centralizes complex business rules and keeps views clean.
"""
from django.db import transaction
from django.utils import timezone
from django.contrib.auth import get_user_model
from .models import Projeto, Sprint, MembroProjeto, HistoricoStatusProjeto

User = get_user_model()


class ProjectService:
    """Service class for project-related business logic."""
    
    @staticmethod
    def create_project_with_creator_as_admin(project_data, creator):
        """
        Creates a project and automatically adds the creator as admin.
        """
        with transaction.atomic():
            # Create the project
            projeto = Projeto.objects.create(
                criado_por=creator,
                **project_data
            )
            
            # Add creator as project admin
            MembroProjeto.objects.create(
                projeto=projeto,
                usuario=creator,
                papel='administrador'
            )
            
            return projeto
    
    @staticmethod
    def change_project_status(projeto, new_status, changed_by, reason=None):
        """
        Changes project status and creates history record.
        """
        if projeto.status == new_status:
            return projeto
            
        with transaction.atomic():
            old_status = projeto.status
            projeto.status = new_status
            projeto.save()
            
            # Create history record
            HistoricoStatusProjeto.objects.create(
                projeto=projeto,
                status_anterior=old_status,
                alterado_por=changed_by,
                observacao=reason
            )
            
            return projeto
    
    @staticmethod
    def add_member_to_project(projeto, usuario, papel='membro', added_by=None):
        """
        Adds a member to a project with specified role.
        """
        # Check if user is already a member
        if MembroProjeto.objects.filter(projeto=projeto, usuario=usuario).exists():
            raise ValueError(f"Usuário {usuario} já é membro do projeto")
        
        return MembroProjeto.objects.create(
            projeto=projeto,
            usuario=usuario,
            papel=papel
        )
    
    @staticmethod
    def archive_project(projeto, archived_by):
        """
        Archives a project and updates related status.
        """
        with transaction.atomic():
            projeto.arquivado = True
            projeto.save()
            
            # Optionally change status to 'concluido' if not already
            if projeto.status != 'concluido':
                ProjectService.change_project_status(
                    projeto, 
                    'concluido', 
                    archived_by, 
                    'Projeto arquivado'
                )
            
            return projeto


class SprintService:
    """Service class for sprint-related business logic."""
    
    @staticmethod
    def create_sprint(sprint_data, projeto):
        """
        Creates a sprint with validation.
        """
        # Validate dates
        if sprint_data.get('data_fim') and sprint_data.get('data_inicio'):
            if sprint_data['data_fim'] <= sprint_data['data_inicio']:
                raise ValueError("Data de fim deve ser posterior à data de início")
        
        return Sprint.objects.create(projeto=projeto, **sprint_data)
    
    @staticmethod
    def complete_sprint(sprint, completed_by):
        """
        Completes a sprint and handles related tasks.
        """
        with transaction.atomic():
            sprint.status = 'concluida'
            sprint.data_fim = timezone.now().date()
            sprint.save()
            
            # Move incomplete tasks to backlog or next sprint
            incomplete_tasks = sprint.tarefas.exclude(status='concluida')
            for task in incomplete_tasks:
                task.sprint = None  # Move to backlog
                task.save()
            
            return sprint
