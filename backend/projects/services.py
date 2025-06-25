"""
Business logic services for the projects app.
Centralizes complex business rules and keeps views clean.
"""
from django.db import transaction
from django.utils import timezone
from django.contrib.auth import get_user_model
from datetime import timedelta
import re
from django.core.exceptions import ValidationError
from .models import Projeto, Sprint, MembroProjeto, HistoricoStatusProjeto
from tasks.models import Tarefa

User = get_user_model()


class ProjectService:
    """Service class for project-related business logic."""
    
    @staticmethod
    def validate_project_dates(data_inicio, data_fim):
        """
        Validates project start and end dates.
        
        Args:
            data_inicio: Project start date
            data_fim: Project end date
            
        Returns:
            tuple: (is_valid, error_message)
        """
        if not data_inicio:
            return False, "Data de início é obrigatória"
        
        if data_fim and data_inicio >= data_fim:
            return False, "Data de fim deve ser posterior à data de início"
        
        # Check if start date is not too far in the past
        thirty_days_ago = timezone.now().date() - timedelta(days=30)
        if data_inicio < thirty_days_ago:
            return False, "Data de início não pode ser anterior a 30 dias"
        
        return True, None
    
    @staticmethod
    def generate_project_code(titulo):
        """
        Generates a project code based on the title.
        
        Args:
            titulo: Project title
            
        Returns:
            str: Generated project code
        """
        # Remove special characters and convert to uppercase
        clean_title = re.sub(r'[^a-zA-Z0-9\s]', '', titulo)
        words = clean_title.split()
        
        if len(words) >= 2:
            # Use first letter of first two words
            code = ''.join([word[0].upper() for word in words[:2]])
        else:
            # Use first 3 characters of the title
            code = clean_title[:3].upper()
        
        # Add timestamp suffix to ensure uniqueness
        timestamp = timezone.now().strftime('%m%d')
        return f"{code}-{timestamp}"
    
    @staticmethod
    def calculate_project_progress(projeto):
        """
        Calculates project progress based on completed tasks.
        
        Args:
            projeto: Project instance
            
        Returns:
            int: Progress percentage (0-100)
        """
        tasks = Tarefa.objects.filter(projeto=projeto)
        total_tasks = tasks.count()
        
        if total_tasks == 0:
            return 0
        
        completed_tasks = tasks.filter(status='FEITO').count()
        return int((completed_tasks / total_tasks) * 100)
    
    @staticmethod
    def get_project_tasks_stats(projeto):
        """
        Gets detailed task statistics for a project.
        
        Args:
            projeto: Project instance
            
        Returns:
            dict: Task statistics
        """
        tasks = Tarefa.objects.filter(projeto=projeto)
        total_tasks = tasks.count()
        
        if total_tasks == 0:
            return {
                'total_tasks': 0,
                'completed_tasks': 0,
                'progress_percentage': 0,
                'status': 'no_tasks'
            }
        
        completed_tasks = tasks.filter(status='FEITO').count()
        progress_percentage = (completed_tasks / total_tasks) * 100
        
        # Determine status based on progress
        if progress_percentage == 100:
            status = 'completed'
        elif progress_percentage >= 75:
            status = 'near_completion'
        elif progress_percentage >= 25:
            status = 'in_progress'
        else:
            status = 'started'
        
        return {
            'total_tasks': total_tasks,
            'completed_tasks': completed_tasks,
            'progress_percentage': round(progress_percentage, 2),
            'status': status
        }
    
    @staticmethod
    def is_project_delayed(projeto):
        """
        Checks if a project is delayed.
        
        Args:
            projeto: Project instance
            
        Returns:
            bool: True if project is delayed, False otherwise
        """
        hoje = timezone.now().date()
        return projeto.data_fim < hoje and projeto.status != 'CONCLUIDO'
    
    @staticmethod
    def get_remaining_days(projeto):
        """
        Calculates the number of days remaining until the project end date.
        
        Args:
            projeto: Project instance
            
        Returns:
            int: Number of days remaining (0 if end date has passed)
        """
        hoje = timezone.now().date()
        if projeto.data_fim < hoje:
            return 0
        return (projeto.data_fim - hoje).days
    
    @staticmethod
    def create_project_with_creator_as_admin(project_data, creator):
        """
        Creates a project and automatically adds the creator as admin.
        """
        # Validate dates
        is_valid, error_message = ProjectService.validate_project_dates(
            project_data.get('data_inicio'), project_data.get('data_fim')
        )
        
        if not is_valid:
            raise ValidationError({"error": error_message})
            
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
                papel='GERENTE'
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
    def add_member_to_project(projeto, usuario, papel='MEMBRO', added_by=None):
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
            if projeto.status != 'CONCLUIDO':
                ProjectService.change_project_status(
                    projeto, 
                    'CONCLUIDO', 
                    archived_by, 
                    'Projeto arquivado'
                )
            
            return projeto


class SprintService:
    """Service class for sprint-related business logic."""
    
    @staticmethod
    def calculate_sprint_progress(sprint):
        """
        Calculates sprint progress based on completed tasks.
        
        Args:
            sprint: Sprint instance
            
        Returns:
            int: Progress percentage (0-100)
        """
        tasks = Tarefa.objects.filter(sprint=sprint)
        total_tasks = tasks.count()
        
        if total_tasks == 0:
            return 0
        
        completed_tasks = tasks.filter(status='FEITO').count()
        return int((completed_tasks / total_tasks) * 100)
    
    @staticmethod
    def create_sprint(sprint_data, projeto):
        """Creates a new sprint for a project"""
        # Implementation goes here
        pass
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
