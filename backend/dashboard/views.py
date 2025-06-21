"""
Views for the dashboard app.
Provides API endpoints for metrics, analytics, and reporting.
"""
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from drf_spectacular.utils import extend_schema, OpenApiParameter
from drf_spectacular.types import OpenApiTypes
from .services import DashboardService


class DashboardOverviewView(APIView):
    """
    Dashboard overview with key metrics.
    """
    permission_classes = [IsAuthenticated]
    
    @extend_schema(
        summary="Get dashboard overview",
        description="Returns overview metrics including projects, tasks, sprints, and users statistics.",
        responses={200: dict}
    )
    def get(self, request):
        """Get dashboard overview metrics."""
        try:
            overview = DashboardService.get_overview_metrics()
            return Response(overview, status=status.HTTP_200_OK)
        except Exception as e:
            return Response(
                {'error': str(e)}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class ProjectMetricsView(APIView):
    """
    Project-related metrics and statistics.
    """
    permission_classes = [IsAuthenticated]
    
    @extend_schema(
        summary="Get project metrics",
        description="Returns project status distribution and progress statistics.",
        responses={200: dict}
    )
    def get(self, request):
        """Get project metrics."""
        try:
            metrics = {
                'status_distribution': list(DashboardService.get_project_status_distribution()),
                'progress': DashboardService.get_project_progress(),
            }
            return Response(metrics, status=status.HTTP_200_OK)
        except Exception as e:
            return Response(
                {'error': str(e)}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class TaskMetricsView(APIView):
    """
    Task-related metrics and statistics.
    """
    permission_classes = [IsAuthenticated]
    
    @extend_schema(
        summary="Get task metrics",
        description="Returns task status and priority distribution.",
        responses={200: dict}
    )
    def get(self, request):
        """Get task metrics."""
        try:
            metrics = {
                'status_distribution': list(DashboardService.get_task_status_distribution()),
                'priority_distribution': list(DashboardService.get_priority_distribution()),
            }
            return Response(metrics, status=status.HTTP_200_OK)
        except Exception as e:
            return Response(
                {'error': str(e)}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class UserMetricsView(APIView):
    """
    User workload and activity metrics.
    """
    permission_classes = [IsAuthenticated]
    
    @extend_schema(
        summary="Get user metrics",
        description="Returns user workload statistics and activity metrics.",
        responses={200: dict}
    )
    def get(self, request):
        """Get user metrics."""
        try:
            workload = DashboardService.get_user_workload()
            metrics = {
                'workload': [
                    {
                        'user': {
                            'id': user.id,
                            'username': user.username,
                            'email': user.email,
                        },
                        'assigned_tasks': user.assigned_tasks,
                        'active_tasks': user.active_tasks,
                        'completed_tasks': user.completed_tasks,
                        'projects_count': user.projects_count,
                    }
                    for user in workload[:20]  # Top 20 users
                ]
            }
            return Response(metrics, status=status.HTTP_200_OK)
        except Exception as e:
            return Response(
                {'error': str(e)}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class SprintMetricsView(APIView):
    """
    Sprint performance metrics.
    """
    permission_classes = [IsAuthenticated]
    
    @extend_schema(
        summary="Get sprint metrics",
        description="Returns active sprint progress and performance metrics.",
        responses={200: dict}
    )
    def get(self, request):
        """Get sprint metrics."""
        try:
            metrics = {
                'active_sprints': DashboardService.get_sprint_metrics(),
            }
            return Response(metrics, status=status.HTTP_200_OK)
        except Exception as e:
            return Response(
                {'error': str(e)}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class PerformanceTrendsView(APIView):
    """
    Performance trends and analytics.
    """
    permission_classes = [IsAuthenticated]
    
    @extend_schema(
        summary="Get performance trends",
        description="Returns performance trends over a specified period.",
        parameters=[
            OpenApiParameter(
                name='days',
                type=OpenApiTypes.INT,
                location=OpenApiParameter.QUERY,
                description='Number of days to analyze (default: 30)',
                default=30
            )
        ],
        responses={200: dict}
    )
    def get(self, request):
        """Get performance trends."""
        try:
            days = int(request.query_params.get('days', 30))
            if days < 1 or days > 365:
                days = 30
            
            trends = DashboardService.get_performance_trends(days)
            return Response(trends, status=status.HTTP_200_OK)
        except Exception as e:
            return Response(
                {'error': str(e)}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class RecentActivityView(APIView):
    """
    Recent activity summary.
    """
    permission_classes = [IsAuthenticated]
    
    @extend_schema(
        summary="Get recent activity",
        description="Returns summary of recent activity in the system.",
        parameters=[
            OpenApiParameter(
                name='days',
                type=OpenApiTypes.INT,
                location=OpenApiParameter.QUERY,
                description='Number of days to look back (default: 7)',
                default=7
            )
        ],
        responses={200: dict}
    )
    def get(self, request):
        """Get recent activity."""
        try:
            days = int(request.query_params.get('days', 7))
            if days < 1 or days > 30:
                days = 7
            
            activity = DashboardService.get_recent_activity(days)
            return Response(activity, status=status.HTTP_200_OK)
        except Exception as e:
            return Response(
                {'error': str(e)}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class ProjectProgressView(APIView):
    """
    Detailed project progress report.
    """
    permission_classes = [IsAuthenticated]
    
    @extend_schema(
        summary="Get project progress report",
        description="Returns detailed progress information for all projects.",
        responses={200: dict}
    )
    def get(self, request):
        """Get project progress report."""
        try:
            progress = DashboardService.get_project_progress()
            return Response({'projects': progress}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response(
                {'error': str(e)}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class UserWorkloadView(APIView):
    """
    Detailed user workload report.
    """
    permission_classes = [IsAuthenticated]
    
    @extend_schema(
        summary="Get user workload report",
        description="Returns detailed workload information for all users.",
        responses={200: dict}
    )
    def get(self, request):
        """Get user workload report."""
        try:
            workload = DashboardService.get_user_workload()
            users_data = [
                {
                    'user': {
                        'id': user.id,
                        'username': user.username,
                        'email': user.email,
                        'first_name': user.first_name,
                        'last_name': user.last_name,
                    },
                    'assigned_tasks': user.assigned_tasks,
                    'active_tasks': user.active_tasks,
                    'completed_tasks': user.completed_tasks,
                    'projects_count': user.projects_count,
                    'workload_ratio': (
                        user.active_tasks / max(user.assigned_tasks, 1)
                    ) * 100,
                }
                for user in workload
            ]
            return Response({'users': users_data}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response(
                {'error': str(e)}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
