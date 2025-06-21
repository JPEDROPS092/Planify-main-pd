"""
Utility functions for the projects app.
Helper functions and constants used across the app.
"""
from django.utils import timezone
from datetime import timedelta
from django.db.models import Q
import re


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


def calculate_project_progress(projeto):
    """
    Calculates project progress based on completed tasks.
    
    Args:
        projeto: Project instance
        
    Returns:
        dict: Progress information
    """
    total_tasks = projeto.tarefas.count()
    
    if total_tasks == 0:
        return {
            'total_tasks': 0,
            'completed_tasks': 0,
            'progress_percentage': 0,
            'status': 'no_tasks'
        }
    
    completed_tasks = projeto.tarefas.filter(status='concluida').count()
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


def get_project_health_status(projeto):
    """
    Evaluates project health based on various metrics.
    
    Args:
        projeto: Project instance
        
    Returns:
        dict: Health status information
    """
    today = timezone.now().date()
    health_score = 100
    issues = []
    
    # Check if project is overdue
    if projeto.data_fim and today > projeto.data_fim and projeto.status != 'concluido':
        health_score -= 30
        days_overdue = (today - projeto.data_fim).days
        issues.append(f"Projeto atrasado em {days_overdue} dias")
    
    # Check task completion rate
    progress = calculate_project_progress(projeto)
    if progress['total_tasks'] > 0:
        completion_rate = progress['progress_percentage']
        
        # If project should be near completion but isn't
        if projeto.data_fim:
            total_days = (projeto.data_fim - projeto.data_inicio).days
            elapsed_days = (today - projeto.data_inicio).days
            expected_progress = (elapsed_days / total_days) * 100 if total_days > 0 else 0
            
            if completion_rate < expected_progress - 20:  # 20% tolerance
                health_score -= 20
                issues.append("Taxa de conclusão abaixo do esperado")
    
    # Check for blocked tasks
    blocked_tasks = projeto.tarefas.filter(status='bloqueada').count()
    if blocked_tasks > 0:
        health_score -= min(blocked_tasks * 5, 25)  # Max 25 points deduction
        issues.append(f"{blocked_tasks} tarefa(s) bloqueada(s)")
    
    # Check team activity (simplified)
    recent_activity = projeto.tarefas.filter(
        atualizado_em__gte=timezone.now() - timedelta(days=7)
    ).count()
    
    if recent_activity == 0 and projeto.status == 'em_andamento':
        health_score -= 15
        issues.append("Nenhuma atividade recente")
    
    # Determine health status
    if health_score >= 80:
        status = 'healthy'
    elif health_score >= 60:
        status = 'warning'
    else:
        status = 'critical'
    
    return {
        'health_score': max(health_score, 0),
        'status': status,
        'issues': issues,
        'recommendations': _get_health_recommendations(status, issues)
    }


def _get_health_recommendations(status, issues):
    """
    Provides recommendations based on project health status.
    
    Args:
        status: Health status
        issues: List of identified issues
        
    Returns:
        list: List of recommendations
    """
    recommendations = []
    
    if status == 'critical':
        recommendations.append("Atenção urgente necessária")
        recommendations.append("Revisar cronograma e recursos")
    
    if "atrasado" in str(issues):
        recommendations.append("Redefinir prazos ou aumentar recursos")
    
    if "bloqueada" in str(issues):
        recommendations.append("Resolver impedimentos nas tarefas")
    
    if "atividade recente" in str(issues):
        recommendations.append("Aumentar engajamento da equipe")
    
    if "Taxa de conclusão" in str(issues):
        recommendations.append("Acelerar desenvolvimento ou revisar escopo")
    
    return recommendations


def search_projects(queryset, search_term):
    """
    Performs search across project fields.
    
    Args:
        queryset: Project queryset
        search_term: Search term
        
    Returns:
        QuerySet: Filtered queryset
    """
    if not search_term:
        return queryset
    
    return queryset.filter(
        Q(titulo__icontains=search_term) |
        Q(descricao__icontains=search_term) |
        Q(criado_por__username__icontains=search_term) |
        Q(criado_por__first_name__icontains=search_term) |
        Q(criado_por__last_name__icontains=search_term)
    )


def format_duration(start_date, end_date=None):
    """
    Formats duration between two dates in a human-readable format.
    
    Args:
        start_date: Start date
        end_date: End date (defaults to today)
        
    Returns:
        str: Formatted duration
    """
    if not end_date:
        end_date = timezone.now().date()
    
    delta = end_date - start_date
    days = delta.days
    
    if days == 0:
        return "Hoje"
    elif days == 1:
        return "1 dia"
    elif days < 30:
        return f"{days} dias"
    elif days < 365:
        months = days // 30
        remaining_days = days % 30
        if remaining_days == 0:
            return f"{months} mês" if months == 1 else f"{months} meses"
        else:
            return f"{months}m {remaining_days}d"
    else:
        years = days // 365
        remaining_days = days % 365
        months = remaining_days // 30
        
        if months == 0:
            return f"{years} ano" if years == 1 else f"{years} anos"
        else:
            return f"{years}a {months}m"


# Constants for project management
PROJECT_STATUS_COLORS = {
    'pendente': '#FFA500',      # Orange
    'em_andamento': '#007BFF',  # Blue
    'pausado': '#FFC107',       # Yellow
    'concluido': '#28A745',     # Green
    'cancelado': '#DC3545',     # Red
}

PRIORITY_COLORS = {
    'baixa': '#6C757D',         # Gray
    'media': '#FFC107',         # Yellow
    'alta': '#FD7E14',          # Orange
    'critica': '#DC3545',       # Red
}

TASK_STATUS_ICONS = {
    'pendente': '⏳',
    'em_andamento': '🔄',
    'bloqueada': '🚫',
    'concluida': '✅',
    'cancelada': '❌',
}
