"""
URL configuration for the dashboard app.
"""
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

app_name = 'dashboard'

# Create a router for ViewSets
router = DefaultRouter()

urlpatterns = [
    # Include router URLs
    path('', include(router.urls)),
    
    # Dashboard overview
    path('overview/', views.DashboardOverviewView.as_view(), name='overview'),
    
    # Metrics endpoints
    path('metrics/projects/', views.ProjectMetricsView.as_view(), name='project-metrics'),
    path('metrics/tasks/', views.TaskMetricsView.as_view(), name='task-metrics'),
    path('metrics/users/', views.UserMetricsView.as_view(), name='user-metrics'),
    path('metrics/sprints/', views.SprintMetricsView.as_view(), name='sprint-metrics'),
    
    # Analytics endpoints
    path('analytics/trends/', views.PerformanceTrendsView.as_view(), name='performance-trends'),
    path('analytics/activity/', views.RecentActivityView.as_view(), name='recent-activity'),
    
    # Report endpoints
    path('reports/project-progress/', views.ProjectProgressView.as_view(), name='project-progress'),
    path('reports/user-workload/', views.UserWorkloadView.as_view(), name='user-workload'),
]
