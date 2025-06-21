"""
Business logic services for the dashboard app.
Handles metrics calculation and data aggregation.
"""
from django.db.models import Count, Sum, Avg, Q
from django.utils import timezone
from datetime import timedelta, date
from projects.models import Projeto, Sprint, MembroProjeto
from tasks.models import Tarefa, AtribuicaoTarefa
from django.contrib.auth import get_user_model

User = get_user_model()


class DashboardService:
    """Service class for dashboard metrics and analytics."""
    
    @staticmethod
    def get_overview_metrics():
        """
        Returns general overview metrics for the dashboard.
        """
        return {
            'projects': {
                'total': Projeto.objects.count(),
                'active': Projeto.objects.filter(arquivado=False).count(),
                'completed': Projeto.objects.filter(status='concluido').count(),
                'in_progress': Projeto.objects.filter(status='em_andamento').count(),
            },
            'tasks': {
                'total': Tarefa.objects.count(),
                'completed': Tarefa.objects.filter(status='concluida').count(),
                'in_progress': Tarefa.objects.filter(status='em_andamento').count(),
                'pending': Tarefa.objects.filter(status='pendente').count(),
                'blocked': Tarefa.objects.filter(status='bloqueada').count(),
            },
            'sprints': {
                'total': Sprint.objects.count(),
                'active': Sprint.objects.filter(status='em_andamento').count(),
                'completed': Sprint.objects.filter(status='concluida').count(),
            },
            'users': {
                'total': User.objects.count(),
                'active_projects': MembroProjeto.objects.values('usuario').distinct().count(),
            }
        }
    
    @staticmethod
    def get_project_status_distribution():
        """
        Returns project distribution by status.
        """
        return Projeto.objects.values('status').annotate(
            count=Count('id')
        ).order_by('status')
    
    @staticmethod
    def get_task_status_distribution():
        """
        Returns task distribution by status.
        """
        return Tarefa.objects.values('status').annotate(
            count=Count('id')
        ).order_by('status')
    
    @staticmethod
    def get_priority_distribution():
        """
        Returns task distribution by priority.
        """
        return Tarefa.objects.values('prioridade').annotate(
            count=Count('id')
        ).order_by('prioridade')
    
    @staticmethod
    def get_recent_activity(days=7):
        """
        Returns recent activity summary.
        """
        cutoff_date = timezone.now() - timedelta(days=days)
        
        return {
            'new_projects': Projeto.objects.filter(
                criado_em__gte=cutoff_date
            ).count(),
            'new_tasks': Tarefa.objects.filter(
                criado_em__gte=cutoff_date
            ).count(),
            'completed_tasks': Tarefa.objects.filter(
                status='concluida',
                atualizado_em__gte=cutoff_date
            ).count(),
            'new_sprints': Sprint.objects.filter(
                criado_em__gte=cutoff_date
            ).count(),
        }
    
    @staticmethod
    def get_user_workload():
        """
        Returns user workload statistics.
        """
        return User.objects.annotate(
            assigned_tasks=Count('atribuicoes_tarefa'),
            active_tasks=Count(
                'atribuicoes_tarefa',
                filter=Q(atribuicoes_tarefa__tarefa__status__in=['pendente', 'em_andamento'])
            ),
            completed_tasks=Count(
                'atribuicoes_tarefa',
                filter=Q(atribuicoes_tarefa__tarefa__status='concluida')
            ),
            projects_count=Count('membros_projeto')
        ).filter(
            Q(assigned_tasks__gt=0) | Q(projects_count__gt=0)
        ).order_by('-active_tasks')
    
    @staticmethod
    def get_project_progress():
        """
        Returns project progress statistics.
        """
        projects = Projeto.objects.annotate(
            total_tasks=Count('tarefas'),
            completed_tasks=Count(
                'tarefas',
                filter=Q(tarefas__status='concluida')
            )
        ).filter(total_tasks__gt=0)
        
        project_progress = []
        for project in projects:
            progress_percentage = (
                (project.completed_tasks / project.total_tasks) * 100
                if project.total_tasks > 0 else 0
            )
            project_progress.append({
                'project': {
                    'id': project.id,
                    'titulo': project.titulo,
                    'status': project.status,
                },
                'total_tasks': project.total_tasks,
                'completed_tasks': project.completed_tasks,
                'progress_percentage': round(progress_percentage, 2),
            })
        
        return sorted(project_progress, key=lambda x: x['progress_percentage'], reverse=True)
    
    @staticmethod
    def get_sprint_metrics():
        """
        Returns sprint performance metrics.
        """
        active_sprints = Sprint.objects.filter(status='em_andamento').annotate(
            total_tasks=Count('tarefas'),
            completed_tasks=Count(
                'tarefas',
                filter=Q(tarefas__status='concluida')
            )
        )
        
        sprint_metrics = []
        for sprint in active_sprints:
            progress_percentage = (
                (sprint.completed_tasks / sprint.total_tasks) * 100
                if sprint.total_tasks > 0 else 0
            )
            
            # Calculate days remaining
            days_remaining = None
            if sprint.data_fim:
                days_remaining = (sprint.data_fim - date.today()).days
            
            sprint_metrics.append({
                'sprint': {
                    'id': sprint.id,
                    'nome': sprint.nome,
                    'projeto': sprint.projeto.titulo,
                },
                'total_tasks': sprint.total_tasks,
                'completed_tasks': sprint.completed_tasks,
                'progress_percentage': round(progress_percentage, 2),
                'days_remaining': days_remaining,
                'data_fim': sprint.data_fim,
            })
        
        return sprint_metrics
    
    @staticmethod
    def get_performance_trends(days=30):
        """
        Returns performance trends over the specified period.
        """
        cutoff_date = timezone.now() - timedelta(days=days)
        
        # Daily task completion trend
        daily_completions = []
        for i in range(days):
            day = (timezone.now() - timedelta(days=i)).date()
            completed = Tarefa.objects.filter(
                status='concluida',
                atualizado_em__date=day
            ).count()
            daily_completions.append({
                'date': day,
                'completed_tasks': completed
            })
        
        return {
            'daily_task_completions': list(reversed(daily_completions)),
            'avg_daily_completions': sum(
                day['completed_tasks'] for day in daily_completions
            ) / days if days > 0 else 0,
        }
